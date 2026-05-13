"""Run this script on Render to download model from Google Drive."""
import gdown
import os

os.makedirs("saved_model", exist_ok=True)

# Replace with your actual Google Drive file IDs
MODEL_ID = "YOUR_MODEL_FILE_ID"
CLASS_ID = "YOUR_CLASS_INDICES_FILE_ID"

print("Downloading model...")
gdown.download(f"https://drive.google.com/uc?id={MODEL_ID}", "saved_model/plant_model.h5")

print("Downloading class indices...")
gdown.download(f"https://drive.google.com/uc?id={CLASS_ID}", "saved_model/class_indices.json")

print("Done!")