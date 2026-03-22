"""
Plot training results and compare ablation models.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

def main():
    OUTPUT_DIR = Path("outputs")
    PLOT_DIR = OUTPUT_DIR / "comparison_plots"
    PLOT_DIR.mkdir(exist_ok=True, parents=True)

    # Models to compare
    models = {
        "Baseline (B2)": "training_log_b2_baseline.csv",
        "ResNet50": "training_log_resnet50_baseline.csv",
        "Fusion Only": "training_log_b2_fusion.csv",
        "Attention Only": "training_log_b2_attn.csv",
        "Full Model": "training_log_b2_full.csv"
    }

    all_data = []
    summary = []

    for name, filename in models.items():
        path = OUTPUT_DIR / filename
        if not path.exists():
            print(f"Warning: {filename} not found, skipping...")
            continue
            
        df = pd.read_csv(path)
        df["Model"] = name
        all_data.append(df)
        
        # Get best metrics
        best_idx = df["val_f1"].idxmax()
        best_row = df.loc[best_idx]
        
        summary.append({
            "Model": name,
            "Best Val F1": best_row["val_f1"],
            "Best Val Acc": best_row["val_acc"],
            "Epoch": best_row["epoch"]
        })

    if not all_data:
        print("No training logs found in outputs/")
        return

    all_data = pd.concat(all_data)

    # Set style
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({"font.size": 12})

    # Plot 1: Train Loss
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=all_data, x="epoch", y="train_loss", hue="Model", marker="o")
    plt.title("Training Loss Comparison")
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "comparison_train_loss.png", dpi=150)
    print(f"Saved {PLOT_DIR / 'comparison_train_loss.png'}")

    # Plot 2: Val F1
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=all_data, x="epoch", y="val_f1", hue="Model", marker="o")
    plt.title("Validation F1 Comparison")
    plt.ylabel("Macro F1 Score")
    plt.xlabel("Epoch")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "comparison_val_f1.png", dpi=150)
    print(f"Saved {PLOT_DIR / 'comparison_val_f1.png'}")

    # Summary Table
    summary_df = pd.DataFrame(summary).sort_values("Best Val F1", ascending=False)
    print("\n" + "="*40)
    print("MODEL COMPARISON SUMMARY")
    print("="*40)
    
    try:
        print(summary_df.to_markdown(index=False))
    except Exception:
        print(summary_df)
    
    # Save table
    summary_df.to_csv(PLOT_DIR / "comparison_summary.csv", index=False)
    print(f"Saved summary table to {PLOT_DIR / 'comparison_summary.csv'}")

if __name__ == "__main__":
    main()
