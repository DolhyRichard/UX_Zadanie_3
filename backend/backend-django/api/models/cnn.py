# models/cnn.py

import os
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from collections import Counter
from tqdm import tqdm
import librosa

from config import BATCH_SIZE, EPOCHS, RANDOM_SEED, GENRES_PATH, GENRES, SAMPLE_RATE, N_MFCC, DURATION

class CNN:
    def __init__(self):
        self.model = None
        self.random_state = RANDOM_SEED

    def build_model(self, input_shape, n_classes):
        model = models.Sequential([
            layers.Input(shape=input_shape),

            layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling2D(),

            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(n_classes, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def load_dataset(self, segments=3, segment_duration=10):
        """
        Load dataset with multi-segment splitting for each track.
        """
        X, y = [], []
        track_ids = []  # track-level grouping for aggregation
        for genre in GENRES:
            folder = os.path.join(GENRES_PATH, genre)
            for filename in tqdm(os.listdir(folder), desc=f"Processing {genre}"):
                if not (filename.endswith(".wav") or filename.endswith(".au")):
                    continue
                file_path = os.path.join(folder, filename)
                y_track, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

                step = (DURATION - segment_duration) / max(segments - 1, 1)
                for i in range(segments):
                    start = int(i * step * sr)
                    end = int(start + segment_duration * sr)
                    segment = y_track[start:end]
                    if len(segment) < segment_duration * sr:
                        segment = np.pad(segment, (0, int(segment_duration * sr) - len(segment)))

                    # compute MFCC
                    mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=N_MFCC)
                    # add channel dimension
                    X.append(mfcc[..., np.newaxis])
                    y.append(genre)
                    track_ids.append(filename)  # track-level grouping
        return np.array(X), np.array(y), np.array(track_ids)

    def aggregate_track_predictions(self, y_pred_segments, track_ids):
        """
        Aggregate segment-level predictions to track-level using majority vote.
        """
        track_preds = {}
        for pred, tid in zip(y_pred_segments, track_ids):
            track_preds.setdefault(tid, []).append(pred)

        track_final_preds = [Counter(track_preds[tid]).most_common(1)[0][0] for tid in track_preds]
        return track_final_preds, list(track_preds.keys())

    def analyze(self):
        print("Loading dataset for CNN with multi-segment splitting...")
        X, y, track_ids = self.load_dataset(segments=3, segment_duration=10)
        if X.size == 0:
            print("No data found for CNN.")
            return

        # --- GLOBAL NORMALIZATION ---
        mean = np.mean(X, axis=(0, 1, 2), keepdims=True)
        std = np.std(X, axis=(0, 1, 2), keepdims=True) + 1e-9
        X = (X - mean) / std

        # encode labels
        le = LabelEncoder()
        y_enc = le.fit_transform(y)

        # split
        X_train, X_test, y_train, y_test, track_ids_train, track_ids_test = train_test_split(
            X, y_enc, track_ids, test_size=0.2, random_state=self.random_state, stratify=y_enc
        )

        input_shape = X_train.shape[1:]
        n_classes = len(le.classes_)

        # model = self.build_model(input_shape, n_classes)
        # model.summary()

        MODEL_PATH = "saved_models/cnn_model.keras"
        LABELS_PATH = "saved_models/label_encoder.npy"

        # ----------------------------- #
        # 1. IF MODEL EXISTS → LOAD IT
        # ----------------------------- #
        if os.path.exists(MODEL_PATH) and os.path.exists(LABELS_PATH):
            print("Loading existing CNN model...")
            model = load_model(MODEL_PATH)

            saved_classes = np.load(LABELS_PATH, allow_pickle=True)
            if len(saved_classes) != n_classes:
                print("WARNING: Label count changed. Rebuilding model...")
                model = self.build_model(input_shape, n_classes)
        else:
            print("No saved model found. Building a new CNN...")
            model = self.build_model(input_shape, n_classes)

        model.summary()
        self.model = model

        # Retrain if needed
        # model.fit(
        #     X_train, y_train,
        #     batch_size=BATCH_SIZE,
        #     epochs=EPOCHS,
        #     validation_split=0.1,
        #     verbose=2
        # )

        # segment-level predictions
        y_pred_segments = np.argmax(model.predict(X_test), axis=1)

        # aggregate to track-level
        track_preds, track_names = self.aggregate_track_predictions(y_pred_segments, track_ids_test)
        # get true labels per track (use first segment)
        true_track_labels = []
        for tid in track_names:
            idx = np.where(track_ids_test == tid)[0][0]
            true_track_labels.append(y_test[idx])
        true_track_labels = np.array(true_track_labels)

        accuracy = float(accuracy_score(true_track_labels, track_preds))
        print("Track-level CNN Accuracy:", accuracy)
        print(classification_report(true_track_labels, track_preds, target_names=le.classes_))

        self.model = model

        self.model.save("saved_models/cnn_model.keras")
        np.save("saved_models/label_encoder.npy", le.classes_)
        return accuracy, le.classes_

    def preprocess_audio(self, file_path, segments=3, segment_duration=10):
        """
        Create MFCC segments from a user-provided audio file.
        Returns: X (model inputs), track_ids (for consistency)
        """
        audio, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

        X = []
        track_ids = []

        step = (DURATION - segment_duration) / max(segments - 1, 1)

        for i in range(segments):
            start = int(i * step * sr)
            end = int(start + segment_duration * sr)
            segment = audio[start:end]

            if len(segment) < segment_duration * sr:
                segment = np.pad(segment, (0, int(segment_duration * sr) - len(segment)))

            mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=N_MFCC)
            X.append(mfcc[..., np.newaxis])   # add channel dim
            track_ids.append(file_path)

        return np.array(X), np.array(track_ids)

    # def predict_user_song(self, file_path):
    #     """
    #     Predicts the genre of a user-provided audio file using trained CNN.
    #     """
    #     print(f"\n🔍 Processing user file: {file_path}")
    #
    #     # load saved label encoder
    #     LABELS_PATH = "saved_models/label_encoder.npy"
    #     if not os.path.exists(LABELS_PATH):
    #         print("ERROR: No saved label encoder found. Run training first.")
    #         return
    #
    #     classes = np.load(LABELS_PATH, allow_pickle=True)
    #
    #     X, track_ids = self.preprocess_audio(file_path)
    #
    #     # apply same normalization used for training
    #     mean = np.mean(X, axis=(0, 1, 2), keepdims=True)
    #     std = np.std(X, axis=(0, 1, 2), keepdims=True) + 1e-9
    #     X = (X - mean) / std
    #
    #     # get segment predictions
    #     y_pred_segments = np.argmax(self.model.predict(X), axis=1)
    #
    #     # majority vote
    #     final_pred = Counter(y_pred_segments).most_common(1)[0][0]
    #
    #     print(f"🎵 Final Prediction: **{classes[final_pred]}**\n")
    #     return classes[final_pred]


    def predict_user_song(self, file_path):
        LABELS_PATH = "saved_models/label_encoder.npy"
        if not os.path.exists(LABELS_PATH):
            return None, None  # return None if labels missing

        labels = np.load(LABELS_PATH, allow_pickle=True)
        X, _ = self.preprocess_audio(file_path)

        # normalization
        mean = np.mean(X, axis=(0, 1, 2), keepdims=True)
        std = np.std(X, axis=(0, 1, 2), keepdims=True) + 1e-9
        X = (X - mean) / std

        probs = self.model.predict(X)
        y_pred = np.argmax(probs, axis=1)
        from collections import Counter
        final_index = Counter(y_pred).most_common(1)[0][0]
        label = labels[final_index]

        confidence = float(np.mean(probs[:, final_index]))
        return label, confidence
