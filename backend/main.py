from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os

# Import your model functions from model.py
from model import load_model, predict

# Create FastAPI application
app = FastAPI(
    title="Plant Disease Detection API",
    description="Upload a plant image to detect diseases",
    version="1.0.0",
)

# ------------------------------------------------------------------------------
# CORS Configuration
# ------------------------------------------------------------------------------
# Allow React frontend running on localhost ports 3000 and 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Startup Event - Load Model
# ------------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """
    Load the trained TensorFlow model when the server starts.
    The model file should be located at:
        saved_model/plant_model.h5
    """
    try:
        load_model()
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        raise e


# ------------------------------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Plant Disease Detection API is running 🌿"
    }


# ------------------------------------------------------------------------------
# Health Check Endpoint
# ------------------------------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ------------------------------------------------------------------------------
# Prediction Endpoint
# ------------------------------------------------------------------------------
@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """
    Upload a leaf image and get disease prediction.
    Supported formats: JPG, JPEG, PNG, WEBP
    Maximum file size: 10 MB
    """

    # Allowed MIME types
    allowed_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp",
    ]

    # Validate file type
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid file type: {file.content_type}. "
                "Only JPG, JPEG, PNG, and WEBP are allowed."
            ),
        )

    # Read uploaded file
    contents = await file.read()

    # Validate file size (10 MB max)
    max_size = 10 * 1024 * 1024  # 10 MB
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum allowed size is 10 MB.",
        )

    # Ensure file is not empty
    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # Perform prediction
    try:
        result = predict(contents)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )


# ------------------------------------------------------------------------------
# Run the Server
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )