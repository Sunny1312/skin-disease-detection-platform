"""
Generate Grad-CAM visualizations for sample images.
Run after training to create explainability outputs.
"""

import sys
from pathlib import Path

import torch
import numpy as np
from PIL import Image
from torchvision import transforms

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import CHECKPOINT_DIR, OUTPUT_DIR, IMAGE_SIZE, CLASS_NAMES
from explainability.gradcam import GradCAM, overlay_heatmap, create_gradcam


def preprocess_image(image_path: Path, image_size: int = 224) -> tuple:
    """Load and preprocess image. Returns (tensor, numpy RGB for overlay)."""
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img_t = transform(Image.fromarray(img_np)).unsqueeze(0)
    # Resize numpy for overlay
    from PIL import Image as PILImage
    img_resized = np.array(PILImage.fromarray(img_np).resize((image_size, image_size)))
    return img_t, img_resized


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt_path = CHECKPOINT_DIR / "best_model.pt"
    if not ckpt_path.exists():
        print("Train the model first (train.py)")
        return

    gradcam, model = create_gradcam(ckpt_path, device)
    model.eval()

    # Create output dir
    gradcam_dir = OUTPUT_DIR / "gradcam"
    gradcam_dir.mkdir(exist_ok=True)

    # Get a few test images - use first image from each class if available
    from data.dataset import prepare_splits, load_dataset_paths
    from config import DATASET_PATH

    paths, labels = load_dataset_paths(DATASET_PATH)
    # Pick 2 images per class
    by_class = {}
    for p, l in zip(paths, labels):
        if l not in by_class:
            by_class[l] = []
        if len(by_class[l]) < 2:
            by_class[l].append(p)

    count = 0
    for cls_idx, img_paths in sorted(by_class.items()):
        for img_path in img_paths[:2]:
            img_path = Path(img_path)
            if not img_path.exists():
                continue
            try:
                img_t, img_np = preprocess_image(img_path, IMAGE_SIZE)
                img_t = img_t.to(device)

                with torch.enable_grad():
                    cam = gradcam.generate(img_t, target_class=cls_idx)

                overlay = overlay_heatmap(cam, img_np, alpha=0.5)
                out_path = gradcam_dir / f"gradcam_{CLASS_NAMES[cls_idx].replace(' ', '_')}_{count}.jpg"
                Image.fromarray(overlay).save(out_path)
                count += 1
                if count >= 20:
                    break
            except Exception as e:
                print(f"Skip {img_path}: {e}")
        if count >= 20:
            break

    print(f"Saved {count} Grad-CAM visualizations to {gradcam_dir}")


if __name__ == "__main__":
    main()
