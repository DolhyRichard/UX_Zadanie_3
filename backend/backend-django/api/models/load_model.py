from tensorflow.keras.models import load_model
import numpy as np

def load_cnn_model():
    model = load_model("saved_models/cnn_model.keras")
    classes = np.load("saved_models/label_encoder.npy", allow_pickle=True)
    return model, classes
