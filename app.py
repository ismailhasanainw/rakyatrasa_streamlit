import streamlit as st
from PIL import Image
from model_predict import predict_image_class
from gdrive_helper import upload_to_gdrive
import tempfile

st.set_page_config(page_title="RakyatRasa", layout="centered")

st.title("🍛 RakyatRasa - Image Annotation App")
st.write("Unggah gambar masakan tradisional Indonesia untuk diklasifikasi secara otomatis. Jika tidak akurat, Anda bisa memberi anotasi manual.")

uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Preview Gambar", use_column_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        img.save(tmp.name)
        pred_label, confidence = predict_image_class(tmp.name)

    st.write(f"🧠 Prediksi Otomatis: **{pred_label}** (kepercayaan: {confidence:.2f})")

    if confidence < 0.8:
        manual_label = st.text_input("📝 Klasifikasi tidak yakin. Masukkan label manual:")
        if manual_label:
            label_final = manual_label
            st.success(f"Label disimpan sebagai: {label_final}")
        else:
            label_final = None
    else:
        label_final = pred_label

    if label_final:
        if st.button("💾 Simpan ke Google Drive"):
            upload_to_gdrive(uploaded_file, label_final)
            st.success("✅ Gambar dan label berhasil disimpan ke Google Drive.")