# models/knn.py

import os
import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report

from config import RANDOM_SEED, MODEL_SAVE_PATH
from ..utils.dataset_loader import load_classical_dataset
from ..utils.preprocess import extract_feature_vector


class KNNClassifier:
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
        self.model = None
        self.label_encoder = None
        self.random_state = RANDOM_SEED
        self.accuracy = None

    # ---------------------------------------------------------------------
    # TRAIN OR LOAD MODEL
    # ---------------------------------------------------------------------
    def analyze(self):
        """
        Loads KNN model if saved.
        Otherwise trains it and saves it.
        """
        model_path = os.path.join(MODEL_SAVE_PATH, "knn_model.joblib")
        le_path = os.path.join(MODEL_SAVE_PATH, "knn_label_encoder.joblib")
        acc_path = os.path.join(MODEL_SAVE_PATH, "knn_accuracy.txt")

        # ------------------------------------------------------
        # Load model if exists
        # ------------------------------------------------------
        if os.path.exists(model_path) and os.path.exists(le_path):
            print("Loading saved KNN model...")
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(le_path)

            if os.path.exists(acc_path):
                with open(acc_path, "r") as f:
                    self.accuracy = float(f.read().strip())

            return self.accuracy

        # ------------------------------------------------------
        # Train model
        # ------------------------------------------------------
        print("Training k-NN model (first time)...")

        X, y = load_classical_dataset()
        if X.size == 0:
            print("No data found.")
            return None

        # Encode labels
        le = LabelEncoder()
        y_enc = le.fit_transform(y)
        self.label_encoder = le

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_enc, test_size=0.2, random_state=self.random_state, stratify=y_enc
        )

        # k-NN pipeline
        clf = make_pipeline(
            StandardScaler(),
            KNeighborsClassifier(n_neighbors=self.n_neighbors)
        )
        clf.fit(X_train, y_train)
        self.model = clf

        # Accuracy
        y_pred = clf.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        print("k-NN Accuracy:", self.accuracy)
        print(classification_report(y_test, y_pred, target_names=le.classes_))

        # Save model and encoder
        os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
        joblib.dump(clf, model_path)
        joblib.dump(le, le_path)

        with open(acc_path, "w") as f:
            f.write(str(self.accuracy))

        return self.accuracy

    # ---------------------------------------------------------------------
    # RETURN ACCURACY
    # ---------------------------------------------------------------------
    def get_accuracy(self):
        return self.accuracy

    # ---------------------------------------------------------------------
    # PREDICT
    # ---------------------------------------------------------------------
    def predict_user_song(self, feature_vector):
        """
        Takes 1D feature vector (not file path)
        Returns (label, confidence)
        """

        # Load model if needed
        if self.model is None or self.label_encoder is None:
            self.analyze()

        if self.model is None:
            return None, None

        # Ensure vector is 2D
        X = np.array(feature_vector).reshape(1, -1)

        # Predict index
        pred_idx = self.model.predict(X)[0]
        pred_label = self.label_encoder.inverse_transform([pred_idx])[0]

        # Confidence (soft voting using neighbors)
        neigh_dist, neigh_idx = self.model.named_steps['kneighborsclassifier'].kneighbors(X)

        # Convert distances → similarity confidence (inverse distance)
        dist = neigh_dist[0]
        if np.sum(dist) == 0:
            confidence = 1.0
        else:
            weights = 1 / (dist + 1e-8)
            confidence = float(np.mean(weights / np.sum(weights)))

        return pred_label, confidence
