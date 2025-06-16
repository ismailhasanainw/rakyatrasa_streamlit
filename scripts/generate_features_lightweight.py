# ============================================
# Script: generate_features_lightweight.py
# Fungsi: Generate fitur ringan dari dataset gambar tanpa TensorFlow
#         Menggunakan histogram warna sebagai fitur visual sederhana
# ============================================

import os
import numpy as np
from PIL import Image
import pickle
from tqdm import tqdm

# ====== Konfigurasi Folder Dataset ======
ROOT_DIR = "dataset_drive"  # Ganti dengan lokasi folder gambar kamu
OUTPUT_FEATURES = "features.npy"
OUTPUT_PATHS = "paths.pkl"

# ====== Fungsi Ekstraksi Histogram Fitur ======
def extract_color_histogram(img_path):
    try:
        img = Image.open(img_path).convert("RGB")
        img = img.resize((128, 128))
        hist = img.histogram()  # 256*3 = 768 dimensi
        hist = np.array(hist) / sum(hist)  # Normalisasi
        return hist.astype(np.float32)
    except Exception as e:
        print(f"[!] Gagal baca {img_path}: {e}")
        return None

# ====== Proses Semua Gambar ======
features = []
paths = []

for root, _, files in os.walk(ROOT_DIR):
    for fname in files:
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(root, fname)
            feat = extract_color_histogram(path)
            if feat is not None:
                features.append(feat)
                paths.append(path)

# ====== Simpan Output ======
np.save(OUTPUT_FEATURES, np.array(features))
with open(OUTPUT_PATHS, "wb") as f:
    pickle.dump(paths, f)

print(f"✅ Berhasil generate fitur: {len(features)} gambar")
print(f"→ features.npy | {OUTPUT_FEATURES}")
print(f"→ paths.pkl    | {OUTPUT_PATHS}")
