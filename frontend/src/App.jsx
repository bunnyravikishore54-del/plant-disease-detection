import { useState } from "react";
import axios from "axios";
import Upload from "./components/Upload";
import ResultCard from "./components/ResultCard";
import Loader from "./components/Loader";

// Change this to your deployed backend URL when hosting
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelect = (file) => {
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!image) return;

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", image);

      const response = await axios.post(`${API_URL}/predict`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 30000,
      });

      setResult(response.data);
    } catch (err) {
      if (err.code === "ECONNABORTED") {
        setError("Request timed out. Please try again.");
      } else if (err.response) {
        setError(err.response.data.detail || "Analysis failed. Please try again.");
      } else {
        setError("Cannot connect to server. Make sure the backend is running.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50">
      <div className="max-w-2xl mx-auto px-4 py-10">

        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 bg-green-100 text-green-800 text-xs font-semibold px-3 py-1 rounded-full mb-4">
            🌿 AI-Powered Plant Health
          </div>
          <h1 className="text-4xl font-extrabold text-gray-900 leading-tight">
            Plant Disease <span className="text-green-600">Detector</span>
          </h1>
          <p className="text-gray-500 mt-3 text-base">
            Upload a photo of your plant. AI will detect diseases and suggest treatments.
          </p>
        </div>

        {/* Upload */}
        <Upload onFileSelect={handleFileSelect} hasFile={!!image} />

        {/* Preview */}
        {preview && (
          <div className="mt-4 rounded-2xl overflow-hidden border border-gray-200 shadow-sm">
            <div className="flex items-center justify-between px-4 py-2 bg-white border-b border-gray-100">
              <span className="text-sm text-gray-500 font-medium">📷 {image?.name}</span>
              <button
                onClick={handleReset}
                className="text-xs text-red-500 hover:text-red-700 font-medium"
              >
                ✕ Remove
              </button>
            </div>
            <img
              src={preview}
              alt="Plant preview"
              className="w-full max-h-80 object-cover"
            />
          </div>
        )}

        {/* Analyze Button */}
        {image && !loading && (
          <button
            onClick={handleAnalyze}
            className="mt-4 w-full bg-green-600 hover:bg-green-700 active:scale-[0.99] text-white font-semibold py-3.5 px-6 rounded-2xl transition-all duration-150 flex items-center justify-center gap-2 shadow-md"
          >
            🔍 Analyze Plant
          </button>
        )}

        {/* Loader */}
        {loading && <Loader />}

        {/* Error */}
        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-800 rounded-2xl p-4 text-sm flex items-start gap-2">
            <span>⚠️</span>
            <div>
              <p className="font-semibold">Analysis failed</p>
              <p className="mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {result && <ResultCard result={result} />}

        {/* Footer */}
        <p className="text-center text-xs text-gray-400 mt-10">
          Supports 38 plant diseases across 14 crop types • PlantVillage Dataset
        </p>
      </div>
    </div>
  );
}