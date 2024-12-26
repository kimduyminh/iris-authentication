import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

def load_model(model_path):
    try:
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")

def preprocess_image(image_bytes, target_size=(299, 299)):
    """
    Preprocess the input image bytes to match the model input format.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0  # Normalize to [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {e}")

def compare_images(model, image_bytes1, image_bytes2, threshold=0.2):
    """
    Compare two images by passing them one at a time through the model
    and calculating the similarity based on the outputs.
    """
    try:
        img1 = preprocess_image(image_bytes1)
        img2 = preprocess_image(image_bytes2)

        output1 = model.predict(img1, verbose=0)[0]
        output2 = model.predict(img2, verbose=0)[0]

        similarity = np.linalg.norm(output1 - output2)  # Euclidean distance
        is_match = similarity < threshold  # Match if similarity is below the threshold
        return is_match, similarity  # Return match status and similarity score
    except Exception as e:
        raise RuntimeError(f"Error comparing images: {e}")

def main(name):
    print("Loading model...")

    # Define directories and model path
    base_dir = r"C:\\Code\\Biometric\\iris-authentication\\database_images"
    captured_dir = r"C:\\Code\\Biometric\\iris-authentication\\captured"
    model_path = r"C:\\Code\\Biometric\\iris-authentication\\model\\iris_authentication_model.keras"

    # Load the model
    model = load_model(model_path)

    threshold = 0.001  # Updated threshold for match criteria
    user_folder = os.path.join(base_dir, name)

    if not os.path.exists(user_folder):
        raise FileNotFoundError(f"User folder '{user_folder}' not found.")

    # Get all image paths from the folders
    database_images = sorted(
        [os.path.join(user_folder, img) for img in os.listdir(user_folder) if img.endswith(".jpg")]
    )
    captured_images = sorted(
        [os.path.join(captured_dir, img) for img in os.listdir(captured_dir) if img.endswith(".jpg")]
    )

    if len(database_images) != 4 or len(captured_images) != 4:
        raise ValueError("Both folders must contain exactly 4 images.")

    correct_predictions = 0
    total_cases = 0
    print("Starting predictions...")

    # Compare all captured images with all database images
    for img1_path in captured_images:
        for img2_path in database_images:
            try:
                with open(img1_path, "rb") as f1, open(img2_path, "rb") as f2:
                    img1_bytes = f1.read()
                    img2_bytes = f2.read()

                match, similarity = compare_images(model, img1_bytes, img2_bytes, threshold)
                total_cases += 1

                if match:
                    correct_predictions += 1

                # Log the comparison result
                print(
                    f"Comparing {os.path.basename(img1_path)} with {os.path.basename(img2_path)}:\n"
                    f"Similarity Score: {similarity:.4f}\n"
                    f"Prediction: {'Match' if match else 'No Match'}\n"
                    f"{'-' * 50}"
                )
            except Exception as e:
                print(f"Error processing {img1_path} and {img2_path}: {e}")

    # Authentication decision
    print(f"Correct Predictions: {correct_predictions}/{total_cases}")
    return correct_predictions > 12  # Return True if at least 13 matches are found
