import os
import numpy as np
from PIL import Image
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

# Load model untuk ekstraksi fitur
feature_model = tf.keras.applications.MobileNetV2(include_top=False, pooling='avg')

def load_and_preprocess(image_file, size=(224, 224)):
    img = Image.open(image_file).convert("RGB").resize(size)
    img = np.array(img) / 255.0
    return img

def predict_by_similarity(uploaded_file, features_db, paths_db, labels_folder="dataset/train/labels/"):
    img = load_and_preprocess(uploaded_file)
    img_feat = feature_model.predict(np.expand_dims(img, axis=0))[0].reshape(1, -1)

    sims = cosine_similarity(img_feat, features_db)[0]
    best_idx = np.argmax(sims)
    best_match_path = paths_db[best_idx]
    confidence = sims[best_idx] * 100

    fname = os.path.basename(best_match_path)
    label_file = fname.rsplit(".", 1)[0] + ".txt"
    label_path = os.path.join(labels_folder, label_file)

    label = "Tidak diketahui"
    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            label = f.read().strip()

    return label, confidence