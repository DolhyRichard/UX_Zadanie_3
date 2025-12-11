# models/random_forest.py

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from config import RANDOM_SEED, MODEL_SAVE_PATH
from ..utils.dataset_loader import load_classical_dataset
# from ..utils.preprocess import extract_feature_vector


class RandomForestModel:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.accuracy = None
        self.random_state = RANDOM_SEED

    # ---------------------------------------------------------------------
    # TRAIN OR LOAD MODEL
    # ---------------------------------------------------------------------
    def analyze(self):
        model_path = os.path.join(MODEL_SAVE_PATH, "rf_model.joblib")
        le_path = os.path.join(MODEL_SAVE_PATH, "rf_label_encoder.joblib")
        acc_path = os.path.join(MODEL_SAVE_PATH, "rf_accuracy.txt")

        # ---------------------------------------
        # Load existing model
        # ---------------------------------------
        if os.path.exists(model_path) and os.path.exists(le_path):
            print("Loading saved RandomForest model...")
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(le_path)

            if os.path.exists(acc_path):
                with open(acc_path, "r") as f:
                    self.accuracy = float(f.read().strip())

            return self.accuracy

        # ---------------------------------------
        # Train new model
        # ---------------------------------------
        print("Training RandomForest (first time)...")

        X, y = load_classical_dataset()
        if X.size == 0:
            print("No samples found.")
            return None

        # Encode labels
        le = LabelEncoder()
        y_enc = le.fit_transform(y)
        self.label_encoder = le

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_enc, test_size=0.2, random_state=self.random_state, stratify=y_enc
        )

        # Train RF
        clf = RandomForestClassifier(
            n_estimators=250,
            random_state=self.random_state
        )
        clf.fit(X_train, y_train)
        self.model = clf

        # Evaluate
        y_pred = clf.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)

        print("RandomForest Accuracy:", self.accuracy)
        print(classification_report(y_test, y_pred, target_names=le.classes_))

        # Save model + encoder + accuracy
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
        Takes 1D feature vector.
        Returns (label, confidence).
        """

        # Load model if needed
        if self.model is None or self.label_encoder is None:
            self.analyze()

        if self.model is None:
            return None, None

        # Ensure vector is 2D
        X = np.array(feature_vector).reshape(1, -1)

        # Predict class index
        pred_idx = self.model.predict(X)[0]
        pred_label = self.label_encoder.inverse_transform([pred_idx])[0]

        # Confidence from predict_proba
        if hasattr(self.model, "predict_proba"):
            probas = self.model.predict_proba(X)[0]
            confidence = float(probas[pred_idx])
        else:
            confidence = None

        return pred_label, confidence
