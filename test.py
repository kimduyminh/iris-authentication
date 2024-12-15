import torch
print(torch.cuda.is_available())
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))

import tensorflow as tf

print("TensorFlow version:", tf.__version__)
print("Num GPUs Available:", len(tf.config.list_physical_devices('GPU')))
print("Available GPUs:", tf.config.list_physical_devices('GPU'))

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"  # Show detailed logs
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
