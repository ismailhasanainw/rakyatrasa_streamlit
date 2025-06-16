import os
import numpy as np
from PIL import Image
from tqdm import tqdm
import imagehash
import pickle

def load_and_preprocess(img_path, size=(128, 128)):
    img = Image.open(img_path).convert("L").resize(size)
    return img

def extract_features_from_folder(folder_path):
    features = []
    paths = []
    for fname in tqdm(os.listdir(folder_path)):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(folder_path, fname)
            img = load_and_preprocess(path)
            feat = extract_feature_vector(img)
            features.append(feat)
            paths.append(path)
    return np.array(features), paths

def extract_features(image):
    img = image.resize((224, 224)).convert("RGB")
    return extract_feature_vector(img)

def save_features_and_paths(features, paths, out_dir="dataset"):
    os.makedirs(out_dir, exist_ok=True)
    np.save(os.path.join(out_dir, "features.npy"), features)
    with open(os.path.join(out_dir, "paths.pkl"), "wb") as f:
        pickle.dump(paths, f)
