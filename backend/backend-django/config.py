# GLOBAL PATHS
DATA_PATH = "../data/"
GENRES_PATH = "../data/genres/"  # expects subfolders per genre, e.g. data/genres/blues/*.au
RAW_AUDIO_PATH = "../data/raw/"
PROCESSED_PATH = "../data/processed/"
MODEL_SAVE_PATH = "saved_models/"

GENRES = [
    'blues',
    'classical',
    'country',
    'disco',
    'hiphop',
    'jazz',
    'metal',
    'pop',
    'reggae',
    'rock'
]

# AUDIO PARAMETERS
SAMPLE_RATE = 22050
N_MFCC = 40
HOP_LENGTH = 512
N_FFT = 2048
DURATION = 30  # seconds to load from each track

# MEL/SPECTROGRAM (for CNN/CRNN)
N_MELS = 128
FIXED_FRAMES = 128  # number of time frames to pad/truncate to for spectrograms

# TRAINING DEFAULTS
TRAIN_TEST_SPLIT = 0.2   # test size
BATCH_SIZE = 32
EPOCHS = 50

# RANDOM SEED
RANDOM_SEED = 42
