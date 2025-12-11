# main.py

from models import get_model

def print_menu():
    print("Choose a method for analyzing samples:")
    print("1 = CNN")
    print("2 = CRNN")
    print("3 = SVM")
    print("4 = k-NN")
    print("5 = Random Forest")
    print("6 = Predict using existing models")
    print("q = quit")

choice_map = {
    "1": "cnn",
    "2": "crnn",
    "3": "svm",
    "4": "knn",
    "5": "rf"
}

if __name__ == "__main__":
    print_menu()
    choice = input("Your choice: ").strip()
    if choice.lower() == "q":
        print("Bye.")
        exit()

    if choice == "6":
        print("\nLoading all trained models...\n")

        loaded_models = {}
        for key, name in choice_map.items():
            try:
                model = get_model(name, load_trained=True)
                loaded_models[name] = model
                print(f"Loaded {name.upper()}")
            except Exception as e:
                print(f"{name.upper()} not loaded: {e}")

        if not loaded_models:
            print("No models available. Train first.")
            exit()
            # let user choose model to predict
        print("\nAvailable models:")
        for name in loaded_models:
            print(f"- {name}")

        chosen = input("\nChoose model for prediction: ").strip().lower()
        if chosen not in loaded_models:
            print("Invalid selection.")
            exit()

        file_path = input("Enter path to your audio file: ").strip()
        loaded_models[chosen].predict_user_song(file_path)
        exit()

    model_key = choice_map.get(choice)
    if not model_key:
        print("Invalid selection.")
        exit()

    model = get_model(model_key)
    print(f"Initialized model: {model.__class__.__name__}")
    model.analyze()
