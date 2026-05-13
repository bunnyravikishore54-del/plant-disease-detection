from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import anthropic
import base64
import uvicorn
import os

app = FastAPI(title="Plant Disease Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.get("/")
def root():
    return {"status": "ok", "message": "Plant Disease Detection API is running 🌿"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Use JPG, PNG, or WEBP image.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max 10MB.")

    image_b64 = base64.standard_b64encode(contents).decode("utf-8")

    prompt = """You are an expert plant pathologist. Analyze this plant image carefully.
Respond ONLY with a valid JSON object, no extra text:
{
  "disease_name": "Name of disease or 'Healthy Plant'",
  "is_healthy": false,
  "confidence": 85,
  "medicines": ["medicine 1", "medicine 2"],
  "prevention_tips": ["tip 1", "tip 2", "tip 3"],
  "top_predictions": [
    {"label": "Most likely disease", "confidence": 85},
    {"label": "Second possibility", "confidence": 10},
    {"label": "Third possibility", "confidence": 5}
  ]
}"""

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": file.content_type,
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": prompt}
                    ],
                }
            ],
        )

        import json
        raw = message.content[0].text
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
