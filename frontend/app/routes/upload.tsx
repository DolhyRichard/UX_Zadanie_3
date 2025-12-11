import React, { useState, useRef } from "react";

const models = ["CNN", "CRNN", "KNN", "RF", "SVM"];

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [model, setModel] = useState("CNN");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setResult(null);
      setError(null);
      setFeedbackMessage(null);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult(null);
    setError(null);
    setFeedbackMessage(null);

    try {
      const endpointMap: Record<string, string> = {
        CNN: "/api/predict/cnn/",
        CRNN: "/api/predict/crnn/",
        KNN: "/api/predict/knn/",
        RF: "/api/predict/rf/",
        SVM: "/api/predict/svm/",
      };

      const response = await fetch(
        `http://localhost:8000${endpointMap[model]}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Server error: ${response.status} - ${text}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to fetch");
    } finally {
      setLoading(false);
    }
  };

  const sendFeedback = async (correct: boolean) => {
    if (!result?.file_id) {
      setFeedbackMessage("Backend did not return file_id!");
      return;
    }

    try {
      const url = correct
        ? "http://localhost:8000/api/feedback/correct/"
        : "http://localhost:8000/api/feedback/incorrect/";

      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_id: result.file_id }),
      });

      const data = await response.json();

      setFeedbackMessage(
        correct
          ? "Ďakujeme! Predikácia bola označená ako správna."
          : "Súbor bol vymazaný, predikácia bola označená ako nesprávna."
      );
    } catch (err: any) {
      console.error(err);
      setFeedbackMessage("Nepodarilo sa odoslať feedback.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-lg">
        <h1 className="text-3xl font-bold text-center text-indigo-700 mb-6">
          Audio Prediction
        </h1>

        {/* Model Selector */}
        <div className="mb-4">
          <label className="block font-medium mb-2 text-gray-700">
            Select Model:
          </label>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded bg-gray-50 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {models.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>

        {/* Drag & Drop Upload */}
        <div
          onDrop={handleFileDrop}
          onDragOver={(e) => e.preventDefault()}
          onClick={handleClick}
          className="mb-4 p-6 border-2 border-dashed border-indigo-300 rounded-lg text-center cursor-pointer hover:border-indigo-500 transition-colors bg-gray-50 text-gray-900"
        >
          {file ? (
            <p className="text-gray-700 font-medium">Selected: {file.name}</p>
          ) : (
            <p className="text-gray-400">
              Drag & drop audio here, or click to select file
            </p>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="audio/*"
            onChange={(e) => e.target.files && setFile(e.target.files[0])}
            className="hidden"
          />
        </div>

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={loading || !file}
          className={`w-full py-3 rounded text-white font-semibold ${
            loading || !file
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-indigo-500 hover:bg-indigo-600"
          }`}
        >
          {loading ? "Uploading..." : "Upload & Predict"}
        </button>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 border border-red-200 rounded">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Prediction Result */}
        {result && (
          <div className="mt-6 p-4 bg-gray-50 border border-gray-200 rounded">
            <h2 className="font-bold mb-2 text-gray-800">Prediction Result:</h2>
            <pre className="text-sm text-gray-700">
              {JSON.stringify(result, null, 2)}
            </pre>

            {/* Feedback Buttons */}
            <div className="mt-4 flex gap-3">
              <button
                onClick={() => sendFeedback(true)}
                className="flex-1 py-2 bg-green-500 hover:bg-green-600 text-white rounded font-semibold"
              >
                Predikácia bola správna
              </button>
              <button
                onClick={() => sendFeedback(false)}
                className="flex-1 py-2 bg-red-500 hover:bg-red-600 text-white rounded font-semibold"
              >
                Predikácia bola nesprávna
              </button>
            </div>
          </div>
        )}

        {/* Feedback Message */}
        {feedbackMessage && (
          <div className="mt-4 p-3 bg-blue-100 text-blue-700 border border-blue-200 rounded">
            {feedbackMessage}
          </div>
        )}
      </div>
    </div>
  );
}
