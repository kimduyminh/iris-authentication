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
os.environ["OMP_NUM_THREADS"] = "6"
os.environ["TF_NUM_INTRAOP_THREADS"] = "6"
os.environ["TF_NUM_INTEROP_THREADS"] = "2"  # Adjust inter-op threads for better balance
print("Intra-op threads:", tf.config.threading.get_intra_op_parallelism_threads())
print("Inter-op threads:", tf.config.threading.get_inter_op_parallelism_threads())

print(tf.config.list_physical_devices('GPU'))
