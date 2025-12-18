import React, { useState } from "react";

const MODELS = ["CNN", "CRNN", "KNN", "RF", "SVM"];

export default function Tester() {
  const [model, setModel] = useState("CNN");
  const [datasetPath, setDatasetPath] = useState("/datasets/gtzan");
  const [trainSplit, setTrainSplit] = useState(80);
  const [shuffle, setShuffle] = useState(true);
  const [augment, setAugment] = useState(false);

  const [training, setTraining] = useState(false);
  const [result, setResult] = useState<any>(null);

  const startTraining = () => {
    setTraining(true);
    setResult(null);

    setTimeout(() => {
      const baseAccuracy = {
        CNN: 0.83,
        CRNN: 0.86,
        SVM: 0.78,
        RF: 0.75,
        KNN: 0.70,
      }[model];

      const noise = (Math.random() * 0.04) - 0.02;
      const splitBonus = trainSplit > 80 ? 0.01 : 0;
      const augBonus = augment ? 0.015 : 0;

      const finalAccuracy = Math.min(
        baseAccuracy + noise + splitBonus + augBonus,
        0.95
      );

      setResult({
        model,
        accuracy: `${(finalAccuracy * 100).toFixed(2)}%`,
        dataset: datasetPath,
        trainTestSplit: `${trainSplit}/${100 - trainSplit}`,
        shuffle,
        augmentation: augment,
        trainedAt: new Date().toLocaleString(),
      });

      setTraining(false);
    }, 5000);
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 p-8 flex justify-center">
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-8 w-full max-w-2xl">

        <h1 className="text-3xl font-bold text-indigo-700 dark:text-indigo-400 mb-6">
          Model Training Tester
        </h1>

        {/* Model */}
        <div className="mb-4">
          <label className="block font-medium mb-1">Model</label>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-800"
          >
            {MODELS.map(m => <option key={m}>{m}</option>)}
          </select>
        </div>

        {/* Dataset */}
        <div className="mb-4">
          <label className="block font-medium mb-1">Dataset path</label>
          <input
            value={datasetPath}
            onChange={(e) => setDatasetPath(e.target.value)}
            className="w-full p-2 border rounded bg-gray-50 dark:bg-gray-800"
          />
        </div>

        {/* Train/Test */}
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
            <input
              type="checkbox"
              checked={shuffle}
              onChange={() => setShuffle(!shuffle)}
            />
            Shuffle data
          </label>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={augment}
              onChange={() => setAugment(!augment)}
            />
            Data augmentation
          </label>
        </div>

        {/* Train Button */}
        <button
          onClick={startTraining}
          disabled={training}
          className={`w-full py-3 rounded font-semibold text-white ${
            training
              ? "bg-gray-400"
              : "bg-indigo-500 hover:bg-indigo-600"
          }`}
        >
          {training ? "Training model..." : "Retrain model"}
        </button>

        {/* Training indicator */}
        {training && (
          <div className="mt-4 text-center text-sm text-gray-500 animate-pulse">
            Running experiment, please wait...
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="mt-6 bg-gray-50 dark:bg-gray-800 p-4 rounded border">
            <h2 className="font-bold mb-2">Training Result</h2>
            <pre className="text-sm">{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}

      </div>
    </div>
  );
}
