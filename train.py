"""
Training script for Skin Disease Classification.
Optimized for speed and guaranteed learning on limited hardware.
Uses: OneCycleLR, Mixed Precision, Focal Loss, Early Stopping
"""

import os
import sys
import json
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
)
import numpy as np
from tqdm import tqdm

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    DATASET_PATH,
    OUTPUT_DIR,
    CHECKPOINT_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    NUM_WORKERS,
    NUM_EPOCHS,
    LEARNING_RATE,
    USE_AMP,
    GRADIENT_CLIP,
    BACKBONE,
    PRETRAINED,
    NUM_CLASSES,
    EMBED_DIM,
    TRAIN_RATIO,
    VAL_RATIO,
    TEST_RATIO,
    RANDOM_SEED,
    EARLY_STOPPING_PATIENCE,
    CLASS_NAMES,
    LR_PATIENCE,
    LR_FACTOR,
    MIN_LR,
    set_seed,
)
from data.dataset import (
    SkinDataset,
    get_transforms,
    prepare_splits,
    compute_class_weights,
    get_oversampled_indices,
)

from models.hybrid_model import create_model
from models.losses import DualHeadLoss


def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer,
    scaler,
    device,
    use_amp,
):
    model.train()
    total_loss = 0
    all_preds, all_labels = [], []

    pbar = tqdm(loader, desc="Train", leave=False)
    for images, labels in pbar:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)

        with torch.amp.autocast(device_type="cuda", enabled=use_amp):
            binary_logits, class_logits = model(images)
            loss = criterion(binary_logits, class_logits, labels)

        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), GRADIENT_CLIP)
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item()
        preds = class_logits.argmax(dim=1).cpu().numpy()
        all_preds.extend(preds)
        all_labels.extend(labels.cpu().numpy())
        pbar.set_postfix({"loss": f"{loss.item():.4f}"})

    avg_loss = total_loss / len(loader)
    acc = accuracy_score(all_labels, all_preds)
    f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    return avg_loss, acc, f1


@torch.no_grad()
def validate(model, loader, criterion, device, use_amp):
    model.eval()
    total_loss = 0
    all_preds, all_labels = [], []

    for images, labels in tqdm(loader, desc="Val", leave=False):
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        with torch.amp.autocast(device_type="cuda", enabled=use_amp):
            binary_logits, class_logits = model(images)
            loss = criterion(binary_logits, class_logits, labels)

        total_loss += loss.item()
        preds = class_logits.argmax(dim=1).cpu().numpy()
        all_preds.extend(preds)
        all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(loader)
    acc = accuracy_score(all_labels, all_preds)
    f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    return avg_loss, acc, f1


