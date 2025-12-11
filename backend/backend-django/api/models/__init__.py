# models/__init__.py

from .cnn import CNN
from .crnn import CRNN
from .svm import SVMClassifier
from .knn import KNNClassifier
from .random_forest import RandomForestModel

MODEL_REGISTRY = {
    "cnn": CNN,
    "crnn": CRNN,
    "svm": SVMClassifier,
    "knn": KNNClassifier,
    "rf": RandomForestModel,
}


def get_model(name: str):
    name = name.lower()
    if name not in MODEL_REGISTRY:
        raise ValueError(f"Model '{name}' not available. Choose one of {list(MODEL_REGISTRY.keys())}")
    return MODEL_REGISTRY[name]()
