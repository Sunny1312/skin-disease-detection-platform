"""
Skin Disease Dataset with preprocessing and augmentation.
Handles class imbalance via oversampling and class weights.
"""

import os
from pathlib import Path
from typing import Optional, Tuple, Callable

import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image
import cv2
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from collections import Counter

# Try importing torchvision transforms
try:
    from torchvision import transforms
    from torchvision.transforms import functional as F
except ImportError:
    transforms = None


def apply_clahe(image: np.ndarray) -> np.ndarray:
    """CLAHE contrast enhancement for skin images."""
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def reduce_hair_artifacts(image: np.ndarray) -> np.ndarray:
    """Morphological operations to reduce hair/noise artifacts."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    morphed = cv2.morphologyEx(morphed, cv2.MORPH_OPEN, kernel)
    # Use inpainting only on small regions - skip for speed
    return image


class SkinDataset(Dataset):
    """PyTorch Dataset for skin disease images."""

    def __init__(
        self,
        image_paths: list,
        labels: list,
        transform: Optional[Callable] = None,
        preprocess_config: dict = None,
        is_training: bool = True,
    ):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.preprocess_config = preprocess_config or {}
        self.use_clahe = self.preprocess_config.get("clahe", False)
        self.is_training = is_training

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        label = self.labels[idx]

        try:
            image = Image.open(path).convert("RGB")
            image = np.array(image)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            image = np.zeros((224, 224, 3), dtype=np.uint8)

        if self.use_clahe and self.is_training and np.random.random() < 0.5:
            try:
                image = apply_clahe(image)
            except Exception:
                pass

        if self.transform:
            if hasattr(self.transform, "transforms"):
                image = Image.fromarray(image)
            image = self.transform(image)

        return image, label


def get_transforms(image_size: int, is_training: bool):
    """Get train/val transforms with augmentation for underrepresented classes."""
    if is_training:
        return transforms.Compose([
            transforms.RandomResizedCrop(image_size, scale=(0.7, 1.0)), # More aggressive cropping
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomAffine(degrees=15, translate=(0.1, 0.1), scale=(0.9, 1.1)), # New affine
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.05), # Stronger jitter
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])
    else:
        return transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])


def discover_classes(dataset_path: Path) -> Tuple[list, dict]:
    """
    Discover class folders and map to indices.
    Returns (class_folders_sorted, folder_to_idx)
    """
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    # Sort by leading number (1., 2., ... 10.)
    def sort_key(p):
        name = p.name
        try:
            num = int(name.split(".")[0])
            return num
        except (ValueError, IndexError):
            return 999

    folders = sorted(folders, key=sort_key)
    folder_to_idx = {f.name: i for i, f in enumerate(folders)}
    return folders, folder_to_idx


def load_dataset_paths(dataset_path: Path) -> Tuple[list, list]:
    """Load all image paths and labels. Returns (paths, labels)."""
    folders, folder_to_idx = discover_classes(dataset_path)
    paths, labels = [], []

    for folder in folders:
        idx = folder_to_idx[folder.name]
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
            for p in folder.glob(ext):
                paths.append(str(p))
                labels.append(idx)

    return paths, labels


def get_group_id(filename: str) -> str:
    """
    Extract grouping ID from filename to prevent data leakage.
    - ISIC_... -> unique ID (assume independent)
    - 0_1.jpg -> Group ID is '0' (all augmentations of 0 stay together)
    """
    if filename.startswith("ISIC_"):
        return filename  # Assume unique
    if "_" in filename:
        return filename.split("_")[0]  # Group by prefix
    return filename

def prepare_splits(
    dataset_path: Path,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> Tuple[list, list, list, list, list, list]:
    """
    Stratified Group Split to prevent data leakage.
    Splits are performed per-class to maintain balance, respecting patient/lesion groups.
    """
    paths, labels = load_dataset_paths(dataset_path)
    
    # Organize by class
    class_data = {}
    for p, l in zip(paths, labels):
        if l not in class_data:
            class_data[l] = []
        class_data[l].append(p)

    train_paths, val_paths, test_paths = [], [], []
    train_labels, val_labels, test_labels = [], [], []

    print("Performing Grouped Split to prevent leakage...")
    
    for label, class_paths in class_data.items():
        # Get groups for this class
        groups = np.array([get_group_id(Path(p).name) for p in class_paths])
        class_paths = np.array(class_paths)
        
        # Split 1: Train vs Rest
        gss = GroupShuffleSplit(n_splits=1, train_size=train_ratio, random_state=seed)
        train_idx, rest_idx = next(gss.split(class_paths, groups=groups))
        
        c_train_paths = class_paths[train_idx]
        c_rest_paths = class_paths[rest_idx]
        c_rest_groups = groups[rest_idx]
        
        # Split 2: Val vs Test (from Rest)
        # Adjust ratio: val_ratio is relative to total, so we need prob for Rest
        # If Train=0.7, Rest=0.3. Val=0.15 is 0.5 of Rest.
        relative_val_size = val_ratio / (val_ratio + test_ratio)
        
        gss_val = GroupShuffleSplit(n_splits=1, test_size=(1 - relative_val_size), random_state=seed)
        val_idx, test_idx = next(gss_val.split(c_rest_paths, groups=c_rest_groups))
        
        c_val_paths = c_rest_paths[val_idx]
        c_test_paths = c_rest_paths[test_idx]
        
        # Extend lists
        train_paths.extend(c_train_paths)
        val_paths.extend(c_val_paths)
        test_paths.extend(c_test_paths)
        
        train_labels.extend([label] * len(c_train_paths))
        val_labels.extend([label] * len(c_val_paths))
        test_labels.extend([label] * len(c_test_paths))

    print(f"Split complete. Train: {len(train_paths)}, Val: {len(val_paths)}, Test: {len(test_paths)}")
    return train_paths, train_labels, val_paths, val_labels, test_paths, test_labels


def compute_class_weights(labels: list, num_classes: int) -> torch.Tensor:
    """Compute inverse frequency weights for imbalanced classes."""
    counts = Counter(labels)
    weights = []
    total = len(labels)
    for c in range(num_classes):
        n = counts.get(c, 1)
        # Inverse frequency, smooth to avoid extreme values
        w = total / (num_classes * n + 1e-6)
        weights.append(w)
    weights = torch.tensor(weights, dtype=torch.float32)
    return weights / weights.sum() * num_classes


def get_oversampled_indices(paths: list, labels: list, max_per_class: Optional[int] = None) -> list:
    """
    Oversample minority classes for training.
    Returns indices for oversampled dataset.
    """
    labels = np.array(labels)
    indices = np.arange(len(labels))
    counts = Counter(labels)
    max_count = max(counts.values())
    if max_per_class is not None:
        max_count = min(max_count, max_per_class)

    resampled_indices = []
    for c in sorted(counts.keys()):
        class_indices = indices[labels == c]
        n = len(class_indices)
        if n < max_count:
            # Oversample
            extra = np.random.choice(class_indices, size=max_count - n, replace=True)
            resampled_indices.extend(class_indices.tolist())
            resampled_indices.extend(extra.tolist())
        else:
            # Undersample if needed
            if max_per_class and n > max_per_class:
                chosen = np.random.choice(class_indices, size=max_per_class, replace=False)
                resampled_indices.extend(chosen.tolist())
            else:
                resampled_indices.extend(class_indices.tolist())

    np.random.shuffle(resampled_indices)
    return resampled_indices
