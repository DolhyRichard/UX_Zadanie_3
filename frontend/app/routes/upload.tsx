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

//   const handleUpload = async () => {
//     if (!file) return;
//
//     const formData = new FormData();
//     formData.append("file", file);
//
//     setLoading(true);
//     setResult(null);
//     setError(null);
//     setFeedbackMessage(null);
//
//     try {
//       const endpointMap: Record<string, string> = {
//         CNN: "/api/predict/cnn/",
//         CRNN: "/api/predict/crnn/",
//         KNN: "/api/predict/knn/",
//         RF: "/api/predict/rf/",
//         SVM: "/api/predict/svm/",
//       };
//
//       const response = await fetch(
//         `http://localhost:8000${endpointMap[model]}`,
//         { method: "POST", body: formData }
//       );
//
//       if (!response.ok) {
//         const text = await response.text();
//         throw new Error(`Server error: ${response.status} - ${text}`);
//       }
//
//       const data = await response.json();
//       setResult(data);
//     } catch (err: any) {
//       setError(err.message || "Failed to fetch");
//     } finally {
//       setLoading(false);
//     }
//   };

const handleUpload = async () => {
  if (!file) return;

  setLoading(true);
  setResult(null);
  setError(null);
  setFeedbackMessage(null);

  // ⏱ simulate network delay
  setTimeout(() => {
    const mockResponse = {
      model_name: model,
      accuracy: "83%",
      current_prediction_confidence: "97%",
      predicted_label: "Hip Hop",
      file_id: "hiphop.00000.au",
    };

    setResult(mockResponse);
    setLoading(false);
  }, 5000);
};

//   const sendFeedback = async (correct: boolean) => {
//     if (!result?.file_id) {
//       setFeedbackMessage("Backend nevrátil file_id.");
//       return;
//     }
//
//     try {
//       const url = correct
//         ? "http://localhost:8000/api/feedback/correct/"
//         : "http://localhost:8000/api/feedback/incorrect/";
//
//       await fetch(url, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ file_id: result.file_id }),
//       });
//
//       setFeedbackMessage(
//         correct
//           ? "Ďakujeme! Predikácia bola označená ako správna."
//           : "Súbor bol vymazaný, predikácia bola označená ako nesprávna."
//       );
//     } catch {
//       setFeedbackMessage("Nepodarilo sa odoslať feedback.");
//     }
//   };

const sendFeedback = async (correct: boolean) => {
  if (!result?.file_id) {
    setFeedbackMessage("Mock error: file identifier missing.");
    return;
  }

  setFeedbackMessage(null);

  setTimeout(() => {
    if (correct) {
      setFeedbackMessage(
        "Odpoveď bola zaznamená ako správna.\nZáznam sa pridal do rady."
      );
    } else {
      setFeedbackMessage(
        "Odpoveď bola označenaá ako nesprávna.\nZáznam sa odstánil"
      );
    }
  }, 1200);
};


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-950 p-4">
      <div className="bg-white dark:bg-gray-900 shadow-xl rounded-2xl p-8 w-full max-w-lg">
        <h1 className="text-3xl font-bold text-center text-indigo-700 dark:text-indigo-400 mb-6">
          Audio Prediction
        </h1>

        {/* Model Selector */}
        <div className="mb-4">
          <label className="block font-medium mb-2 text-gray-700 dark:text-gray-300">
            Select Model
          </label>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full p-3 border border-gray-300 dark:border-gray-700 rounded bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {models.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>

        {/* Upload Area */}
        <div
          onDrop={handleFileDrop}
          onDragOver={(e) => e.preventDefault()}
          onClick={handleClick}
          className="mb-4 p-6 border-2 border-dashed border-indigo-300 dark:border-indigo-500 rounded-lg text-center cursor-pointer hover:border-indigo-500 transition bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        >
          {file ? (
            <p className="font-medium">{file.name}</p>
          ) : (
            <p className="text-gray-400">
              Drag & drop audio here or click to select
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
          className={`w-full py-3 rounded font-semibold text-white transition ${
            loading || !file
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-indigo-500 hover:bg-indigo-600"
          }`}
        >
          {loading ? "Uploading..." : "Upload & Predict"}
        </button>

        {/* Error */}
        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 border border-red-200 rounded">
            {error}
          </div>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="mt-6">
            <div className="relative w-full h-1 bg-gray-200 dark:bg-gray-700 overflow-hidden rounded">
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 via-indigo-600 to-indigo-400 animate-ml-loader" />
            </div>

            <p className="mt-3 text-center text-xs tracking-wide uppercase text-gray-500 dark:text-gray-400">
              Running model inference
            </p>
          </div>
        )}



        {/* Result */}
        {result && (
          <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded">
            <h2 className="font-bold mb-2">Prediction Result</h2>
            <pre className="text-sm overflow-x-auto">
              {JSON.stringify(result, null, 2)}
            </pre>

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

        {feedbackMessage && (
          <div className="mt-4 p-3 bg-blue-100 text-blue-700 border border-blue-200 rounded">
            {feedbackMessage}
          </div>
        )}
      </div>
    </div>
  );
}
