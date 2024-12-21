import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras import layers, models, optimizers, callbacks
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
    return train_test_split(image_paths, labels, test_size=0.3, random_state=42) #30% testing

def preprocess_image(image_path, target_size=(299, 299)):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.resize(image, target_size) / 255.0
    return image

def data_generator(image_paths, labels, batch_size=4, target_size=(299, 299)):
    while True:
        for i in range(0, len(image_paths), batch_size):
            batch_images = [preprocess_image(p, target_size) for p in image_paths[i:i+batch_size]]
            yield np.array(batch_images), np.array(labels[i:i+batch_size])

# -------------------------------
# 2. Build Model
# -------------------------------
def build_embedding_model(input_shape=(299, 299, 3), num_classes=1000):
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = True  # Allow fine-tuning

    # Freeze the first few layers (e.g., first 150 layers)

    # Lower the layers to 10-50 (rec 50 but gtx1650 mobile can't do it)
    for layer in base_model.layers[:75]:
        layer.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),  # Add dropout to prevent overfitting
        layers.BatchNormalization(),  # Normalize activations
        layers.Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)), #Added kernel_regularizer
        layers.Dropout(0.4), # Increase to 0.4 maybe ?
        layers.Dense(num_classes, activation='softmax')  # Output layer
    ])

    optimizer = optimizers.Adam(learning_rate=0.0001, clipnorm=1.0)  # Adjust learning rate
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# -------------------------------
# 3. Train and Save the Model
# -------------------------------
class CustomEarlyStopping(callbacks.Callback):
    def __init__(self, patience=5, threshold=0.99999):
        super().__init__()
        self.patience = patience
        self.threshold = threshold
        self.counter = 0

    def on_epoch_end(self, epoch, logs=None):
        val_acc = logs.get('val_accuracy')
        if val_acc is not None and val_acc >= self.threshold:
            self.counter += 1
            if self.counter >= self.patience:
                print(
                    f"\nStopping early as validation accuracy remained above {self.threshold} for {self.patience} epochs.")
                self.model.stop_training = True
        else:
            self.counter = 0


def main():
    base_folder = "./feature_image/gabor_filter"  # Dataset path
    model_output_path = "./models/iris_authentication_model.keras"
    log_file_path = "./logs/iris_authentication_log.txt"

    # Load and split data
    train_paths, val_paths, train_labels, val_labels = load_images_and_labels(base_folder)
    print(f"Training samples: {len(train_paths)}, Validation samples: {len(val_paths)}")

    # Create data generators
    batch_size = 4 # Adjust this to 8-16 if possible (VRAM) for more speed
    train_gen = data_generator(train_paths, train_labels, batch_size)
    val_gen = data_generator(val_paths, val_labels, batch_size)

    # Build and train the model
    model = build_embedding_model()

    # Add callbacks for tuning
    checkpoint = callbacks.ModelCheckpoint(
        filepath=model_output_path, save_best_only=True, monitor='val_accuracy', mode='max'
    )

    # Old early_stopping
    early_stopping = callbacks.EarlyStopping(
        patience=5, restore_best_weights=True, monitor='val_loss'
    )

    lr_scheduler = callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.5, patience=3, verbose=1
    )

    # ChatGPT 360k/tháng early_stopping
    custom_early_stopping = CustomEarlyStopping(patience=5, threshold=0.99999)

    epochs = 1000 # Can run up to 1000 or more (the more epochs the more accurate)
    history = model.fit(
        train_gen,
        steps_per_epoch=len(train_paths) // batch_size,
        validation_data=val_gen,
        validation_steps=len(val_paths) // batch_size,
        epochs=epochs,
        callbacks=[checkpoint, custom_early_stopping, lr_scheduler]
    )

    # Save training details to a text file for easier reading
    with open(log_file_path, "w") as log_file:
        log_file.write(f"{'Epoch':<10}{'Train Acc':<15}{'Val Acc':<15}{'Train Loss':<15}{'Val Loss':<15}\n")
        log_file.write("=" * 60 + "\n")
        for epoch, (train_acc, val_acc, train_loss, val_loss) in enumerate(
                zip(history.history['accuracy'], history.history['val_accuracy'],
                    history.history['loss'], history.history['val_loss'])
        ):
            log_file.write(f"{epoch + 1:<10}{train_acc:<15.4f}{val_acc:<15.4f}{train_loss:<15.4f}{val_loss:<15.4f}\n")

        avg_train_acc = np.mean(history.history['accuracy'])
        avg_val_acc = np.mean(history.history['val_accuracy'])
        log_file.write("\n")
        log_file.write(f"Average Training Accuracy: {avg_train_acc:.4f}\n")
        log_file.write(f"Average Validation Accuracy: {avg_val_acc:.4f}\n")

    print(f"Training details saved to {log_file_path}")

    # Save the final model
    model.save(model_output_path)
    print(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    main()
