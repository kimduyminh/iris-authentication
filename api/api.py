# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import io
# import os
#
# def load_model(model_path):
#     return tf.keras.models.load_model(model_path)
#
# def preprocess_image(image_bytes, target_size=(299, 299)):
#     """
#     Preprocess the input image bytes to match the model input format.
#     """
#     img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#     img = img.resize(target_size)
#     img_array = np.array(img) / 255.0  # Normalize to [0, 1]
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     return img_array
#
# def compare_images(model, image_bytes1, image_bytes2, threshold=0.5):
#     """
#     Compare two images by passing them one at a time through the model
#     and calculating the similarity based on the outputs.
#
#     Args:
#         model: The loaded TensorFlow model.
#         image_bytes1: The first image in byte format.
#         image_bytes2: The second image in byte format.
#         threshold: Threshold for considering the outputs as a match.
#
#     Returns:
#         True if the outputs are similar (within the threshold), False otherwise.
#     """
#     # Preprocess each image
#     img1 = preprocess_image(image_bytes1)
#     img2 = preprocess_image(image_bytes2)
#
#     # Get predictions for each image
#     output1 = model.predict(img1)[0]  # Prediction for the first image
#     output2 = model.predict(img2)[0]  # Prediction for the second image
#
#     # Compare the outputs (e.g., cosine similarity, Euclidean distance, etc.)
#     similarity = np.linalg.norm(output1 - output2)  # Euclidean distance
#     print(f"Similarity score: {similarity}")
#
#     # If similarity is below the threshold, consider the images as a match
#     return similarity < threshold
#
# if __name__ == "__main__":
#     model_path = r"./iris_authentication_model.keras"
#     model = load_model(model_path)
#
#     # Test with two images
#     with open(r".\processed_image\000\S6000S00.jpg", "rb") as f1, \
#          open(r".\processed_image\001\S6001S03.jpg", "rb") as f2:
#         image_bytes1 = f1.read()
#         image_bytes2 = f2.read()
#         result = compare_images(model, image_bytes1, image_bytes2, threshold=0.5)
#         print("Images Match:" if result else "Images Do Not Match")
#

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


# def generate_test_cases(base_dir):
#     """
#     Generate test cases by iterating through the directory and pairing images.
#     """
#     test_cases = []
#     for person_id, files in itertools.groupby(sorted(os.listdir(base_dir)), key=lambda x: x[:3]):
#         files = list(files)
#         # Test cases for the same person
#         same_person_pairs = list(itertools.combinations(files, 2))
#         test_cases.extend([(os.path.join(base_dir, person_id, f1), os.path.join(base_dir, person_id, f2), True)
#                            for f1, f2 in same_person_pairs])
#
#     # Test cases for different people
#     person_dirs = [os.path.join(base_dir, d) for d in sorted(os.listdir(base_dir))]
#     for d1, d2 in itertools.combinations(person_dirs, 2):
#         file1 = os.path.join(d1, sorted(os.listdir(d1))[0])
#         file2 = os.path.join(d2, sorted(os.listdir(d2))[0])
#         test_cases.append((file1, file2, False))
#
#     return test_cases


# if __name__ == "__main__":
#     base_dir = "./processed_image"
#     model_path = r"./iris_authentication_model.keras"
#     result_file = "comparison_results.txt"
#     model = load_model(model_path)
#
#     test_cases = generate_test_cases(base_dir)
#     test_cases = test_cases[:15]  # Limit to 15 test cases
#
#     with open(result_file, "w") as file:
#         for idx, (img1_path, img2_path, expected_match) in enumerate(test_cases):
#             with open(img1_path, "rb") as f1, open(img2_path, "rb") as f2:
#                 img1_bytes = f1.read()
#                 img2_bytes = f2.read()
#                 match, similarity = compare_images(model, img1_bytes, img2_bytes, threshold=0.5)
#                 result = (
#                     f"Test Case {idx + 1}:\n"
#                     f"Image 1: {img1_path}\n"
#                     f"Image 2: {img2_path}\n"
#                     f"Expected Match: {expected_match}\n"
#                     f"Similarity: {similarity}\n"
#                     f"Result: {'Match' if match else 'No Match'}\n"
#                     f"{'-' * 50}\n"
#                 )
#                 file.write(result)
#                 print(result)
#
#     print(f"Results saved to {result_file}")

def generate_true_test_cases(base_dir):
    """
    Generate test cases where images are from the same folder and person.
    These are expected to produce a 'true' match output.
    """
    test_cases = []
    # Iterate through each folder
    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):  # Ensure it's a directory
            images = sorted([img for img in os.listdir(folder_path) if img.startswith("S6")])
            # Create all combinations of image pairs within the folder
            same_person_pairs = list(itertools.combinations(images, 2))
            test_cases.extend([
                (os.path.join(folder_path, img1), os.path.join(folder_path, img2), True)
                for img1, img2 in same_person_pairs
            ])
    return test_cases


if __name__ == "__main__":
    base_dir = "./processed_image"
    true_test_cases = generate_true_test_cases(base_dir)

    # Save to a text file
    result_file = "true_test_cases.txt"
    with open(result_file, "w") as file:
        for idx, (img1_path, img2_path, expected_match) in enumerate(true_test_cases):
            result = f"Test Case {idx + 1}:\nImage 1: {img1_path}\nImage 2: {img2_path}\nExpected Match: {expected_match}\n{'-' * 50}\n"
            file.write(result)

    print(f"True test cases saved to {result_file}")