# Description: This script is used to run inference on a TensorFlow model using a SavedModel.
# The model takes two inputs: a dense tensor and an image tensor.
# The dense tensor is used to represent microphone data, and the image tensor is used to represent a spectrogram image.


import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array


def load_and_preprocess_image(image_path, target_size):
    """Load and preprocess an image for the model."""
    img = load_img(image_path, color_mode='grayscale', target_size=target_size)
    img = img_to_array(img)
    img = np.repeat(img, 4, axis=-1)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalize
    return img


def load_saved_model(model_dir):
    """Load Tims model from the given directory."""
    model = tf.saved_model.load(model_dir)
    return model


def run_inference(model, dense_data, image_data):
    """Run inference using the loaded model."""
    inputs = {
        'dense_input': tf.constant(dense_data, dtype=tf.float32),
        'input_1': tf.constant(image_data, dtype=tf.float32)
    }
    return model.signatures['serving_default'](**inputs)


model_dir = 'model'
model = load_saved_model(model_dir)

# Paths to images
image_paths = ['8000.png', '8001.png', '8002.png']

# Expect this to be microphone data but random data is used for demonstration
dense_data = np.random.normal(size=(1, 8)).astype(np.float32)

# Predict each image
for image_path in image_paths:
    img_data = load_and_preprocess_image(image_path, target_size=(128, 128))
    predictions = run_inference(model, dense_data, img_data)

    print(f"Predictions for {image_path}: {predictions['dense_6'].numpy()}")
