import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

def split_data(base_folder):
    image_paths = []
    labels = []

    # Gather all images and labels
    for folder_index in range(0, 1000):
        folder_path = os.path.join(base_folder, f"{folder_index:03d}")
        if not os.path.exists(folder_path):
            continue
        for image_name in os.listdir(folder_path):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image_paths.append(os.path.join(folder_path, image_name))
                labels.append(folder_index)

    # Split into train and validation sets
    train_paths, val_paths, train_labels, val_labels = train_test_split(image_paths, labels, test_size=0.3, random_state=42)
    return train_paths, val_paths, train_labels, val_labels

def data_generator(image_paths, labels, batch_size=8, target_size=(299, 299)):
    while True:
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i+batch_size]
            batch_labels = labels[i:i+batch_size]
            images = []
            for image_path in batch_paths:
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                if image is not None:
                    image = cv2.resize(image, target_size) / 255.0
                    images.append(image)
            yield np.array(images), np.array(batch_labels)

def configure_gpu_memory(limit_gb=7):
    """
    Configure TensorFlow to limit GPU memory usage.
    """
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_virtual_device_configuration(
                    gpu,
                    [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=limit_gb * 1024)]
                )
            print(f"GPU memory limited to {limit_gb} GB")
        except RuntimeError as e:
            print(f"Error configuring GPU memory: {e}")

def image_data_generator(base_folder, batch_size=8, target_size=(299, 299)):
    folder_indices = [f"{i:03d}" for i in range(0, 1000)]
    while True:
        for folder_index in folder_indices:
            folder_path = os.path.join(base_folder, folder_index)
            if not os.path.exists(folder_path):
                continue
            images, labels = [], []
            for image_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_name)
                if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    continue

                # Load and preprocess image
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                if image is None:
                    print(f"Could not load image: {image_path}")
                    continue
                image = cv2.resize(image, target_size) / 255.0
                images.append(image)
                labels.append(int(folder_index))

                if len(images) == batch_size:
                    print(f"Batch sample: {labels}")  # Verify batch labels
                    yield np.array(images), np.array(labels)
                    images, labels = [], []

def build_inceptionv3_model(input_shape, num_classes):
    """
    Build the InceptionV3-based model for classification.
    """
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # Freeze base layers

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.0001),  # Lower learning rate
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def main():
    from timeit import default_timer as timer
    start = timer()
    configure_gpu_memory(limit_gb=7)

    base_folder = "./feature_image/gabor_filter"
    batch_size = 8

    # Split data into train and validation sets
    train_paths, val_paths, train_labels, val_labels = split_data(base_folder)

    # Build the model
    input_shape = (299, 299, 3)
    num_classes = len(np.unique(train_labels))
    model = build_inceptionv3_model(input_shape, num_classes)

    # Training and validation generators
    train_generator = data_generator(train_paths, train_labels, batch_size=batch_size)
    val_generator = data_generator(val_paths, val_labels, batch_size=batch_size)

    print("Training the model...")
    history = model.fit(
        train_generator,
        steps_per_epoch=len(train_paths) // batch_size,
        validation_data=val_generator,
        validation_steps=len(val_paths) // batch_size,
        epochs=100  # Increased epochs
    )

    # Save the trained model
    model_output_path = "./iris_recognition_inceptionv3_gabor.h5"
    model.save(model_output_path)
    print(f"Model saved to {model_output_path}")
    end = timer()
    print("Finished in "+str(end-start)+"s")

if __name__ == "__main__":
    main()
