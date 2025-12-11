# models/crnn.py
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from collections import Counter
import librosa

from config import BATCH_SIZE, EPOCHS, RANDOM_SEED, N_MELS, FIXED_FRAMES
from ..utils.dataset_loader import load_cnn_dataset


class CRNN:
    def __init__(self):
        self.model = None
        self.random_state = RANDOM_SEED
        self.label_encoder = None
        self.overall_accuracy = None

    def build_model(self, input_shape, n_classes):
        inp = layers.Input(shape=input_shape)
        x = layers.Conv2D(16, (3, 3), padding='same', activation='relu')(inp)
        x = layers.MaxPool2D((2, 2))(x)
        x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = layers.MaxPool2D((2, 2))(x)

        x = layers.Permute((2, 1, 3))(x)  # (frames, n_mels, channels)
        x = layers.TimeDistributed(layers.Flatten())(x)
        x = layers.Bidirectional(layers.GRU(64, return_sequences=False))(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        out = layers.Dense(n_classes, activation='softmax')(x)

        model = models.Model(inputs=inp, outputs=out)
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def analyze(self):
        """
        Train (or load) the CRNN model and compute overall accuracy.
        Returns overall accuracy and label encoder for predictions.
        """
        print("Loading spectrogram dataset for CRNN...")
        X, y = load_cnn_dataset()
        if X.size == 0:
            print("No data found for CRNN.")
            return None, None

        le = LabelEncoder()
        y_enc = le.fit_transform(y)
        self.label_encoder = le

        X_train, X_test, y_train, y_test = train_test_split(
            X, y_enc, test_size=0.2, random_state=self.random_state, stratify=y_enc
        )

        input_shape = X_train.shape[1:]
        n_classes = len(le.classes_)

        model = self.build_model(input_shape, n_classes)
        model.summary()

        model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.1, verbose=2)

        y_pred = np.argmax(model.predict(X_test), axis=1)
        acc = accuracy_score(y_test, y_pred)
        self.overall_accuracy = acc

        print(f"CRNN Overall Accuracy: {acc}")
        print(classification_report(y_test, y_pred, target_names=le.classes_))

        self.model = model
        return acc, le

    def preprocess_audio(self, file_path):
        """
        Preprocess uploaded song into CRNN input.
        Returns processed spectrogram.
        """
        # Here we can assume load_cnn_dataset uses librosa or similar to produce spectrogram
        # For a single file:
        audio, sr = librosa.load(file_path, sr=None)
        # Compute Mel spectrogram (example)
        spect = librosa.feature.melspectrogram(audio, sr=sr, n_mels=N_MELS)
        # Resize / pad to FIXED_FRAMES
        if spect.shape[1] < FIXED_FRAMES:
            pad_width = FIXED_FRAMES - spect.shape[1]
            spect = np.pad(spect, ((0,0),(0,pad_width)), mode='constant')
        else:
            spect = spect[:, :FIXED_FRAMES]

        spect = spect[..., np.newaxis]  # add channel dim
        spect = np.expand_dims(spect, axis=0)  # add batch dim
        return spect

    def predict_user_song(self, file_path):
        """
        Predict uploaded song.
        Returns label and confidence.
        """
        if self.model is None or self.label_encoder is None:
            print("Model not trained. Call analyze() first.")
            return None, None

        X = self.preprocess_audio(file_path)
        probs = self.model.predict(X)[0]  # single sample
        pred_idx = np.argmax(probs)
        label = self.label_encoder.classes_[pred_idx]
        confidence = float(probs[pred_idx])
        return label, confidence
