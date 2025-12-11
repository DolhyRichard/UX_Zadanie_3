import librosa
import numpy as np
from config import SAMPLE_RATE, N_MFCC

def extract_mfcc_from_song(path):
    y, sr = librosa.load(path, sr=SAMPLE_RATE)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    return mfcc[..., np.newaxis]
