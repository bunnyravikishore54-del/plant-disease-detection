# 🌿 Plant Disease Detection App

An AI-powered web application that detects plant diseases from images and suggests treatments.

![Demo](demo.gif)

## Features
- 📸 Upload plant images (JPG, PNG, WEBP)
- 🔬 Detects 38 types of plant diseases across 14 crops
- 💊 Suggests medicines and treatments
- 🛡️ Provides prevention tips
- 📊 Shows confidence scores

## Tech Stack
- **Frontend:** React 18, Vite, TailwindCSS, Axios
- **Backend:** Python, FastAPI, TensorFlow 2.13, EfficientNetB3
- **Dataset:** PlantVillage (54,000+ images, 38 classes)
- **Deployment:** Vercel (frontend) + Render (backend)

## Local Setup

### Backend
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train.py           # Train the model (1-4 hours)
python main.py            # Start API server
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
\`\`\`

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health |
| POST | `/predict` | Predict disease from image |

## Model Performance
- Training accuracy: ~97%
- Validation accuracy: ~95%
- Dataset: PlantVillage

## Live Demo
- Frontend: [your-app.vercel.app](https://your-app.vercel.app)
- API: [your-api.onrender.com](https://your-api.onrender.com)