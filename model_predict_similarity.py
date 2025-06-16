from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from feature_extraction import extract_features
import imagehash
import io
import os


def extract_image_features(image: Image.Image) -> np.ndarray:
    """
    Convert image to grayscale hash vector for similarity comparison.
    """
    hash_val = imagehash.phash(image)
    return np.array(hash_val.hash, dtype=np.float32).flatten().reshape(1, -1)


def predict_by_similarity(image_file, features_db: np.ndarray, paths_db: list[str]) -> tuple[str, float]:
    """
    Predict the label of the uploaded image by comparing it to the database of features.
    """

    uploaded_image = Image.open(image_file).convert("RGB")
    uploaded_feature = extract_features(uploaded_image)
    uploaded_feature = uploaded_feature.reshape(1, -1) 
    similarities = cosine_similarity(uploaded_feature, features_db)[0]
    best_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_idx])

    # Ekstrak label dari path
    best_path = paths_db[best_idx]
    label = os.path.basename(os.path.dirname(best_path))

    return label, best_score * 100
