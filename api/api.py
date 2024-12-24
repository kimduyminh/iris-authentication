from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from .db_connection import get_connection
import cv2
import numpy as np
import tensorflow as tf
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Load trained model
MODEL_PATH = "./models/iris_authentication_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# Folder to store iris images
IRIS_IMAGE_FOLDER = "./iris_images"
os.makedirs(IRIS_IMAGE_FOLDER, exist_ok=True)

# Helper functions
def preprocess_image(image_path, target_size=(299, 299)):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.resize(image, target_size) / 255.0
    return np.expand_dims(image, axis=0)

def compare_iris(image1_path, image2_path):
    img1 = preprocess_image(image1_path)
    img2 = preprocess_image(image2_path)
    pred1 = model.predict(img1)
    pred2 = model.predict(img2)
    return np.argmax(pred1) == np.argmax(pred2)

# API routes
@app.route("/create-account", methods=["POST"])
def create_account():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    name = data.get("name")
    iris_right = request.files.get("iris_image_right")
    iris_left = request.files.get("iris_image_left")

    if not all([username, email, name, iris_right, iris_left]):
        return jsonify({"error": "Missing required fields"}), 400

    # Save iris images
    right_path = os.path.join(IRIS_IMAGE_FOLDER, secure_filename(f"{username}_right.jpg"))
    left_path = os.path.join(IRIS_IMAGE_FOLDER, secure_filename(f"{username}_left.jpg"))
    iris_right.save(right_path)
    iris_left.save(left_path)

    # Insert user into database
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, name, iris_image_right, iris_image_left)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, name, right_path, left_path))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Account created successfully"}), 201
    except Exception as e:
        logging.error(f"Error creating account for {username}: {e}")
        return jsonify({"error": "Failed to create account"}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.form
    username = data.get("username")
    iris_file = request.files.get("iris_image")

    if not all([username, iris_file]):
        return jsonify({"error": "Missing required fields"}), 400

    # Save temporary iris image
    temp_path = os.path.join(IRIS_IMAGE_FOLDER, "temp_iris.jpg")
    iris_file.save(temp_path)

    # Fetch user from database
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT iris_image_right, iris_image_left, email, name FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            os.remove(temp_path)
            return jsonify({"error": "User not found"}), 404

        right_path, left_path, email, name = user
        # Compare iris images
        if compare_iris(temp_path, right_path) or compare_iris(temp_path, left_path):
            os.remove(temp_path)
            return jsonify({"message": "Login successful", "email": email, "name": name}), 200
        else:
            os.remove(temp_path)
            return jsonify({"error": "Iris does not match"}), 403

    except Exception as e:
        logging.error(f"Error during login for {username}: {e}")
        return jsonify({"error": "Failed to login"}), 500

@app.route("/update-account", methods=["PUT"])
def update_account():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    name = data.get("name")
    iris_right = request.files.get("iris_image_right")
    iris_left = request.files.get("iris_image_left")

    if not username:
        return jsonify({"error": "Missing username"}), 400

    updates = []
    params = []

    if email:
        updates.append("email = %s")
        params.append(email)
    if name:
        updates.append("name = %s")
        params.append(name)
    if iris_right:
        right_path = os.path.join(IRIS_IMAGE_FOLDER, secure_filename(f"{username}_right_updated.jpg"))
        iris_right.save(right_path)
        updates.append("iris_image_right = %s")
        params.append(right_path)
    if iris_left:
        left_path = os.path.join(IRIS_IMAGE_FOLDER, secure_filename(f"{username}_left_updated.jpg"))
        iris_left.save(left_path)
        updates.append("iris_image_left = %s")
        params.append(left_path)

    if not updates:
        return jsonify({"error": "No updates provided"}), 400

    params.append(username)
    query = f"UPDATE users SET {', '.join(updates)} WHERE username = %s"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Account updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating account for {username}: {e}")
        return jsonify({"error": "Failed to update account"}), 500

@app.route("/delete-account", methods=["DELETE"])
def delete_account():
    data = request.form
    username = data.get("username")

    if not username:
        return jsonify({"error": "Missing username"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting account for {username}: {e}")
        return jsonify({"error": "Failed to delete account"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
