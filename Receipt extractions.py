import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Path to your receipt images
data_dir = 'path_to_receipt_images'
img_size = 128  # You can adjust this size as needed

def load_data(data_dir):
    images = []
    for img_name in os.listdir(data_dir):
        img_path = os.path.join(data_dir, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Load in grayscale
        img = cv2.resize(img, (img_size, img_size))  # Resize to a consistent size
        images.append(img)
    return np.array(images)

# Load images
images = load_data(data_dir)

# Normalize images
images = images / 255.0

# Reshape for the CNN input (add channel dimension)
images = images.reshape(-1, img_size, img_size, 1)

print(f"Loaded {images.shape[0]} images with shape {images.shape[1:]}")