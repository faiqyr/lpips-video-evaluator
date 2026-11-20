import streamlit as st
import cv2
import torch
import lpips
import numpy as np
import tempfile
import matplotlib.pyplot as plt

# Konfigurasi Halaman Web
st.set_page_config(page_title="LPIPS Video Evaluator", layout="wide")
st.title("🎥 Evaluasi Stabilitas Temporal Video (LPIPS)")
st.markdown("Aplikasi ini menghitung metrik LPIPS antar-frame untuk mendeteksi stabilitas, *flickering* (Variance), dan *morphing* (Max).")

# Inisialisasi model LPIPS (menggunakan arsitektur AlexNet yang umum untuk standar LPIPS)
# Fitur st.cache_resource digunakan agar model tidak didownload/diloop ulang setiap kali upload video
@st.cache_resource
def load_lpips_model():
    return lpips.LPIPS(net='alex')

loss_fn_alex = load_lpips_model()

# Fungsi untuk memproses frame menjadi tensor PyTorch yang diterima LPIPS
def preprocess_frame(frame):
    # Konversi BGR (OpenCV) ke RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Konversi ke Tensor, ubah dimensi menjadi (C, H, W), dan tambah batch dimensi (1, C, H, W)
    frame_tensor = torch.tensor(frame_rgb).permute(2, 0, 1).unsqueeze(0).float()
    # Normalisasi nilai piksel dari [0, 255] menjadi rentang [-1, 1] sesuai syarat LPIPS
    frame_tensor = (frame_tensor / 255.0) * 2.0 - 1.0
    return frame_tensor

# Area Upload Video
uploaded_file = st.file_uploader("Upload Video Iterasi (.mp4, .avi, .mov)", type=['mp4', 'avi', 'mov'])

if uploaded_file is not None:
    st.info("Memproses video... Mohon tunggu sebentar.")
    
    # Simpan video upload ke temporary file karena OpenCV butuh path file fisik
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    # Buka video menggunakan OpenCV
    cap = cv2.VideoCapture(tfile.name)
    
    lpips_distances = []
    prev_frame_tensor = None
    frame_count = 0
    
    # Progress bar untuk UI
    progress_bar = st.progress(0)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Proses frame saat ini
        curr_frame_tensor = preprocess_frame(frame)
        
        # Hitung LPIPS jika sudah ada frame sebelumnya (F_i vs F_i+1)
        if prev_frame_tensor is not None:
            # Hitung jarak perseptual (jangan menghitung gradien/backward pass)
            with torch.no_grad():
                distance = loss_fn_alex(prev_frame_tensor, curr_frame_tensor)
            lpips_distances.append(distance.item())
            
        prev_frame_tensor = curr_frame_tensor
        frame_count += 1
        
        # Update progress bar
        if total_frames > 0:
            progress_bar.progress(min(frame_count / total_frames, 1.0))
            
    cap.release()
    
    # Pastikan video valid dan memiliki minimal 2 frame
    if len(lpips_distances) > 0:
        st.success(f"Video berhasil dievaluasi! Total frame yang dianalisis: {frame_count}")
        
        # Kalkulasi Statistik (Mean, Variance, Max)
        mean_lpips = np.mean(lpips_distances)
        var_lpips = np.var(lpips_distances)
        max_lpips = np.max(lpips_distances)
        
        # Menampilkan Metrik menggunakan elemen kolom Streamlit
        st.subheader("📊 Hasil Kalkulasi Statistik LPIPS")
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean LPIPS (Stabilitas)", f"{mean_lpips:.4f}", help="Makin rendah makin stabil")
        col2.metric("Variance (Indikasi Flickering)", f"{var_lpips:.6f}", help="Makin rendah fluktuasi kedipan makin kecil")
        col3.metric("Max LPIPS (Indikasi Morphing)", f"{max_lpips:.4f}", help="Makin rendah risiko morphing ekstrem makin kecil")
        
        # Visualisasi Grafik Frame-by-Frame
        st.subheader("📈 Evaluasi Fluktuasi Frame-by-Frame")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(range(1, len(lpips_distances) + 1), lpips_distances, color='#2ca02c', linewidth=1.5)
        ax.set_xlabel('Urutan Frame Berpasangan')
        ax.set_ylabel('Nilai LPIPS')
        ax.set_title('Fluktuasi Jarak Perseptual Antar Frame')
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Tampilkan grafik di web
        st.pyplot(fig)
        
        # Opsional: Tampilkan raw data
        with st.expander("Lihat Data LPIPS per Frame"):
            st.write(lpips_distances)
            
    else:
        st.error("Video terlalu pendek atau gagal diproses.")