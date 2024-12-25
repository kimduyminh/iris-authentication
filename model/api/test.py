import tensorflow as tf
import numpy as np
from PIL import Image
import io


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






#match, similarity = compare_images(model, img1_bytes, img2_bytes, threshold=0.5)

