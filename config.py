"""
Configuration for Skin Disease Detection System.
Optimized for: Intel i5-13450HX, 24GB RAM, NVIDIA GPU
"""

import os
from pathlib import Path

# Paths - adjust DATASET_PATH if needed
BASE_DIR = Path(__file__).resolve().parent
DESKTOP = Path(r"C:\Users\Surya Sunanda\Desktop")
DATASET_PATH = DESKTOP / "Skin_Dataset" / "IMG_CLASSES"
OUTPUT_DIR = BASE_DIR / "outputs"
CHECKPOINT_DIR = BASE_DIR / "checkpoints"

# Create directories
OUTPUT_DIR.mkdir(exist_ok=True)
CHECKPOINT_DIR.mkdir(exist_ok=True)

# Training - optimized for speed and learning
IMAGE_SIZE = 260  # Native for B2
BATCH_SIZE = 24   # RTX 4050 6GB: reduced for B2 + larger img
NUM_WORKERS = 2   # Data loading; 4=fastest, 0 if Windows multiprocessing errors
NUM_EPOCHS = 50
EARLY_STOPPING_PATIENCE = 10  # Increased patience for harder task

# Learning - ensures model keeps improving
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 0.01
LR_PATIENCE = 4
LR_FACTOR = 0.5
MIN_LR = 1e-6

# Mixed precision for 2x speed on GPU
USE_AMP = True
GRADIENT_CLIP = 1.0

# Model
BACKBONE = "efficientnet_b2"
PRETRAINED = True
NUM_CLASSES = 10
EMBED_DIM = 256

# Data split
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15
RANDOM_SEED = 42

# Class names (order must match folder indexing)
CLASS_NAMES = [
    "Eczema",
    "Melanoma",
    "Atopic Dermatitis",
    "Basal Cell Carcinoma",
    "Melanocytic Nevi",
    "Benign Keratosis-like Lesions",
    "Psoriasis",
    "Seborrheic Keratosis",
    "Tinea Ringworm Candidiasis",
    "Warts Molluscum Viral Infections",
]

# Reproducibility
def set_seed(seed):
    import torch
    import random
    import numpy as np
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
