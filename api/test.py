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
    return similarity < threshold, similarity  # Return match status and similarity score


def generate_true_test_cases(base_dir, limit=20):
    """
    Generate test cases where images are from the same folder and person.
    """
    test_cases = []
    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            images = sorted([img for img in os.listdir(folder_path) if img.startswith("S6")])
            cases = [
                (os.path.join(folder_path, img1), os.path.join(folder_path, img2), True)
                for img1, img2 in itertools.combinations(images, 2)
            ]
            test_cases.extend(cases)
    return test_cases[:limit]


def generate_false_test_cases(base_dir, limit=20):
    """
    Generate test cases where images are from different folders (different people).
    """
    test_cases = []
    folders = sorted(os.listdir(base_dir))
    for folder1, folder2 in itertools.combinations(folders, 2):
        folder1_path = os.path.join(base_dir, folder1)
        folder2_path = os.path.join(base_dir, folder2)
        if os.path.isdir(folder1_path) and os.path.isdir(folder2_path):
            img1 = os.path.join(folder1_path, sorted(os.listdir(folder1_path))[0])
            img2 = os.path.join(folder2_path, sorted(os.listdir(folder2_path))[0])
            test_cases.append((img1, img2, False))
    return test_cases[:limit]


if __name__ == "__main__":
    base_dir = "./processed_image"
    model_path = r"./iris_authentication_model.keras"
    result_file = "test_results.txt"
    model = load_model(model_path)

    true_test_cases = generate_true_test_cases(base_dir, limit=20)
    false_test_cases = generate_false_test_cases(base_dir, limit=20)

    all_test_cases = true_test_cases + false_test_cases
    correct_predictions = 0
    total_cases = len(all_test_cases)

    with open(result_file, "w") as file:
        for idx, (img1_path, img2_path, expected_match) in enumerate(all_test_cases):
            with open(img1_path, "rb") as f1, open(img2_path, "rb") as f2:
                img1_bytes = f1.read()
                img2_bytes = f2.read()
                match, similarity = compare_images(model, img1_bytes, img2_bytes, threshold=0.5)
                is_correct = match == expected_match
                if is_correct:
                    correct_predictions += 1

                result = (
                    f"Test Case {idx + 1}:\n"
                    f"Image 1: {img1_path}\n"
                    f"Image 2: {img2_path}\n"
                    f"Expected Match: {expected_match}\n"
                    f"Similarity Score: {similarity:.4f}\n"
                    f"Prediction: {'Match' if match else 'No Match'}\n"
                    f"Correct Prediction: {is_correct}\n"
                    f"{'-' * 50}\n"
                )
                file.write(result)
                print(result)

    # Calculate and display accuracy
    accuracy = (correct_predictions / total_cases) * 100 if total_cases > 0 else 0
    print(f"Correct Predictions: {correct_predictions}/{total_cases}")
    print(f"Accuracy: {accuracy:.2f}%")
    with open(result_file, "a") as file:
        file.write(f"Correct Predictions: {correct_predictions}/{total_cases}\n")
        file.write(f"Accuracy: {accuracy:.2f}%\n")

    print(f"Results saved to {result_file}")
