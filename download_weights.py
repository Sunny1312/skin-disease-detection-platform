import timm
import os

def download_model():
    print("Attempting to download EfficientNet-B2 weights...")
    try:
        # This triggers the download and caches it
        model = timm.create_model('efficientnet_b2', pretrained=True)
        print("SUCCESS: Model weights downloaded and cached!")
        print("You can now run 'py train.py' again.")
    except Exception as e:
        print(f"ERROR: Download failed. Details: {e}")

if __name__ == "__main__":
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"
    download_model()