from tensorflow.keras.models import load_model
from tensorflow.keras import layers, models
import numpy as np
from ..utils.extract_mfcc import extract_mfcc_from_song

def retrain_with_new_song(model_path, label_path, song_path, new_label, threshold=0.90):
    # Load model + classes
    model = load_model(model_path)
    classes = np.load(label_path, allow_pickle=True)

    # Add class if new
    if new_label not in classes:
        classes = np.append(classes, new_label)

    # Convert to index
    label_index = np.where(classes == new_label)[0][0]

    # Extract MFCC
    X_new = extract_mfcc_from_song(song_path)
    X_new = np.expand_dims(X_new, axis=0)
    y_new = np.array([label_index])

    # Freeze convolution layers
    for layer in model.layers[:-3]:
        layer.trainable = False

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    # Retrain only the classification head
    history = model.fit(X_new, y_new, epochs=20, verbose=0)

    # Check threshold
    last_acc = history.history['accuracy'][-1]
    print("Fine-tuning accuracy:", last_acc)

    # Save updated model + classes
    model.save(model_path)
    np.save(label_path, classes)

    return last_acc
