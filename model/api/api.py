import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import itertools


def load_model(model_path):
    return tf.keras.models.load_model(model_path)


def preprocess_image(image_bytes, target_size=(299, 299)):
    """
    Preprocess the input image bytes to match the model input format.
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0  # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array


def compare_images(model, image_bytes1, image_bytes2, threshold=0.5):
    """
    Compare two images by passing them one at a time through the model
    and calculating the similarity based on the outputs.
    """
    img1 = preprocess_image(image_bytes1)
    img2 = preprocess_image(image_bytes2)

    output1 = model.predict(img1)[0]
    output2 = model.predict(img2)[0]

    similarity = np.linalg.norm(output1 - output2)  # Euclidean distance
    return similarity < threshold, similarity  # Return match status and score

#match, similarity = compare_images(model, img1_bytes, img2_bytes, threshold=0.5)

def main(name):
    base_dir = "./database_images"
    captured_dir = "./captured"
    model_path = r"./model/iris_authentication_model.keras"
    model = load_model(model_path)
    correct_predictions = 0
    total_cases = 0
    threshold = 0.5  # Similarity threshold for matching

    # Ensure the target user's folder exists
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

    # Ensure both folders have 4 images each
    if len(database_images) != 4 or len(captured_images) != 4:
        raise ValueError("Both folders must contain exactly 4 images.")

    # Compare all captured images with all database images
    for img1_path in captured_images:
        for img2_path in database_images:
            with open(img1_path, "rb") as f1, open(img2_path, "rb") as f2:
                img1_bytes = f1.read()
                img2_bytes = f2.read()
                match, similarity = compare_images(model, img1_bytes, img2_bytes, threshold)
                total_cases += 1
                if match:
                    correct_predictions += 1

                # Optional: Log the comparison result (can be removed in production)
                print(
                    f"Comparing {img1_path} with {img2_path}:\n"
                    f"Similarity Score: {similarity:.4f}\n"
                    f"Prediction: {'Match' if match else 'No Match'}\n"
                    f"{'-' * 50}"
                )

    # Authentication decision
    print(f"Correct Predictions: {correct_predictions}/{total_cases}")
    return correct_predictions > 12