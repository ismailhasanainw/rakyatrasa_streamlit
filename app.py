import streamlit as st
from PIL import Image
import tempfile

# === Konfigurasi Halaman ===
st.set_page_config(page_title="RakyatRasa", layout="wide")

# === CSS Custom dari HTML (ringkasan styling penting) ===
st.markdown("""
<style>
    .upload-section {
        border: 2px dashed #f97316;
        border-radius: 8px;
        padding: 3rem;
        text-align: center;
        background: #fefefe;
    }
    .upload-section:hover {
        border-color: #ea580c;
        background: #fff7ed;
    }
    .uploaded-img {
        width: 100%;
        max-height: 300px;
        object-fit: cover;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
    }
    .btn-save {
        background: #ea580c;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 6px;
    }
    .btn-save:hover {
        background: #dc2626;
    }
</style>
""", unsafe_allow_html=True)

# === Header ===
st.markdown("""
<div style='text-align: center; background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%); color: white; padding: 2rem 0;'>
    <h1 style='margin-bottom: 0.5rem;'>RakyatRasa</h1>
    <p>Discover Indonesian Flavors Through Collaborative Intelligence</p>
    <p style='font-style: italic;'>"Indonesia on a Plate — Preserving Traditions Through Human-AI Collaboration"</p>
</div>
""", unsafe_allow_html=True)

# === Tab Navigasi ===
tabs = st.tabs(["Upload & Label", "Search Foods", "Verification", "Database"])

# === Upload Tab ===
with tabs[0]:
    st.subheader("📤 Upload Traditional Indonesian Food Image")
    uploaded_file = st.file_uploader("Upload Gambar Makanan Tradisional", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Preview Gambar", use_column_width=True)

        # Simulasi Prediksi AI
        st.success("✅ AI berhasil mengenali gambar sebagai: Sayur Asem")
        st.write("**Kepercayaan AI:** 87%")
        st.progress(87)

        # Form Manual Labeling
        with st.expander("📝 Koreksi atau Anotasi Manual"):
            food_name = st.text_input("Nama Makanan", value="Sayur Asem")
            region = st.selectbox("Asal Daerah", [
                "Jawa Barat", "DKI Jakarta", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur",
                "Sumatera Barat", "Sumatera Utara", "Bali", "Sulawesi Selatan", "Kalimantan Timur"
            ])
            taste = st.multiselect("Karakteristik Rasa", [
                "Manis", "Asin", "Pedas", "Asam", "Gurih", "Segar", "Rempah", "Santan", "Umami"
            ], default=["Asam", "Segar", "Gurih"])
            category = st.selectbox("Kategori", [
                "Sayuran", "Nasi & Noodles", "Daging", "Seafood", "Snack & Kue", "Sup & Soto", "Minuman"
            ])
            desc = st.text_area("Deskripsi Tambahan", "Sayur Asem adalah...")

        if st.button("💾 Simpan ke Database"):
            st.success(f"Data berhasil disimpan: {food_name} dari {region}")

# Tab lainnya bisa diisi belakangan sesuai fungsionalitas
