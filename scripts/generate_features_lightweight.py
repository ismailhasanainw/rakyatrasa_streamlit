# scripts/generate_features_lightweight.py
import os
import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

# === SETTING ===
DATASET_DIR = "dataset/train/images"
OUTPUT_FEATURES = "dataset/features.npy"
OUTPUT_PATHS = "dataset/paths.pkl"

# === READ FILE PATHS ===
image_paths = []
for root, _, files in os.walk(DATASET_DIR):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            image_paths.append(os.path.join(root, file))

# === IMAGE TO TEXT FEATURES (Simulasi TF-IDF: pakai nama folder + nama file) ===
texts = [os.path.basename(os.path.dirname(p)) + " " + os.path.basename(p) for p in image_paths]
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(texts).toarray()

# === Normalize fitur ===
features = normalize(features)

# === Save ===
np.save(OUTPUT_FEATURES, features)
import pickle
with open(OUTPUT_PATHS, "wb") as f:
    pickle.dump(image_paths, f)

print(f"[✓] Saved {len(image_paths)} features to {OUTPUT_FEATURES}")
