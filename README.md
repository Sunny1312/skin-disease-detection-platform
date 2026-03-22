# Skin Disease Detection System

End-to-end skin disease classification using deep learning, with explainability and care recommendations.

## Features

- **Hybrid architecture**: EfficientNet backbone + attention + multi-scale fusion
- **Dual output**: Binary (diseased vs normal) + 10-class disease classification
- **Handles imbalance**: Focal Loss, class weights, oversampling
- **Explainability**: Grad-CAM heatmaps
- **Local deployment**: FastAPI backend + React frontend, no cloud APIs
- **Research-ready**: Metrics, ROC curves, confusion matrices

## Requirements

- Python 3.10+
- CUDA-capable NVIDIA GPU (recommended)
- 24 GB RAM
- ~10 GB disk for dataset + models

## Setup

```bash
# Install Python dependencies (use py on Windows if python not in PATH)
py -m pip install -r requirements.txt

# For GPU: install CUDA-enabled PyTorch from https://pytorch.org
# Example: py -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# (Optional) Install Node.js and frontend dependencies
cd frontend && npm install
```

## Dataset

Place the Kaggle "Skin Diseases Image Dataset" in:

```
C:\Users\Surya Sunanda\Desktop\Skin_Dataset\IMG_CLASSES\
```

Folder structure: one subfolder per class (e.g., `1. Eczema 1677`, `2. Melanoma 15.75k`, ...).

## Usage

### 1. Train the model

```bash
python train.py
```

Training uses:
- OneCycleLR for fast convergence
- Mixed precision (AMP) for speed
- Early stopping (patience=7)
- Oversampling for minority classes

**Speed tips**: Reduce `IMAGE_SIZE` to 192 or `BATCH_SIZE` to 16 if GPU memory is limited. Set `NUM_WORKERS=0` on Windows if you get multiprocessing errors.

### 2. Evaluate

```bash
python evaluate.py
```

Generates `outputs/confusion_matrix.png`, `roc_curves.png`, `per_class_metrics.png`, and `evaluation_report.json`.

### 3. Run backend API

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Or double-click `run_backend.bat`.

### 4. Run frontend

```bash
cd frontend && npm run dev
```

Open http://localhost:5173, upload a skin image, and view predictions with Grad-CAM and recommendations.

## Project Structure

```
Skin_Disease_Detection/
├── config.py           # Configuration
├── train.py            # Training script
├── evaluate.py         # Evaluation and plots
├── data/               # Dataset and transforms
├── models/             # Hybrid model, losses
├── explainability/     # Grad-CAM
├── backend/            # FastAPI service
├── frontend/           # React + Tailwind UI
├── research/           # Experimental notes
└── outputs/            # Metrics, plots
```

## Configuration (config.py)

| Parameter | Default | Description |
|-----------|---------|-------------|
| IMAGE_SIZE | 224 | Input size (smaller = faster) |
| BATCH_SIZE | 32 | Reduce if OOM |
| NUM_WORKERS | 4 | 0 on Windows if spawn errors |
| NUM_EPOCHS | 50 | Max epochs |
| EARLY_STOPPING_PATIENCE | 7 | Stop if no improvement |

## Medical Disclaimer

This system is for educational and research purposes only. It is not a substitute for professional medical advice. Always consult a dermatologist for medical concerns.

## License

MIT
