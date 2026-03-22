"""
Hybrid Skin Disease Classification Model.
- EfficientNet backbone for feature extraction
- Channel + Spatial Attention (CBAM-like)
- Multi-scale feature fusion (FPN-style)
- Dual output: binary (normal vs diseased) + 10-class disease classification
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple

try:
    import timm
except ImportError:
    timm = None


class ChannelAttention(nn.Module):
    """Squeeze-and-Excitation style channel attention."""

    def __init__(self, in_channels: int, reduction: int = 16):
        super().__init__()
        reduction = max(1, min(reduction, in_channels))
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, in_channels // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // reduction, in_channels, bias=False),
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, c, _, _ = x.size()
        avg_out = self.fc(self.avg_pool(x).view(b, c))
        max_out = self.fc(self.max_pool(x).view(b, c))
        return self.sigmoid(avg_out + max_out).view(b, c, 1, 1)


class SpatialAttention(nn.Module):
    """Spatial attention to focus on clinically relevant regions."""

    def __init__(self, kernel_size: int = 7):
        super().__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=kernel_size // 2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        out = torch.cat([avg_out, max_out], dim=1)
        return self.sigmoid(self.conv(out))


class AttentionBlock(nn.Module):
    """Channel + Spatial attention block."""

    def __init__(self, in_channels: int, reduction: int = 16):
        super().__init__()
        self.ca = ChannelAttention(in_channels, reduction)
        self.sa = SpatialAttention(7)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x * self.ca(x)
        x = x * self.sa(x)
        return x


class HybridSkinModel(nn.Module):
    """
    Hybrid model with:
    - Pretrained EfficientNet backbone
    - Multi-scale feature extraction (low + mid + high)
    - Attention on fused features
    - Dual head: binary + multi-class
    """

    def __init__(
        self,
        num_classes: int = 10,
        backbone: str = "efficientnet_b0",
        pretrained: bool = True,
        embed_dim: int = 256,
        dropout: float = 0.3,
        use_attention: bool = True,
        use_fusion: bool = True,
    ):
        super().__init__()
        self.num_classes = num_classes
        self.use_attention = use_attention
        self.use_fusion = use_fusion

        if timm is None:
            raise ImportError("timm is required. Install: pip install timm")

        # Backbone - EfficientNet provides multi-scale features
        self.backbone = timm.create_model(
            backbone,
            pretrained=pretrained,
            features_only=True,
            out_indices=(1, 2, 3, 4),  # 4 scales
        )

        # Get channel dimensions from backbone
        with torch.no_grad():
            dummy = torch.randn(1, 3, 224, 224)
            features = self.backbone(dummy)
        channels = [f.shape[1] for f in features]

        # Multi-scale fusion setup
        self.lateral_convs = nn.ModuleList()
        if self.use_fusion:
            # Fusing all scales
            for c in channels:
                self.lateral_convs.append(
                    nn.Sequential(
                        nn.Conv2d(c, 64, 1),
                        nn.BatchNorm2d(64),
                        nn.ReLU(inplace=True),
                    )
                )
            fused_channels = 64 * len(channels)
        else:
            # No fusion - use only the last (deepest) feature map
            # We still project it to 64 channels to match the 'lateral' style or just project to embed_dim?
            # To be fair, let's project the last feature to a consistent size
            # Or better: Project last feature to 'embed_dim' directly in the head if no attention?
            # But if we want "Attention only" (No Fusion), we need an intermediate tensor.
            # Let's project the last feature to 256 channels (arbitrary, but consistent)
            self.last_conv = nn.Sequential(
                nn.Conv2d(channels[-1], 256, 1),
                nn.BatchNorm2d(256),
                nn.ReLU(inplace=True)
            )
            fused_channels = 256

        # Attention Mechanism
        if self.use_attention:
            self.attention = AttentionBlock(fused_channels, reduction=16)
        else:
            self.attention = nn.Identity()

        # Final projection before classification
        self.fusion_conv = nn.Sequential(
            nn.Conv2d(fused_channels, embed_dim, 3, padding=1),
            nn.BatchNorm2d(embed_dim),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d(1),
        )

        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(embed_dim, embed_dim)
        self.relu = nn.ReLU(inplace=True)

        # Dual heads
        self.binary_head = nn.Linear(embed_dim, 1)
        self.class_head = nn.Linear(embed_dim, num_classes)

    def forward(
        self, x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        features = self.backbone(x)

        if self.use_fusion:
            # Upsample all to same spatial size and fuse
            target_size = features[-1].shape[2:]
            fused_list = []
            for i, feat in enumerate(features):
                if feat.shape[2:] != target_size:
                    feat = F.interpolate(feat, size=target_size, mode="bilinear", align_corners=False)
                fused_list.append(self.lateral_convs[i](feat))
            x_feat = torch.cat(fused_list, dim=1)
        else:
            # Use only the last feature map
            x_feat = self.last_conv(features[-1])

        # Attention
        if self.use_attention:
            x_feat = self.attention(x_feat)

        out = self.fusion_conv(x_feat).flatten(1)
        out = self.dropout(out)
        out = self.relu(self.fc(out))
        out = self.dropout(out)

        binary_logits = self.binary_head(out)
        class_logits = self.class_head(out)

        return binary_logits, class_logits


def create_model(
    num_classes: int = 10,
    backbone: str = "efficientnet_b0",
    pretrained: bool = True,
    embed_dim: int = 256,
    use_attention: bool = True,
    use_fusion: bool = True,
) -> HybridSkinModel:
    """Factory to create model."""
    return HybridSkinModel(
        num_classes=num_classes,
        backbone=backbone,
        pretrained=pretrained,
        embed_dim=embed_dim,
        use_attention=use_attention,
        use_fusion=use_fusion,
    )
