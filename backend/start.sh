#!/bin/bash
echo "Downloading model from Google Drive..."
python download_model.py
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port $PORT