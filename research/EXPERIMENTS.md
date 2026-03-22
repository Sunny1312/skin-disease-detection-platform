# Skin Disease Classification - Experimental Framework

## Baseline vs Proposed Model

### Baseline (Simple CNN)
- Architecture: 4-layer CNN (Conv-BN-ReLU-MaxPool x4, FC)
- No transfer learning, no attention, no multi-scale fusion
- Single output head
- Training: Adam, cross-entropy, no class weighting

### Proposed (Hybrid Model)
- Backbone: EfficientNet-B0 (pretrained ImageNet)
- Attention: Channel + Spatial (CBAM-style)
- Multi-scale feature fusion from 4 backbone stages
- Dual head: binary (diseased vs normal) + 10-class
- Training: AdamW, Focal Loss, class weights, OneCycleLR

## Ablation Study

| Experiment | Attention | Multi-scale | Focal Loss | Class Weights | Augmentation |
|------------|-----------|-------------|------------|---------------|--------------|
| 1. Full model | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2. No attention | ✗ | ✓ | ✓ | ✓ | ✓ |
| 3. No multi-scale | ✓ | ✗ | ✓ | ✓ | ✓ |
| 4. CE instead of Focal | ✓ | ✓ | ✗ | ✓ | ✓ |
| 5. No class weights | ✓ | ✓ | ✓ | ✗ | ✓ |
| 6. Minimal augmentation | ✓ | ✓ | ✓ | ✓ | ✗ |

## Expected Results

- **Accuracy**: >85% on test set (target)
- **Macro F1**: Balanced performance across classes
- **ROC-AUC**: >0.95 macro average
- **Explainability**: Grad-CAM highlights clinically relevant regions

## Limitations

1. **Dataset**: All images are diseased - no "normal" skin for binary head validation
2. **Class imbalance**: Melanocytic Nevi (7970) vs Atopic Dermatitis (1257)
3. **Domain**: Single dataset - may not generalize to different imaging conditions
4. **Clinical use**: Requires validation on independent clinical datasets

## Future Improvements

- Add normal skin images for binary head
- Test-time augmentation (TTA)
- Ensemble of multiple backbones
- External validation dataset
- Uncertainty quantification
