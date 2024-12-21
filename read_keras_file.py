import tensorflow as tf
import cv2

# Path to the saved model
model_path = "./models/iris_authentication_model.keras"

# Load the Keras model
model = tf.keras.models.load_model(model_path)

# Print model summary
model.summary()

# Optionally, test the model with some input data
import numpy as np

# Example input (assuming the model input shape is (224, 224, 3))
# Example input data resized to match model input shape
input_data = np.random.random((1, 224, 224, 3))  # Initial shape (224, 224)
input_data_resized = np.array([cv2.resize(img, (299, 299)) for img in input_data])  # Resize to (299, 299)

predictions = model.predict(input_data_resized)
print("Predictions:", predictions)
