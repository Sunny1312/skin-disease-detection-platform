"""
Comprehensive evaluation with ROC-AUC, confusion matrix, per-class metrics.
Generates publication-ready figures.
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
)
from torch.utils.data import DataLoader
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    DATASET_PATH,
    OUTPUT_DIR,
    CHECKPOINT_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    NUM_WORKERS,
    NUM_CLASSES,
    CLASS_NAMES,
    TRAIN_RATIO,
    VAL_RATIO,
    TEST_RATIO,
    RANDOM_SEED,
)
from data.dataset import SkinDataset, get_transforms, prepare_splits
from models.hybrid_model import create_model


def plot_confusion_matrix(cm, output_path):
    """Save confusion matrix as publication-ready figure."""
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        annot_kws={"size": 8},
    )
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix - Skin Disease Classification")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_roc_curves(y_true, y_proba, output_path):
    """Plot one-vs-rest ROC curves for each class."""
    n_classes = len(CLASS_NAMES)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    y_true_bin = np.eye(n_classes)[y_true]

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_proba[:, i])
        roc_auc[i] = roc_auc_score(y_true_bin[:, i], y_proba[:, i])

    # Macro average
    fpr["macro"], tpr["macro"], _ = roc_curve(y_true_bin.ravel(), y_proba.ravel())
    roc_auc["macro"] = roc_auc_score(y_true_bin, y_proba, average="macro", multi_class="ovr")

    plt.figure(figsize=(10, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, n_classes))
    for i, name in enumerate(CLASS_NAMES):
        plt.plot(fpr[i], tpr[i], color=colors[i], lw=2,
                 label=f"{name} (AUC={roc_auc[i]:.2f})")
    plt.plot(fpr["macro"], tpr["macro"], "k--", lw=2, label=f"Macro (AUC={roc_auc['macro']:.2f})")
    plt.plot([0, 1], [0, 1], "gray", lw=1, linestyle="--")
    plt.xlim([0, 1])
    plt.ylim([0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves (One-vs-Rest)")
    plt.legend(loc="lower right", fontsize=7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")
    return roc_auc


def plot_per_class_metrics(metrics_df, output_path):
    """Bar chart of per-class precision, recall, F1."""
    x = np.arange(len(CLASS_NAMES))
    width = 0.25
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - width, metrics_df["precision"], width, label="Precision")
    ax.bar(x, metrics_df["recall"], width, label="Recall")
    ax.bar(x + width, metrics_df["f1"], width, label="F1")
    ax.set_xticks(x)
    ax.set_xticklabels(CLASS_NAMES, rotation=45, ha="right")
    ax.legend()
    ax.set_title("Per-Class Performance Metrics")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Evaluating on: {device}")

    ckpt_path = CHECKPOINT_DIR / "best_model.pt"
    if not ckpt_path.exists():
        print("No trained model found. Run train.py first.")
        return

    ckpt = torch.load(ckpt_path, map_location=device)
    config = ckpt.get("config", {})
    class_names = config.get("class_names", CLASS_NAMES)

    model = create_model(
        num_classes=config.get("num_classes", NUM_CLASSES),
        backbone=config.get("backbone", "efficientnet_b0"),
        pretrained=False,
        embed_dim=config.get("embed_dim", 256),
    )
    model.load_state_dict(ckpt["model_state_dict"])
    model = model.to(device)
    model.eval()

    _, _, _, _, test_paths, test_labels = prepare_splits(
        DATASET_PATH,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        seed=RANDOM_SEED,
    )

    test_ds = SkinDataset(
        test_paths,
        test_labels,
        transform=get_transforms(IMAGE_SIZE, is_training=False),
        is_training=False,
    )
    test_loader = DataLoader(
        test_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
    )

    all_preds = []
    all_proba = []
    all_labels = []

    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="Evaluating"):
            images = images.to(device)
            _, class_logits = model(images)
            proba = torch.softmax(class_logits, dim=1).cpu().numpy()
            preds = class_logits.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_proba.extend(proba)
            all_labels.extend(labels.numpy())

    all_preds = np.array(all_preds)
    all_proba = np.array(all_proba)
    all_labels = np.array(all_labels)

    # Overall metrics
    acc = accuracy_score(all_labels, all_preds)
    f1_macro = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    f1_weighted = f1_score(all_labels, all_preds, average="weighted", zero_division=0)
    prec_macro = precision_score(all_labels, all_preds, average="macro", zero_division=0)
    rec_macro = recall_score(all_labels, all_preds, average="macro", zero_division=0)

    try:
        roc_auc_macro = roc_auc_score(all_labels, all_proba, average="macro", multi_class="ovr")
        roc_auc_weighted = roc_auc_score(all_labels, all_proba, average="weighted", multi_class="ovr")
    except Exception as e:
        print(f"ROC-AUC calc warning: {e}")
        roc_auc_macro = roc_auc_weighted = 0

    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"Accuracy:       {acc:.4f}")
    print(f"F1 (macro):     {f1_macro:.4f}")
    print(f"F1 (weighted):  {f1_weighted:.4f}")
    print(f"Precision:      {prec_macro:.4f}")
    print(f"Recall:         {rec_macro:.4f}")
    print(f"ROC-AUC macro:  {roc_auc_macro:.4f}")
    print(f"ROC-AUC weighted: {roc_auc_weighted:.4f}")

    report = classification_report(
        all_labels, all_preds, target_names=class_names, zero_division=0, output_dict=True
    )

    cm = confusion_matrix(all_labels, all_preds)
    OUTPUT_DIR.mkdir(exist_ok=True)

    plot_confusion_matrix(cm, OUTPUT_DIR / "confusion_matrix.png")
    roc_auc_dict = plot_roc_curves(all_labels, all_proba, OUTPUT_DIR / "roc_curves.png")

    # Per-class metrics for bar chart
    metrics_data = []
    for i, name in enumerate(class_names):
        if name in report:
            metrics_data.append({
                "class": name,
                "precision": report[name]["precision"],
                "recall": report[name]["recall"],
                "f1": report[name]["f1-score"],
                "support": report[name]["support"],
            })
        else:
            metrics_data.append({
                "class": name,
                "precision": 0, "recall": 0, "f1": 0, "support": 0,
            })

    import pandas as pd
    df = pd.DataFrame(metrics_data)
    plot_per_class_metrics(df, OUTPUT_DIR / "per_class_metrics.png")

    # Save full report
    full_metrics = {
        "accuracy": acc,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "precision_macro": prec_macro,
        "recall_macro": rec_macro,
        "roc_auc_macro": roc_auc_macro,
        "roc_auc_weighted": roc_auc_weighted,
        "per_class": metrics_data,
        "roc_auc_per_class": {class_names[i]: float(roc_auc_dict.get(i, 0)) for i in range(len(class_names))},
    }
    with open(OUTPUT_DIR / "evaluation_report.json", "w") as f:
        json.dump(full_metrics, f, indent=2)

    print(f"\nReport saved to {OUTPUT_DIR / 'evaluation_report.json'}")


if __name__ == "__main__":
    main()
