import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

/* ---------------- MOCK DATA ---------------- */
const MODELS = ["CNN", "CRNN", "KNN", "RF", "SVM"];
const LABELS = ["Rock", "Hip Hop", "Jazz", "Classical", "Metal"];

const MOCK_SONGS = Array.from({ length: 50 }).map((_, i) => {
  const label = LABELS[i % LABELS.length];
  return {
    id: i + 1,
    filename: `${label.toLowerCase().replace(" ", "")}.${String(i).padStart(5, "0")}.au`,
    label,
  };
});

/* ---------------- COMPONENT ---------------- */
export default function Tester() {
  const navigate = useNavigate();

  const [model, setModel] = useState("CNN");
  const [datasetPath, setDatasetPath] = useState("/datasets/gtzan");
  const [trainSplit, setTrainSplit] = useState(80);
  const [shuffle, setShuffle] = useState(true);
  const [augment, setAugment] = useState(false);

  const [training, setTraining] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [songs, setSongs] = useState(MOCK_SONGS);
  const [showSongs, setShowSongs] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 640);

  // Update isMobile on resize
  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 640);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const removeSong = (id: number) => setSongs(prev => prev.filter(song => song.id !== id));

  const startTraining = () => {
    setTraining(true);
    setResult(null);

    setTimeout(() => {
      const baseAccuracy = { CNN: 0.83, CRNN: 0.86, SVM: 0.78, RF: 0.75, KNN: 0.70 }[model];
      const noise = Math.random() * 0.05 - 0.02;
      const splitFactor = (trainSplit - 70) * 0.001;
      const augFactor = augment ? 0.02 : 0;
      const shuffleFactor = shuffle ? 0.005 : -0.005;

      const finalAccuracy = Math.min(baseAccuracy + noise + splitFactor + augFactor + shuffleFactor, 0.95);

      const trainingResult = {
        model,
        accuracy: `${(finalAccuracy * 100).toFixed(2)}%`,
        dataset: datasetPath,
        trainTestSplit: `${trainSplit}/${100 - trainSplit}`,
        shuffle,
        augmentation: augment,
        samplesUsed: songs.length,
        trainedAt: new Date().toLocaleString(),
      };

      setResult(trainingResult);

      const history = JSON.parse(localStorage.getItem("trainingHistory") || "[]");
      localStorage.setItem("trainingHistory", JSON.stringify([trainingResult, ...history]));

      setTraining(false);
    }, 5000);
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 p-8 flex justify-center">
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-8 w-full max-w-4xl">

        {/* Mobile History Button */}
        {isMobile && (
          <div className="mb-4 flex justify-center">
            <button
              onClick={() => navigate("/history")}
              className="px-3 py-1 text-sm font-semibold rounded bg-indigo-500 hover:bg-indigo-600 text-white transition"
            >
              View History →
            </button>
          </div>
        )}

        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-indigo-700 dark:text-indigo-400 text-center w-full">
            Model Training Tester
          </h1>

          {/* Desktop History Button */}
          {!isMobile && (
            <button
              onClick={() => navigate("/history")}
              className="px-4 py-2 text-sm font-semibold rounded-lg border border-indigo-500 text-indigo-600 hover:bg-indigo-50 dark:text-indigo-400 dark:hover:bg-gray-800 transition"
            >
              View History →
            </button>
          )}
        </div>

        {/* Model Selector */}
        <div className="mb-4">
          <label className="block font-medium mb-1">Model</label>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-800"
          >
            {MODELS.map((m) => (
              <option key={m}>{m}</option>
            ))}
          </select>
        </div>

        {/* Dataset path */}
        <div className="mb-4">
          <label className="block font-medium mb-1">Dataset path</label>
          <input
            value={datasetPath}
            onChange={(e) => setDatasetPath(e.target.value)}
            className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-800"
          />
        </div>

        {/* Dataset preview */}
        <div className="mb-4">
          <div
            onClick={() => setShowSongs(!showSongs)}
            className="flex items-center justify-between p-3 border rounded cursor-pointer bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition"
          >
            <div>
              <p className="font-medium text-gray-800 dark:text-gray-200">
                Training samples
              </p>
              <p className="text-sm text-gray-500">{songs.length} audio files will be used</p>
            </div>
            <div className="text-gray-400 text-xl">{showSongs ? "▼" : "▶"}</div>
          </div>

          {showSongs && (
            <div className="mt-2 max-h-64 overflow-y-auto border rounded bg-gray-50 dark:bg-gray-800 text-sm">
              {songs.map(song => (
                <div key={song.id} className="px-3 py-2 border-b last:border-none text-gray-700 dark:text-gray-300 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                  <span className="font-medium truncate">{song.filename}</span>
                  <div className="flex items-center justify-between sm:justify-end gap-2">
                    <span className="text-sm bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
                      Label: {song.label}
                    </span>
                    <button
                      onClick={() => removeSong(song.id)}
                      className="px-2 py-1 text-xs rounded bg-red-500 hover:bg-red-600 text-white transition"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Train/Test split */}
        <div className="mb-4">
          <label className="block font-medium mb-1">
            Train / Test split ({trainSplit}% / {100 - trainSplit}%)
          </label>
          <input
            type="range"
            min={60}
            max={90}
            value={trainSplit}
            onChange={(e) => setTrainSplit(Number(e.target.value))}
            className="w-full"
          />
        </div>

        {/* Options */}
        <div className="flex gap-6 mb-6">
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={shuffle} onChange={() => setShuffle(!shuffle)} />
            Shuffle data
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={augment} onChange={() => setAugment(!augment)} />
            Data augmentation
          </label>
        </div>

        {/* Train button */}
        <button
          onClick={startTraining}
          disabled={training}
          className={`w-full py-3 rounded font-semibold text-white ${training ? "bg-gray-400" : "bg-indigo-500 hover:bg-indigo-600"}`}
        >
          {training ? "Training model..." : "Retrain model"}
        </button>

        {/* Animated Loading */}
        {training && (
          <div className="mt-6">
            <div className="relative w-full h-1 bg-gray-200 dark:bg-gray-700 overflow-hidden rounded">
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 via-indigo-600 to-indigo-400 animate-ml-loader" />
            </div>
            <p className="mt-3 text-center text-xs tracking-wide uppercase text-gray-500 dark:text-gray-400">
              Repeating my past mistakes so You don't have to
            </p>
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="mt-6 bg-gray-50 dark:bg-gray-800 p-4 rounded border max-h-64 overflow-y-auto">
            <h2 className="font-bold mb-2">Training Result</h2>
            <pre className="text-sm">{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
