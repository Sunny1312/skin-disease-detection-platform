"""
FastAPI backend for Skin Disease Detection.
Local inference - no cloud or paid APIs.
"""

import io
import base64
import sys
from pathlib import Path

import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
from torchvision import transforms

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    CHECKPOINT_DIR,
    IMAGE_SIZE,
    CLASS_NAMES,
    NUM_CLASSES,
    BACKBONE,
    EMBED_DIM,
)
from models.hybrid_model import create_model
from backend.recommendations import get_recommendation

# Grad-CAM (lazy load)
_gradcam = None
_model = None


def load_model():
    global _model
    if _model is not None:
        return _model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt_path = CHECKPOINT_DIR / "best_model.pt"
    if not ckpt_path.exists():
        raise FileNotFoundError("Model not found. Train first with train.py")
    ckpt = torch.load(ckpt_path, map_location=device)
    config = ckpt.get("config", {})
    model = create_model(
        num_classes=config.get("num_classes", NUM_CLASSES),
        backbone=config.get("backbone", BACKBONE),
        pretrained=False,
        embed_dim=config.get("embed_dim", EMBED_DIM),
    )
    model.load_state_dict(ckpt["model_state_dict"])
    model = model.to(device)
    model.eval()
    _model = (model, device)
    return _model


def get_gradcam():
    global _gradcam
    if _gradcam is not None:
        return _gradcam
    from explainability.gradcam import GradCAM
    model, device = load_model()
    target = None
    for name, module in model.backbone.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            target = module
    if target is None and hasattr(model.backbone, "blocks"):
        target = model.backbone.blocks[-1]
    if target is None:
        target = list(model.backbone.children())[-1]
    _gradcam = (GradCAM(model, target), device)
    return _gradcam


def preprocess_image(image_bytes: bytes) -> torch.Tensor:
    """Load and preprocess image for model."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(img).unsqueeze(0)


def image_to_base64(arr: np.ndarray) -> str:
    """Convert numpy RGB image to base64 JPEG string."""
    from PIL import Image as PILImage
    img = PILImage.fromarray(arr.astype(np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


app = FastAPI(title="Skin Disease Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict skin disease from uploaded image."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(400, f"Failed to read file: {e}")

    model, device = load_model()
    img_t = preprocess_image(contents).to(device)

    with torch.no_grad():
        binary_logits, class_logits = model(img_t)
        probs = torch.softmax(class_logits, dim=1)[0].cpu().numpy()
        pred_idx = int(class_logits.argmax(dim=1).item())
        confidence = float(probs[pred_idx])

    # OOD / Irrelevant Detection Threshold
    THRESHOLD = 0.65
    if confidence < THRESHOLD:
        disease_name = "Irrelevant/Unknown"
    else:
        disease_name = CLASS_NAMES[pred_idx]

    rec = get_recommendation(disease_name)

    # Grad-CAM
    gradcam_img_b64 = None
    try:
        from explainability.gradcam import overlay_heatmap
        gradcam, dev = get_gradcam()
        with torch.enable_grad():
            img_t_grad = preprocess_image(contents).to(dev).requires_grad_(True)
            cam = gradcam.generate(img_t_grad, target_class=pred_idx)
        img_np = np.array(Image.open(io.BytesIO(contents)).convert("RGB").resize((IMAGE_SIZE, IMAGE_SIZE)))
        overlay = overlay_heatmap(cam, img_np, alpha=0.5)
        gradcam_img_b64 = image_to_base64(overlay)
    except Exception as e:
        print(f"Grad-CAM failed: {e}")

    return {
        "disease": disease_name,
        "confidence": confidence,
        "severity": rec["severity"],
        "recommendations": rec,
        "all_probabilities": {CLASS_NAMES[i]: float(probs[i]) for i in range(len(CLASS_NAMES))},
        "gradcam_image": gradcam_img_b64,
    }


@app.get("/classes")
def get_classes():
    return {"classes": CLASS_NAMES}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
