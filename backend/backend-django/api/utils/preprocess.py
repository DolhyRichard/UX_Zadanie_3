# utils/preprocess.py

import numpy as np
import librosa
from config import (
    SAMPLE_RATE,
    N_MFCC,
    HOP_LENGTH,
    N_FFT,
    DURATION,
    N_MELS,
    FIXED_FRAMES
)


def extract_feature_vector(file_path):
    """
    Return 1D feature vector (classical features) for classical ML models:
      - mean MFCC (N_MFCC)
      - mean chroma (12)
      - mean spectral_contrast (7)
    """
    y, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)
    if y is None or y.size == 0:
        return None

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC,
                                hop_length=HOP_LENGTH, n_fft=N_FFT)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=HOP_LENGTH)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=HOP_LENGTH)

    # mean over time axis -> feature vectors
    feat = np.hstack([
        np.mean(mfcc, axis=1),
        np.mean(chroma, axis=1),
        np.mean(contrast, axis=1)
    ])
    return feat


def extract_log_mel_spectrogram(file_path):
    """
    Return a fixed-size log-mel spectrogram (N_MELS x FIXED_FRAMES).
    Pads or truncates in time dimension to FIXED_FRAMES.
    """

    y, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)
    if y is None or y.size == 0:
        # return zeros so caller can handle shape consistently
        return np.zeros((N_MELS, FIXED_FRAMES), dtype=np.float32)

    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=N_MELS, hop_length=HOP_LENGTH, n_fft=N_FFT
    )
    # convert to log
    log_mel = librosa.power_to_db(mel, ref=np.max)

    # fix time dimension (columns)
    if log_mel.shape[1] < FIXED_FRAMES:
        # pad
        pad_width = FIXED_FRAMES - log_mel.shape[1]
        log_mel = np.pad(log_mel, ((0, 0), (0, pad_width)), mode='constant')
    else:
        # truncate
        log_mel = log_mel[:, :FIXED_FRAMES]

    return log_mel.astype(np.float32)
