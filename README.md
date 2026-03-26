# Skin Diagnostics and Classification Platform 🔬🩺

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent, end-to-end dermatological screening and classification platform. This project implements a novel **HybridSkinModel** that integrates deep learning feature extraction with attention mechanisms and multi-scale fusion to accurately identify 10 different types of skin diseases.

---

## 📖 Abstract

Skin diseases comprise a significant percentage of the world's population, making early and accurate diagnosis necessary to avoid complications and secure better outcomes. Due to the high visual similarity among different skin conditions and limited access to dermatological expertise, manual diagnosis can be challenging. 

This repository presents an automated, AI-driven approach for skin disease diagnosis using the **HybridSkinModel**. By combining an EfficientNet backbone with Spatial/Channel Attention (CBAM) and Multi-scale Feature Fusion, the model effectively learns specific visual patterns, enhances regions of interest, and suppresses background noise—enabling robust multi-class dermatological image analysis.

## 📊 Dataset

This project utilizes the **Skin Diseases Image Dataset** available on Kaggle. It contains diverse dermatological images spanning multiple classes with varying textures, colors, and background conditions.

🔗 **Dataset Link:** [Skin Diseases Image Dataset by ismailpromus](https://www.kaggle.com/datasets/ismailpromus/skin-diseases-image-dataset)

**Supported Disease Categories (10 Classes):**
- Eczema
- Melanoma
- Atopic Dermatitis
- Basal Cell Carcinoma
- Melanocytic Nevi
- Benign Keratosis-like Lesions
- Psoriasis
- Seborrheic Keratosis
- Tinea Ringworm Candidiasis
- Warts Molluscum Viral Infections

## 🧠 Model Architecture (HybridSkinModel)

The diagnostic pipeline (`Input → Processing → Output`) integrates three core strategies:
1. **Backbone Feature Extraction:** Uses EfficientNet-B2 to extract hierarchical representations.
2. **Attention Mechanisms:** Incorporates Squeeze-and-Excitation (SE) and Convolutional Block Attention Modules (CBAM) to focus on lesion-specific areas while filtering out irrelevant background noise.
3. **Multi-scale Fusion:** Merges features from different spatial resolutions, capturing both fine-grained lesion textures and global structural patterns.

### Experimental Results
Extensive ablation studies validate the hybrid approach. The final test performance metrics:
- **Accuracy:** `88.60%`
- **Macro F1-Score:** `83.74%`
- **Weighted F1-Score:** `88.63%`

Explainability is provided via **Grad-CAM**, generating visual heatmaps that highlight the regions of the image most critical to the model's prediction.

---

## ⚙️ Tech Stack

- **Deep Learning / AI:** PyTorch, Torchvision, Timm
- **Computer Vision:** OpenCV, PIL, Grad-CAM
- **Backend API:** FastAPI, Uvicorn
- **Frontend UI:** React, Vite, Tailwind CSS
- **Data Analysis:** Pandas, NumPy, Matplotlib, Seaborn

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.10+
- Node.js (for frontend)
- CUDA-capable NVIDIA GPU (highly recommended for training)

### 2. Clone the Repository
```bash
git clone https://github.com/Sunny1312/skin-disease-detection-platform.git
cd skin-disease-detection-platform
```

### 3. Backend & AI Setup
Install the required Python dependencies:
```bash
# On Windows, use 'py' if 'python' is not in PATH
python -m pip install -r requirements.txt
```
*(Optional but recommended): Install CUDA-enabled PyTorch for GPU acceleration from [pytorch.org](https://pytorch.org).*

### 4. Dataset Configuration
Download the dataset from the Kaggle link above. Update the `DATASET_PATH` in `config.py` to point to the extracted `IMG_CLASSES` folder on your local machine.

### 5. Frontend Setup
Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
```

---

## 💻 Usage

### Training the Model
To train the model from scratch using mixed precision and early stopping:
```bash
python train.py
```
*(If you encounter OOM errors, reduce `IMAGE_SIZE` or `BATCH_SIZE` in `config.py`)*

### Evaluating the Model
Evaluate the trained model and generate metrics (ROC curves, Confusion Matrices, Grad-CAM samples):
```bash
python evaluate.py
```
Outputs are saved in the `outputs/` directory.

### Running the Full Application
Start the backend API server:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
# Alternatively, run: run_backend.bat
```

Start the React frontend:
```bash
cd frontend
npm run dev
```
Navigate to `http://localhost:5173` in your browser. Upload a skin image to receive a prediction, visual Grad-CAM analysis, and care recommendations.

---

## 📂 Project Structure

```text
skin-disease-detection-platform/
├── backend/            # FastAPI service & prediction routing
├── config.py           # Centralized configuration and hyperparameters
├── data/               # Dataset loading, augmentation, and preprocessing
├── evaluate.py         # Evaluation scripts, metric generation, and plotting
├── explainability/     # Grad-CAM heatmap generation
├── frontend/           # React + Tailwind CSS User Interface
├── models/             # HybridSkinModel architecture and loss functions
├── outputs/            # Generated metrics, plots, and visual samples
├── research/           # Experimental notes and ablation studies
├── requirements.txt    # Python dependencies
└── train.py            # Main training loop
```

---

## 👥 Authors

- **Surya Sunanda Meesala**
- **N. Mohitha Reddy**
- **Thokala Pavani** 

---

## ⚠️ Medical Disclaimer
This system is an experimental prototype intended for educational and research purposes only. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified dermatologist or healthcare provider for any medical concerns.

## 📄 License
This project is licensed under the MIT License.
