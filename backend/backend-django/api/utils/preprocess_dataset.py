# utils/preprocess_dataset.py

import os
import numpy as np
import librosa
from config import GENRES_PATH, GENRES, SAMPLE_RATE, N_MFCC, DURATION, PROCESSED_PATH
from tqdm import tqdm

SEGMENTS = 3
SEGMENT_DURATION = 10  # seconds

def preprocess_and_save():
    X, y, track_ids = [], [], []

    os.makedirs(PROCESSED_PATH, exist_ok=True)

    for genre in GENRES:
        folder = os.path.join(GENRES_PATH, genre)
        for filename in tqdm(os.listdir(folder), desc=f"Processing {genre}"):
            if not (filename.endswith(".wav") or filename.endswith(".au")):
                continue
            file_path = os.path.join(folder, filename)
            y_track, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

            step = (DURATION - SEGMENT_DURATION) / max(SEGMENTS - 1, 1)
            for i in range(SEGMENTS):
                start = int(i * step * sr)
                end = int(start + SEGMENT_DURATION * sr)
                segment = y_track[start:end]
                if len(segment) < SEGMENT_DURATION * sr:
                    segment = np.pad(segment, (0, int(SEGMENT_DURATION * sr) - len(segment)))

                mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=N_MFCC)
                mfcc = mfcc[..., np.newaxis]  # add channel dimension

                X.append(mfcc)
                y.append(genre)
                track_ids.append(filename)

    X = np.array(X)
    y = np.array(y)
    track_ids = np.array(track_ids)

    # save arrays
    np.save(os.path.join(PROCESSED_PATH, "X.npy"), X)
    np.save(os.path.join(PROCESSED_PATH, "y.npy"), y)
    np.save(os.path.join(PROCESSED_PATH, "track_ids.npy"), track_ids)
    print(f"Saved {len(X)} segments to {PROCESSED_PATH}")

if __name__ == "__main__":
    preprocess_and_save()