def main():
    set_seed(RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    if device.type == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="Resume training from best_model.pt")
    parser.add_argument("--backbone", type=str, default=BACKBONE, help="Backbone model name")
    parser.add_argument("--no-attention", action="store_true", help="Disable attention mechanism")
    parser.add_argument("--no-fusion", action="store_true", help="Disable multi-scale fusion")
    parser.add_argument("--suffix", type=str, default="", help="Suffix for output files")
    parser.add_argument("--epochs", type=int, default=NUM_EPOCHS, help="Number of epochs")
    args = parser.parse_args()

    use_attention = not args.no_attention
    use_fusion = not args.no_fusion
    backbone_name = args.backbone
    num_epochs = args.epochs

    # Update output paths with suffix if provided
    suffix = args.suffix
    if suffix and not suffix.startswith("_"):
        suffix = "_" + suffix

    log_file = OUTPUT_DIR / f"training_log{suffix}.csv"
    ckpt_path = CHECKPOINT_DIR / f"best_model{suffix}.pt"

    # Prepare data
    print("Preparing data splits...")
    train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = prepare_splits(
        DATASET_PATH,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        seed=RANDOM_SEED,
    )

    # Oversample minority classes for training (speeds up learning on rare classes)
    train_indices = get_oversampled_indices(train_paths, train_labels, max_per_class=3000)
    train_paths = [train_paths[i] for i in train_indices]
    train_labels = [train_labels[i] for i in train_indices]

    print(f"Train: {len(train_paths)}, Val: {len(val_paths)}, Test: {len(test_paths)}")

    train_ds = SkinDataset(
        train_paths,
        train_labels,
        transform=get_transforms(IMAGE_SIZE, is_training=True),
        preprocess_config={"clahe": True},
        is_training=True,
    )
    val_ds = SkinDataset(
        val_paths,
        val_labels,
        transform=get_transforms(IMAGE_SIZE, is_training=False),
        is_training=False,
    )

    train_loader = DataLoader(
        train_ds,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
        drop_last=True,
        persistent_workers=NUM_WORKERS > 0,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
    )

    # Class weights for imbalance
    class_weights = compute_class_weights(train_labels, NUM_CLASSES).to(device)
    criterion = DualHeadLoss(class_weights=class_weights, focal_gamma=2.0, binary_weight=0.2)

    # Model
    model = create_model(
        num_classes=NUM_CLASSES,
        backbone=backbone_name,
        pretrained=PRETRAINED,
        embed_dim=EMBED_DIM,
        use_attention=use_attention,
        use_fusion=use_fusion,
    )
    model = model.to(device)

    # Optimizer
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=0.01)

    # ReduceLROnPlateau - reduces LR when val loss plateaus, helps escape local minima
    scheduler = ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=LR_FACTOR,
        patience=5,
        min_lr=MIN_LR,
    )

    scaler = torch.amp.GradScaler("cuda", enabled=USE_AMP)

    # Training loop
    best_f1 = 0
    best_epoch = 0
    start_epoch = 0
    patience_counter = 0

    if args.resume:
        if ckpt_path.exists():
            print(f"Resuming from checkpoint: {ckpt_path}")
            checkpoint = torch.load(ckpt_path, map_location=device)
            model.load_state_dict(checkpoint["model_state_dict"])
            optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
            if "scaler_state_dict" in checkpoint:
                scaler.load_state_dict(checkpoint["scaler_state_dict"])
            start_epoch = checkpoint["epoch"]
            best_f1 = checkpoint["best_f1"]
            best_epoch = start_epoch
            print(f"Resumed at epoch {start_epoch} with best F1: {best_f1:.4f}")
        else:
            print(f"No checkpoint found at {ckpt_path}, starting fresh.")

    # CSV Logging header
    if not args.resume or not log_file.exists():
        with open(log_file, "w") as f:
            f.write("epoch,train_loss,train_acc,train_f1,val_loss,val_acc,val_f1,lr\n")

    for epoch in range(start_epoch, num_epochs):
        start = time.time()
        train_loss, train_acc, train_f1 = train_one_epoch(
            model, train_loader, criterion, optimizer, scaler, device, USE_AMP
        )
        val_loss, val_acc, val_f1 = validate(model, val_loader, criterion, device, USE_AMP)
        scheduler.step(val_f1)  # Reduce LR when val_f1 plateaus
        elapsed = time.time() - start

        lr = optimizer.param_groups[0]["lr"]
        print(
            f"Epoch {epoch+1}/{num_epochs} | "
            f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} F1: {train_f1:.4f} | "
            f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f} F1: {val_f1:.4f} | "
            f"LR: {lr:.2e} | {elapsed:.1f}s"
        )
        
        # Log to CSV
        with open(log_file, "a") as f:
            f.write(f"{epoch+1},{train_loss:.4f},{train_acc:.4f},{train_f1:.4f},{val_loss:.4f},{val_acc:.4f},{val_f1:.4f},{lr:.2e}\n")

        # Save best
        if val_f1 > best_f1:
            best_f1 = val_f1
            best_epoch = epoch + 1
            patience_counter = 0
            torch.save(
                {
                    "epoch": epoch + 1,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "scaler_state_dict": scaler.state_dict(),
                    "best_f1": best_f1,
                    "config": {
                        "num_classes": NUM_CLASSES,
                        "backbone": backbone_name,
                        "embed_dim": EMBED_DIM,
                        "class_names": CLASS_NAMES,
                        "use_attention": use_attention,
                        "use_fusion": use_fusion,
                    },
                },
                ckpt_path,
            )
            print(f"  -> New best model saved (F1: {best_f1:.4f})")
        else:
            patience_counter += 1

        # Early stopping
        if patience_counter >= EARLY_STOPPING_PATIENCE:
            print(f"Early stopping at epoch {epoch+1} (no improvement for {EARLY_STOPPING_PATIENCE} epochs)")
            break

        # Learning rate too low and not improving - could add ReduceLROnPlateau as fallback
        # OneCycleLR handles this, so we rely on early stopping

    print(f"\nTraining complete. Best F1: {best_f1:.4f} at epoch {best_epoch}")

    # Load best and evaluate on test set
    ckpt = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])

    test_ds = SkinDataset(
        test_paths,
        test_labels,
        transform=get_transforms(IMAGE_SIZE, is_training=False),
        is_training=False,
    )
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="Test"):
            images = images.to(device)
            _, class_logits = model(images)
            preds = class_logits.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.numpy())

    # Metrics
    acc = accuracy_score(all_labels, all_preds)
    f1_macro = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    f1_weighted = f1_score(all_labels, all_preds, average="weighted", zero_division=0)
    prec = precision_score(all_labels, all_preds, average="macro", zero_division=0)
    rec = recall_score(all_labels, all_preds, average="macro", zero_division=0)

    print("\n" + "=" * 60)
    print("TEST SET RESULTS")
    print("=" * 60)
    print(f"Accuracy:    {acc:.4f}")
    print(f"F1 (macro): {f1_macro:.4f}")
    print(f"F1 (weighted): {f1_weighted:.4f}")
    print(f"Precision:  {prec:.4f}")
    print(f"Recall:     {rec:.4f}")

    report = classification_report(
        all_labels, all_preds, target_names=CLASS_NAMES, zero_division=0
    )
    print("\nPer-class report:\n", report)

    cm = confusion_matrix(all_labels, all_preds)
    np.save(OUTPUT_DIR / f"confusion_matrix{suffix}.npy", cm)
    print(f"\nConfusion matrix saved to {OUTPUT_DIR / f'confusion_matrix{suffix}.npy'}")

    metrics = {
        "accuracy": float(acc),
        "f1_macro": float(f1_macro),
        "f1_weighted": float(f1_weighted),
        "precision_macro": float(prec),
        "recall_macro": float(rec),
        "best_epoch": best_epoch,
    }
    with open(OUTPUT_DIR / f"test_metrics{suffix}.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("\nDone.")


if __name__ == "__main__":
    main()
