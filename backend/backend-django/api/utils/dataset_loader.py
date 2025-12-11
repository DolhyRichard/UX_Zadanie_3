# utils/dataset_loader.py
import librosa
import os
import numpy as np
from tqdm import tqdm
from config import GENRES, GENRES_PATH, SAMPLE_RATE, N_MFCC, DURATION
from .preprocess import extract_feature_vector, extract_log_mel_spectrogram


def load_classical_dataset():
    """
    Load classical features (1D vectors) for all genres.
    Returns X (n_samples, n_features) and y (n_samples,)
    """

    X, y = [], []
    for genre in GENRES:
        folder = os.path.join(GENRES_PATH, genre)
        if not os.path.isdir(folder):
            print(folder)
            continue
        for filename in tqdm(os.listdir(folder), desc=f"Loading {genre}"):
            if filename.lower().endswith('.au'):
                fp = os.path.join(folder, filename)
                feat = extract_feature_vector(fp)
                if feat is None:
                    continue
                X.append(feat)
                y.append(genre)
    if len(X) == 0:
        return np.array([]), np.array([])
    return np.vstack(X), np.array(y)


import numpy as np
from config import PROCESSED_PATH

def load_cnn_dataset():
    try:
        X = np.load(f"{PROCESSED_PATH}/X.npy")
        y = np.load(f"{PROCESSED_PATH}/y.npy")
        track_ids = np.load(f"{PROCESSED_PATH}/track_ids.npy")
        return X, y, track_ids
    except FileNotFoundError:
        print("Preprocessed dataset not found. Run preprocess_dataset.py first.")
        return np.array([]), np.array([]), np.array([])
