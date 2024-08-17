import os
import cv2
import numpy as np

# Constants
IMG_SIZE = 224  # Vision Transformers typically use 224x224 images

def load_and_preprocess_data(data_dir):
    images = []
    for img_name in os.listdir(data_dir):
        img_path = os.path.join(data_dir, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))  # Resize image to 224x224
        images.append(img)
    images = np.array(images) / 255.0  # Normalize images
    return images

if __name__ == "__main__":
    DATA_DIR = 'data/train/'
    images = load_and_preprocess_data(DATA_DIR)
    print(f"Loaded {images.shape[0]} images with shape {images.shape[1:]}")
