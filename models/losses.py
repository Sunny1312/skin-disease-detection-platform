"""
Loss functions for imbalanced skin disease classification.
Focal Loss reduces emphasis on easy examples, focusing on hard ones.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """
    Focal Loss for imbalanced classification.
    FL(p) = -alpha * (1-p)^gamma * log(p)
    """

    def __init__(
        self,
        alpha: torch.Tensor = None,
        gamma: float = 2.0,
        reduction: str = "mean",
        label_smoothing: float = 0.1,
    ):
        super().__init__()
        self.alpha = alpha  # (num_classes,)
        self.gamma = gamma
        self.reduction = reduction
        self.label_smoothing = label_smoothing

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        inputs: (B, C) logits
        targets: (B,) class indices
        """
        ce_loss = F.cross_entropy(
            inputs,
            targets,
            reduction="none",
            label_smoothing=self.label_smoothing,
        )
        pt = torch.exp(-ce_loss)
        focal_weight = (1 - pt) ** self.gamma
        loss = focal_weight * ce_loss

        if self.alpha is not None:
            alpha_t = self.alpha[targets].to(inputs.device)
            loss = alpha_t * loss

        if self.reduction == "mean":
            return loss.mean()
        elif self.reduction == "sum":
            return loss.sum()
        return loss


class DualHeadLoss(nn.Module):
    """
    Combined loss for binary + multi-class heads.
    In this dataset all samples are diseased, so binary target is always 1.
    """

    def __init__(
        self,
        class_weights: torch.Tensor = None,
        focal_gamma: float = 2.0,
        binary_weight: float = 0.2,
        label_smoothing: float = 0.1,
    ):
        super().__init__()
        self.focal = FocalLoss(
            alpha=class_weights,
            gamma=focal_gamma,
            label_smoothing=label_smoothing,
        )
        self.binary_weight = binary_weight
        self.bce = nn.BCEWithLogitsLoss()

    def forward(
        self,
        binary_logits: torch.Tensor,
        class_logits: torch.Tensor,
        targets: torch.Tensor,
    ) -> torch.Tensor:
        """
        binary_logits: (B, 1)
        class_logits: (B, C)
        targets: (B,) class indices
        """
        # All images are diseased - binary target = 1
        binary_targets = torch.ones_like(binary_logits, device=targets.device)
        bce_loss = self.bce(binary_logits, binary_targets)

        focal_loss = self.focal(class_logits, targets)

        return focal_loss + self.binary_weight * bce_loss
