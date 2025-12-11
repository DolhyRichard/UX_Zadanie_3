# models/svm.py

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
import joblib, os
import numpy as np

from config import RANDOM_SEED, MODEL_SAVE_PATH
from ..utils.dataset_loader import load_classical_dataset


class SVMClassifier:
    def __init__(self):
        self.model = None
        self.le = None
        self.random_state = RANDOM_SEED
        self.accuracy = None  # store accuracy

    # ---------------------------------------------------------------------
    # TRAIN / LOAD MODEL
    # ---------------------------------------------------------------------
    def analyze(self):
        """
        Loads SVM model from disk if available.
        If not, trains and saves it.
        Also calculates accuracy.
        """

        model_path = os.path.join(MODEL_SAVE_PATH, "svm_model.joblib")
        le_path = os.path.join(MODEL_SAVE_PATH, "svm_label_encoder.joblib")
        acc_path = os.path.join(MODEL_SAVE_PATH, "svm_accuracy.txt")

        # ------------------------------------------------------
        # Load existing model
        # ------------------------------------------------------
        if os.path.exists(model_path) and os.path.exists(le_path):
            print("Loading SVM model from disk...")
            self.model = joblib.load(model_path)
            self.le = joblib.load(le_path)

            # Load stored accuracy
            if os.path.exists(acc_path):
                with open(acc_path, "r") as f:
                    self.accuracy = float(f.read().strip())

            return self.accuracy

        # ------------------------------------------------------
        # TRAIN NEW MODEL
        # ------------------------------------------------------
        print("Training SVM (first time)...")
        X, y = load_classical_dataset()
        if X.size == 0:
            print("ERROR: Empty dataset")
            return None

        # Encode labels
        self.le = LabelEncoder()
        y_enc = self.le.fit_transform(y)

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_enc, test_size=0.2, random_state=self.random_state, stratify=y_enc
        )

        # Pipeline: StandardScaler + SVM
        clf = make_pipeline(StandardScaler(),
                            SVC(kernel='rbf', probability=True, random_state=self.random_state))

        clf.fit(X_train, y_train)

        # Accuracy
        y_pred = clf.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        print("SVM Accuracy:", self.accuracy)
        print(classification_report(y_test, y_pred, target_names=self.le.classes_))

        self.model = clf

        # Save
        os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
        joblib.dump(clf, model_path)
        joblib.dump(self.le, le_path)

        # Save accuracy
        with open(acc_path, "w") as f:
            f.write(str(self.accuracy))

        return self.accuracy

    # ---------------------------------------------------------------------
    # RETURN ACCURACY
    # ---------------------------------------------------------------------
    def get_accuracy(self):
        return self.accuracy

    # ---------------------------------------------------------------------
    # PREDICT USER AUDIO
    # ---------------------------------------------------------------------
    def predict_user_song(self, X):
        """
        Takes 1D feature vector.
        Returns (predictedLabel, confidenceScore)
        """

        # Ensure model is loaded
        if self.model is None or self.le is None:
            self.analyze()  # load or train model

        if self.model is None:
            return None, None

        # Convert to 2D for sklearn
        X = np.array(X).reshape(1, -1)

        # Predict
        pred_idx = self.model.predict(X)[0]
        pred_label = self.le.inverse_transform([pred_idx])[0]

        # Confidence using SVC probability=True
        try:
            proba = self.model.predict_proba(X)[0]
            confidence = float(proba[pred_idx])
        except:
            confidence = None

        return pred_label, confidence
