import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

# -------------------------------
# 1. Data Preparation
# -------------------------------
def load_images_and_labels(base_folder, target_size=(299, 299)):
    """
    Load images from subfolders and prepare them with corresponding labels.
    """
    image_paths = []
    labels = []

    for folder_index in range(0, 1000):
        folder_path = os.path.join(base_folder, f"{folder_index:03d}")
        if not os.path.exists(folder_path):
            continue
        for image_name in os.listdir(folder_path):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(folder_path, image_name))
                labels.append(folder_index)
    return train_test_split(image_paths, labels, test_size=0.2, random_state=42)

def preprocess_image(image_path, target_size=(299, 299)):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.resize(image, target_size) / 255.0
    return image

def data_generator(image_paths, labels, batch_size=8, target_size=(299, 299)):
    while True:
        for i in range(0, len(image_paths), batch_size):
            batch_images = [preprocess_image(p, target_size) for p in image_paths[i:i+batch_size]]
            yield np.array(batch_images), np.array(labels[i:i+batch_size])

# -------------------------------
# 2. Build Model
# -------------------------------
def build_embedding_model(input_shape=(299, 299, 3)):
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # Freeze the base model

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu', name='embedding_layer'),
        layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1))  # Normalize embeddings
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# -------------------------------
# 3. Train and Save the Model
# -------------------------------
def main():
    base_folder = "./dataset"  # Dataset path
    model_output_path = "./models/iris_authentication_model.h5"

    # Load and split data
    train_paths, val_paths, train_labels, val_labels = load_images_and_labels(base_folder)
    print(f"Training samples: {len(train_paths)}, Validation samples: {len(val_paths)}")

    # Create data generators
    batch_size = 8
    train_gen = data_generator(train_paths, train_labels, batch_size)
    val_gen = data_generator(val_paths, val_labels, batch_size)
    epochs=1000

    # Build and train the model
    model = build_embedding_model()
    model.fit(train_gen,
              steps_per_epoch=len(train_paths) // batch_size,
              validation_data=val_gen,
              validation_steps=len(val_paths) // batch_size,
              epochs=epochs)

    # Save the model
    model.save(model_output_path)
    print(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    main()
