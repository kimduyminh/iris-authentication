import h5py
from tensorflow.keras.models import load_model

def inspect_h5_file(file_path):
    """
    Inspect the contents of an H5 file.
    """
    with h5py.File(file_path, "r", swmr=False) as f:
        print("\n=== Keys in the file ===")
        print(list(f.keys()))

        # Inspect Model Weights
        if "model_weights" in f.keys():
            print("\n=== Model Weights ===")
            model_weights = f["model_weights"]
            for layer_name in model_weights:
                print(f"Layer: {layer_name}")
                layer_group = model_weights[layer_name]
                for weight_name in layer_group:
                    weight_object = layer_group[weight_name]
                    if isinstance(weight_object, h5py.Dataset):
                        print(f"  Weight: {weight_name}, Shape: {weight_object.shape}")
                    elif isinstance(weight_object, h5py.Group):
                        print(f"  Sub-group: {weight_name}, Keys: {list(weight_object.keys())}")

        # Inspect Optimizer Weights
        if "optimizer_weights" in f.keys():
            print("\n=== Optimizer Weights ===")
            optimizer_weights = f["optimizer_weights"]
            for opt_key in optimizer_weights:
                group = optimizer_weights[opt_key]
                if isinstance(group, h5py.Dataset):
                    print(f"Optimizer Dataset: {opt_key}, Shape: {group.shape}")
                elif isinstance(group, h5py.Group):
                    print(f"Optimizer Group: {opt_key}, Keys: {list(group.keys())}")


def load_model_and_summary(file_path):
    """
    Load and summarize the Keras model.
    """
    print("\n=== Loading Model ===")
    try:
        model = load_model(file_path)
        print("\n=== Model Summary ===")
        model.summary()
    except Exception as e:
        print(f"Error loading model: {e}")


def main():
    file_path = "./iris_recognition_inceptionv3_gabor.h5"

    # Inspect the .h5 file for details
    print("Inspecting the H5 file...")
    inspect_h5_file(file_path)

    # Load the model and display its summary
    print("\nAttempting to load the model...")
    load_model_and_summary(file_path)


if __name__ == "__main__":
    main()

