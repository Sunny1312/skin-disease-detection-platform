"""
Grad-CAM implementation for skin disease model explainability.
Visualizes which regions influenced the model's prediction.
"""

import torch
import torch.nn.functional as F
import numpy as np
import cv2
from pathlib import Path
from typing import Optional, Tuple

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.hybrid_model import HybridSkinModel, create_model


def overlay_heatmap(cam: np.ndarray, image: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Overlay heatmap on RGB image."""
    cam = np.uint8(255 * cam)
    heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    if image.shape[:2] != heatmap.shape[:2]:
        heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
        
    overlay = (alpha * heatmap + (1 - alpha) * image).astype(np.uint8)
    return overlay


class GradCAM:
    """Grad-CAM for hybrid skin model."""

    def __init__(self, model: HybridSkinModel, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def _register_hooks(self):
        self.target_layer.register_forward_hook(self._save_activation)
        self.target_layer.register_full_backward_hook(self._save_gradient)

    def generate(self, input_tensor: torch.Tensor, target_class: Optional[int] = None) -> np.ndarray:
        """
        Generate Grad-CAM heatmap.
        input_tensor: (1, 3, H, W)
        target_class: class index for gradient (default: predicted class)
        """
        self.model.eval()
        input_tensor = input_tensor.requires_grad_(True)

        # Forward pass
        _, class_logits = self.model(input_tensor)
        
        if target_class is None:
            target_class = class_logits.argmax(dim=1).item()

        # Backward pass
        self.model.zero_grad()
        class_logits[0, target_class].backward()

        gradients = self.gradients
        activations = self.activations
        
        if gradients is None or activations is None:
            print("Warning: Gradients or activations are None. Check target layer.")
            return np.zeros((input_tensor.shape[2], input_tensor.shape[3]))

        # Global average pooling of gradients (weights)
        weights = torch.mean(gradients, dim=(2, 3))
        
        # Weighted combination of activation maps
        cam = torch.sum(weights[:, :, None, None] * activations, dim=1, keepdim=True)
        cam = F.relu(cam)
        
        # Normalize
        cam = cam - cam.min()
        if cam.max() > 0:
            cam = cam / cam.max()
            
        # Resize to input resolution
        cam = F.interpolate(
            cam,
            size=(input_tensor.shape[2], input_tensor.shape[3]),
            mode="bilinear",
            align_corners=False,
        )
        return cam[0, 0].cpu().numpy()


def get_target_layer(model: HybridSkinModel):
    """Get the last convolutional layer of EfficientNet backbone for Grad-CAM."""
    # Try to find the last block of the backbone
    backbone = model.backbone
    
    # Check for timm FeatureListNet structure (has 'blocks' attribute)
    if hasattr(backbone, "blocks"):
        # EfficientNet usually has blocks as a Sequential
        return backbone.blocks[-1]
    
    # Fallback: Iterate children and find last Conv2d or container
    # This is tricky for features_only models which might be graph-based
    # But for standard timm models, they are usually nn.Modules
    
    layers = list(backbone.children())
    if len(layers) > 0:
        return layers[-1]
        
    return None


def create_gradcam(
    model_path: Path,
    device: torch.device,
    num_classes: int = 10,
    backbone: str = "efficientnet_b0",
    embed_dim: int = 256,
) -> Tuple[GradCAM, HybridSkinModel]:
    """Load model and create GradCAM object."""
    ckpt = torch.load(model_path, map_location=device)
    config = ckpt.get("config", {})
    
    model = create_model(
        num_classes=config.get("num_classes", num_classes),
        backbone=config.get("backbone", backbone),
        pretrained=False,
        embed_dim=config.get("embed_dim", embed_dim),
        use_attention=config.get("use_attention", True),
        use_fusion=config.get("use_fusion", True),
    )
    model.load_state_dict(ckpt["model_state_dict"])
    model = model.to(device)
    model.eval()

    target = get_target_layer(model)
    if target is None:
        raise ValueError("Could not find target layer for Grad-CAM.")

    gradcam = GradCAM(model, target)
    return gradcam, model
