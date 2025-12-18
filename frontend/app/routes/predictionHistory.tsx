import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

type HistoryItem = {
  id: string;
  filename: string;
  model: string;
  predictedLabel: string;
  confidence: number;
  feedback: "correct" | "incorrect" | "none";
  createdAt: string;
};

const LABELS = ["Hip Hop", "Rock", "Jazz", "Classical", "Pop", "Metal"];
const MODELS = ["CNN", "CRNN", "SVM", "RF", "KNN"];

const MOCK_HISTORY = Array.from({ length: 75 }, (_, i) => {
  const confidence = Math.random() * (0.99 - 0.55) + 0.55;

  return {
    id: `${i + 1}`,
    filename: `song_${String(i + 1).padStart(3, "0")}.wav`,
    model: MODELS[Math.floor(Math.random() * MODELS.length)],
    predictedLabel: LABELS[Math.floor(Math.random() * LABELS.length)],
    confidence,
    feedback:
      confidence > 0.8
        ? "correct"
        : confidence < 0.65
        ? "incorrect"
        : "none",
    createdAt: new Date(
      Date.now() - Math.random() * 1000 * 60 * 60 * 24
    ).toLocaleString(),
  };
});

export default function PredictionHistory() {
  const navigate = useNavigate();
  const [history, setHistory] = useState<HistoryItem[]>(MOCK_HISTORY);
  const [isMobile, setIsMobile] = useState(false);

  // Safe client-side check for window
  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 640);
    handleResize(); // initial check
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 p-8">
      <div className="max-w-5xl mx-auto bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-8">

        {/* Mobile Back Button (Centered) */}
        {isMobile && (
          <div className="mb-4 flex justify-center">
            <button
              onClick={() => navigate("/tester")}
              className="px-4 py-2 text-sm font-semibold rounded bg-indigo-500 hover:bg-indigo-600 text-white transition"
            >
              ← Back to Tester
            </button>
          </div>
        )}

        {/* Header */}
        <div className="relative flex items-center justify-center mb-6">
          <h1 className="text-3xl font-bold text-indigo-700 dark:text-indigo-400 text-center">
            Prediction History
          </h1>

          {/* Desktop Back Button (Top-Right) */}
          {!isMobile && (
            <button
              onClick={() => navigate("/tester")}
              className="absolute right-0 px-4 py-2 text-sm font-semibold rounded-lg border border-indigo-500 text-indigo-600 hover:bg-indigo-50 dark:text-indigo-400 dark:hover:bg-gray-800 transition"
            >
              ← Back to Tester
            </button>
          )}
        </div>

        {/* Description */}
        <p className="text-gray-600 dark:text-gray-400 mb-6 text-center">
          Overview of all uploaded audio files and their prediction results.
        </p>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="text-left border-b dark:border-gray-700">
                <th className="py-3 px-4">File</th>
                <th className="py-3 px-4">Model</th>
                <th className="py-3 px-4">Prediction</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Feedback</th>
                <th className="py-3 px-4">Date</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr
                  key={item.id}
                  className="border-b last:border-none dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
                >
                  <td className="py-3 px-4 font-medium">{item.filename}</td>
                  <td className="py-3 px-4">{item.model}</td>
                  <td className="py-3 px-4">{item.predictedLabel}</td>
                  <td className="py-3 px-4">{(item.confidence * 100).toFixed(1)}%</td>
                  <td className="py-3 px-4">
                    {item.feedback === "correct" && (
                      <span className="px-2 py-1 text-xs rounded bg-green-100 text-green-700">
                        Correct
                      </span>
                    )}
                    {item.feedback === "incorrect" && (
                      <span className="px-2 py-1 text-xs rounded bg-red-100 text-red-700">
                        Incorrect
                      </span>
                    )}
                    {item.feedback === "none" && (
                      <span className="px-2 py-1 text-xs rounded bg-gray-100 text-gray-600">
                        No feedback
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-500">{item.createdAt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {history.length === 0 && (
          <div className="text-center text-gray-500 py-12">
            No prediction history available.
          </div>
        )}
      </div>
    </div>
  );
}
