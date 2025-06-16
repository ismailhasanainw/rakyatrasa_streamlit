import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tqdm import tqdm

def load_and_preprocess(img_path, size=(224, 224)):
    img = Image.open(img_path).convert("RGB").resize(size)
    img = np.array(img) / 255.0
    return img

def extract_features(folder_path):
    feature_model = tf.keras.applications.MobileNetV2(include_top=False, pooling='avg')
    features = []
    paths = []

    for fname in tqdm(os.listdir(folder_path)):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(folder_path, fname)
            img = load_and_preprocess(path)
            feat = feature_model.predict(np.expand_dims(img, axis=0))[0]
            features.append(feat)
            paths.append(path)

    return np.array(features), paths