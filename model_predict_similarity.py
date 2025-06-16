from PIL import Image
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
import imagehash
import io

def extract_image_features(image: Image.Image) -> np.ndarray:
    """
    Convert image to grayscale hash vector for similarity comparison.
    """
    hash_val = imagehash.phash(image)
    return np.array(hash_val.hash, dtype=np.float32).flatten().reshape(1, -1)

def predict_by_similarity(uploaded_image: Image.Image, dataset_folder: str) -> tuple[str, float]:
    """
    Compare uploaded image to images in dataset folder using hash similarity.
    """
    uploaded_features = extract_image_features(uploaded_image)

    best_score = -1
    best_label = "Tidak diketahui"

    for label_folder in os.listdir(dataset_folder):
        label_path = os.path.join(dataset_folder, label_folder)
        if not os.path.isdir(label_path):
            continue

        for fname in os.listdir(label_path):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(label_path, fname)
                try:
                    img = Image.open(img_path).convert("RGB")
                    img_features = extract_image_features(img)
                    score = cosine_similarity(uploaded_features, img_features)[0][0]
                    if score > best_score:
                        best_score = score
                        best_label = label_folder
                except Exception as e:
                    continue

    return best_label, float(best_score)
