import { useState, useRef } from "react";

export default function Upload({ onFileSelect, hasFile }) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) onFileSelect(file);
  };

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) onFileSelect(file);
  };

  return (
    <div
      onClick={() => inputRef.current.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`
        border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer
        transition-all duration-200 select-none
        ${dragging
          ? "border-green-500 bg-green-50 scale-[1.01]"
          : "border-green-300 bg-white hover:border-green-400 hover:bg-green-50"
        }
      `}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
      />
      <div className="text-5xl mb-4">{hasFile ? "🔄" : "📸"}</div>
      <p className="text-lg font-semibold text-gray-700">
        {hasFile ? "Upload a different image" : "Drop your plant photo here"}
      </p>
      <p className="text-sm text-gray-400 mt-1">or click to browse — JPG, PNG, WEBP</p>
    </div>
  );
}