import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io

IMG_SIZE = (224, 224)

# Load model once at startup
_model = None
_class_indices = None
_disease_info = None


def load_model():
    global _model, _class_indices, _disease_info

    print("⏳ Loading model...")
    _model = tf.keras.models.load_model("saved_model/plant_model.h5")
    print("✅ Model loaded!")

    with open("saved_model/class_indices.json") as f:
        _class_indices = json.load(f)  # {0: "Apple___Apple_scab", ...}

    with open("classes.json") as f:
        _disease_info = json.load(f)  # disease details


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Convert raw image bytes to model-ready numpy array."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)  # shape: (1, 224, 224, 3)


def predict(image_bytes: bytes) -> dict:
    """Run inference and return structured result."""
    if _model is None:
        load_model()

    arr = preprocess_image(image_bytes)
    preds = _model.predict(arr, verbose=0)[0]  # shape: (38,)

    top_idx = int(np.argmax(preds))
    confidence = float(preds[top_idx]) * 100

    class_label = _class_indices.get(str(top_idx), "Unknown")
    info = _disease_info.get(str(top_idx), {})

    disease_name = info.get("name", class_label)
    is_healthy = "healthy" in disease_name.lower()

    # Top 3 predictions
    top3_indices = np.argsort(preds)[-3:][::-1]
    top3 = [
        {
            "label": _disease_info.get(str(i), {}).get("name", _class_indices.get(str(i), "")),
            "confidence": round(float(preds[i]) * 100, 1),
        }
        for i in top3_indices
    ]

    return {
        "disease_name": disease_name,
        "is_healthy": is_healthy,
        "confidence": round(confidence, 1),
        "medicines": info.get("medicine", []),
        "prevention_tips": info.get("prevention", []),
        "top_predictions": top3,
    }