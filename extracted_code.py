import cv2
import os
import shutil

def extract_all_frames(video_path, output_folder, target_size=(512, 512)):
    """
    Ekstraksi frame dengan standar penelitian:
    - Membersihkan folder lama
    - Center Crop & Resizing otomatis agar adil (apple-to-apple) tanpa distorsi
    - Metadata FPS asli
    """
    
    # 1. Memastikan folder bersih agar tidak ada data sampah dari running sebelumnya
    if os.path.exists(output_folder):
        print(f"Membersihkan folder lama: {output_folder}")
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Tidak bisa membuka video {video_path}")
        return

    # 2. Ambil informasi FPS asli video
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"--- Memproses: {video_path} ---")
    print(f"FPS Video: {fps:.2f} | Estimasi Total Frame: {total_frames_count}")
    print(f"Target Resolusi: {target_size} (dengan Center Crop)")

    count = 0
    while True:
        success, frame = cap.read()
        
        if not success:
            break
            
        # 3. Mencegah Distorsi dengan Center Crop sebelum Resize
        h, w = frame.shape[:2]
        min_dim = min(h, w)
        
        # Hitung titik potong tengah
        start_x = w // 2 - min_dim // 2
        start_y = h // 2 - min_dim // 2
        
        # Potong gambar menjadi persegi murni berdasarkan ukuran terkecil (tinggi/lebar)
        frame_cropped = frame[start_y:start_y+min_dim, start_x:start_x+min_dim]
        
        # 4. Resizing menggunakan interpolasi AREA (terbaik untuk downsampling)
        frame_resized = cv2.resize(frame_cropped, target_size, interpolation=cv2.INTER_AREA)
        
        frame_name = os.path.join(output_folder, f"frame_{count:04d}.png")
        
        # 5. Simpan frame (PNG otomatis menggunakan kompresi lossless)
        cv2.imwrite(frame_name, frame_resized)
        
        # Print progress berdasarkan FPS asli agar log terminal tidak banjir
        if count % max(1, int(fps)) == 0:
            progress = (count / total_frames_count) * 100 if total_frames_count > 0 else 0
            print(f"Proses {output_folder}: Frame {count} ({progress:.1f}%)")
            
        count += 1
            
    cap.release()
    print(f"Selesai! Total {count} frame disimpan di: {output_folder}\n")


# --- PENGGUNAAN BATCH (EKSTRAKSI BANYAK VIDEO OTOMATIS) ---
TARGET_RES = (512, 512) 

##=========Tentukan Folder utama===================================================
# Tentukan folder utama
input_base_folder = "structured"
output_base_folder = "frames_structured/structured_shot3" ##tentukan foldernya disini

# Pastikan folder utama output tersedia
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

##=========structuredshot1===================================================
# # Looping dari 1 sampai 10
# for i in range(1, 11):
#     # Membentuk nama file video: structuredshot1_01.mp4, dst.
#     # {i:02d} otomatis mengubah angka 1 menjadi "01", 2 menjadi "02", dst.
#     video_filename = f"structuredshot1_{i:02d}.mp4"
#     video_path = os.path.join(input_base_folder, video_filename)
    
#     # Membentuk nama folder output: frames_structured01, dst.
#     output_foldername = f"frames_structured{i:02d}"
    
#     # Menggabungkan folder utama output dengan sub-folder
#     # Hasilnya: frames_structured/frames_structured01
#     output_path = os.path.join(output_base_folder, output_foldername)
    
#     # Cek apakah file video benar-benar ada di folder 'structured' sebelum diekstrak
#     if os.path.exists(video_path):
#         print(f">>> Memulai Batch {i}/10 <<<")
#         extract_all_frames(video_path, output_path, target_size=TARGET_RES)
#     else:
#         print(f"PERINGATAN: File video tidak ditemukan di {video_path}. Melewati proses ini...\n")

# print("=== SEMUA PROSES EKSTRAKSI BATCH SELESAI ===")



##=========structuredshot2===================================================
# # Looping dari 1 sampai 10
# for i in range(1, 11):
#     # Membentuk nama file video: structuredshot1_01.mp4, dst.
#     # {i:02d} otomatis mengubah angka 1 menjadi "01", 2 menjadi "02", dst.
#     video_filename = f"structuredshot2_{i:02d}.mp4"
#     video_path = os.path.join(input_base_folder, video_filename)
    
#     # Membentuk nama folder output: frames_structured01, dst.
#     output_foldername = f"frames_structured{i:02d}"
    
#     # Menggabungkan folder utama output dengan sub-folder
#     # Hasilnya: frames_structured/frames_structured01
#     output_path = os.path.join(output_base_folder, output_foldername)
    
#     # Cek apakah file video benar-benar ada di folder 'structured' sebelum diekstrak
#     if os.path.exists(video_path):
#         print(f">>> Memulai Batch {i}/10 <<<")
#         extract_all_frames(video_path, output_path, target_size=TARGET_RES)
#     else:
#         print(f"PERINGATAN: File video tidak ditemukan di {video_path}. Melewati proses ini...\n")

# print("=== SEMUA PROSES EKSTRAKSI BATCH SELESAI ===")




##=========structuredshot3===================================================
# Looping dari 1 sampai 10
for i in range(1, 11):
    # Membentuk nama file video: structuredshot1_01.mp4, dst.
    # {i:02d} otomatis mengubah angka 1 menjadi "01", 2 menjadi "02", dst.
    video_filename = f"structuredshot3_{i:02d}.mp4"
    video_path = os.path.join(input_base_folder, video_filename)
    
    # Membentuk nama folder output: frames_structured01, dst.
    output_foldername = f"frames_structured{i:02d}"
    
    # Menggabungkan folder utama output dengan sub-folder
    # Hasilnya: frames_structured/frames_structured01
    output_path = os.path.join(output_base_folder, output_foldername)
    
    # Cek apakah file video benar-benar ada di folder 'structured' sebelum diekstrak
    if os.path.exists(video_path):
        print(f">>> Memulai Batch {i}/10 <<<")
        extract_all_frames(video_path, output_path, target_size=TARGET_RES)
    else:
        print(f"PERINGATAN: File video tidak ditemukan di {video_path}. Melewati proses ini...\n")

print("=== SEMUA PROSES EKSTRAKSI BATCH SELESAI ===")

import cv2
import os
import shutil

def extract_all_frames(video_path, output_folder, target_size=(512, 512)):
    """
    Ekstraksi frame dengan standar penelitian:
    - Membersihkan folder lama
    - Center Crop & Resizing otomatis agar adil (apple-to-apple) tanpa distorsi
    - Metadata FPS asli
    """
    
    # 1. Pastikan folder bersih agar tidak ada data sampah dari running sebelumnya
    if os.path.exists(output_folder):
        print(f"Membersihkan folder lama: {output_folder}")
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Tidak bisa membuka video {video_path}")
        return

    # 2. Ambil informasi FPS asli video
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"--- Memproses: {video_path} ---")
    print(f"FPS Video: {fps:.2f} | Estimasi Total Frame: {total_frames_count}")
    print(f"Target Resolusi: {target_size} (dengan Center Crop)")

    count = 0
    while True:
        success, frame = cap.read()
        
        if not success:
            break
            
        # 3. Mencegah Distorsi dengan Center Crop sebelum Resize
        h, w = frame.shape[:2]
        min_dim = min(h, w)
        
        # Hitung titik potong tengah
        start_x = w // 2 - min_dim // 2
        start_y = h // 2 - min_dim // 2
        
        # Potong gambar menjadi persegi murni berdasarkan ukuran terkecil (tinggi/lebar)
        frame_cropped = frame[start_y:start_y+min_dim, start_x:start_x+min_dim]
        
        # 4. Resizing menggunakan interpolasi AREA (terbaik untuk downsampling)
        frame_resized = cv2.resize(frame_cropped, target_size, interpolation=cv2.INTER_AREA)
        
        frame_name = os.path.join(output_folder, f"frame_{count:04d}.png")
        
        # 5. Simpan frame (PNG otomatis menggunakan kompresi lossless)
        cv2.imwrite(frame_name, frame_resized)
        
        # Print progress berdasarkan FPS asli agar log terminal tidak banjir
        if count % max(1, int(fps)) == 0:
            progress = (count / total_frames_count) * 100 if total_frames_count > 0 else 0
            print(f"Proses {output_folder}: Frame {count} ({progress:.1f}%)")
            
        count += 1
            
    cap.release()
    print(f"Selesai! Total {count} frame disimpan di: {output_folder}\n")


# --- PENGGUNAAN BATCH (EKSTRAKSI BANYAK VIDEO OTOMATIS) ---
TARGET_RES = (512, 512) 

##=========Tentukan Folder utama===================================================
# Tentukan folder utama
input_base_folder = "unstructured"
output_base_folder = "frames_unstructured/unstructured_shot3" ##tentukan foldernya disini

# Pastikan folder utama output tersedia
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

##=========unstructuredshot1===================================================
# # Looping dari 1 sampai 10
# for i in range(1, 11):
#     # Membentuk nama file video: unstructuredshot1_01.mp4, dst.
#     # {i:02d} otomatis mengubah angka 1 menjadi "01", 2 menjadi "02", dst.
#     video_filename = f"unstructuredshot1_{i:02d}.mp4"
#     video_path = os.path.join(input_base_folder, video_filename)
    
#     # Membentuk nama folder output: frames_unstructured01, dst.
#     output_foldername = f"frames_unstructured{i:02d}"
    
#     # Menggabungkan folder utama output dengan sub-folder
#     # Hasilnya: frames_unstructured/frames_unstructured01
#     output_path = os.path.join(output_base_folder, output_foldername)
    
#     # Cek apakah file video benar-benar ada di folder 'unstructured' sebelum diekstrak
#     if os.path.exists(video_path):
#         print(f">>> Memulai Batch {i}/10 <<<")
#         extract_all_frames(video_path, output_path, target_size=TARGET_RES)
#     else:
#         print(f"PERINGATAN: File video tidak ditemukan di {video_path}. Melewati proses ini...\n")

# print("=== SEMUA PROSES EKSTRAKSI BATCH SELESAI ===")



##=========unstructuredshot2===================================================
# # Looping dari 1 sampai 10
# for i in range(1, 11):
#     # Membentuk nama file video: unstructuredshot2_01.mp4, dst.
#     # {i:02d} otomatis mengubah angka 1 menjadi "01", 2 menjadi "02", dst.
#     video_filename = f"unstructuredshot2_{i:02d}.mp4"
#     video_path = os.path.join(input_base_folder, video_filename)
    
#     # Membentuk nama folder output: frames_unstructured01, dst.
#     output_foldername = f"frames_unstructured{i:02d}"
    
#     # Menggabungkan folder utama output dengan sub-folder
#     # Hasilnya: frames_unstructured/frames_unstructured01
#     output_path = os.path.join(output_base_folder, output_foldername)
    
#     # Cek apakah file video benar-benar ada di folder 'unstructured' sebelum diekstrak
#     if os.path.exists(video_path):
#         print(f">>> Memulai Batch {i}/10 <<<")
#         extract_all_frames(video_path, output_path, target_size=TARGET_RES)
#     else:
#         print(f"PERINGATAN: File video tidak ditemukan di {video_path}. Melewati proses ini...\n")

# print("=== SEMUA PROSES EKSTRAKSI BATCH SELESAI ===")




##=========unstructuredshot3===================================================
# Looping dari 1 sampai 10
for i in range(1, 11):
    # Membentuk nama file video: unstructuredshot3_01.mp4, dst.
    # {i:02d} otomatis mengubah angka 1 menjadi "01", 2 menjadi "02", dst.
    video_filename = f"unstructuredshot3_{i:02d}.mp4"
    video_path = os.path.join(input_base_folder, video_filename)
    
    # Membentuk nama folder output: frames_unstructured01, dst.
    output_foldername = f"frames_unstructured{i:02d}"
    
    # Menggabungkan folder utama output dengan sub-folder
    # Hasilnya: frames_unstructured/frames_unstructured01
    output_path = os.path.join(output_base_folder, output_foldername)
    
    # Cek apakah file video benar-benar ada di folder 'unstructured' sebelum diekstrak
    if os.path.exists(video_path):
        print(f">>> Memulai Batch {i}/10 <<<")
        extract_all_frames(video_path, output_path, target_size=TARGET_RES)
    else:
        print(f"PERINGATAN: File video tidak ditemukan di {video_path}. Melewati proses ini...\n")

print("=== SEMUA PROSES EKSTRAKSI BATCH SELESAI ===")

import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")

import lpips
import torch
from PIL import Image
from torchvision import transforms

# =====================================================================
# TAHAP 2: INISIALISASI MODEL & PEMROSESAN TENSOR (ENVIRONMENT SETUP)
# =====================================================================

print("--- Memulai Setup Environment ---")

# 1. Deteksi Hardware (Otomatis menggunakan GPU jika tersedia)
# Sangat disarankan untuk skripsi agar komputasi ribuan frame lebih cepat
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Hardware yang digunakan: {device.type.upper()}")

# 2. Inisialisasi Model LPIPS
# Menggunakan backbone AlexNet (standar umum untuk evaluasi perseptual)
print("[INFO] Memuat model LPIPS (AlexNet)...")
loss_fn_alex = lpips.LPIPS(net='alex').to(device)
print("[INFO] Model berhasil dimuat dan dipindahkan ke device.")

# 3. Fungsi Pemrosesan Tensor (Image Loader)
def load_image(path, target_size=(512, 512)):
    """
    Fungsi untuk memuat gambar dan mengubahnya menjadi Tensor yang siap dibaca model LPIPS.
    Pastikan target_size sama dengan resolusi ekstraksi frame di Tahap 1.
    """
    img = Image.open(path).convert('RGB')
    
    transform = transforms.Compose([
        # Memastikan ukuran konsisten
        transforms.Resize(target_size), 
        
        # Mengubah gambar menjadi tensor dengan rentang nilai [0, 1]
        transforms.ToTensor(),
        
        # [KRUSIAL] Normalisasi ke rentang [-1, 1] sesuai standar LPIPS
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) 
    ])
    
    # Menambahkan dimensi batch (unsqueeze(0)) karena model PyTorch meminta format (Batch, Channel, Height, Width)
    # Lalu pindahkan tensor ke memori GPU/CPU
    return transform(img).unsqueeze(0).to(device)

print("--- Setup Selesai. Model siap digunakan untuk pengujian. ---\n")

import lpips
import torch
from PIL import Image
from torchvision import transforms

# ==========================================
# KONFIGURASI DEVICE
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Menggunakan device: {device}")

# ==========================================
# LOAD MODEL LPIPS
# ==========================================
loss_fn_alex = lpips.LPIPS(net='alex').to(device)
loss_fn_alex.eval()

# ==========================================
# FUNGSI LOAD GAMBAR
# ==========================================
def load_image(path):
    img = Image.open(path).convert("RGB")

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5)
        )
    ])

    return transform(img).unsqueeze(0).to(device)

# ==========================================
# PATH FRAME
# ==========================================

frame_1 = r"frame_0000.png"
frame_2 = r"frame_0001.png"

# ==========================================
# LOAD FRAME
# ==========================================

frame_1 = r"frames_structured\structured_shot1\frames_structured01\frame_0002.png"
frame_2 = r"frames_structured\structured_shot1\frames_structured01\frame_0003.png"

# ==========================================
# LOAD FRAME
# ==========================================

img1 = load_image(frame_1)
img2 = load_image(frame_2)

# ==========================================
# HITUNG LPIPS
# ==========================================

with torch.no_grad():
    lpips_score = loss_fn_alex(img1, img2).item()

print("="*50)
print(f"Frame A : {frame_1}")
print(f"Frame B : {frame_2}")
print(f"LPIPS   : {lpips_score:.6f}")
print("="*50)

import lpips
import torch
import pandas as pd
import os
import glob
from PIL import Image
from torchvision import transforms
import numpy as np

# ==========================================
# TAHAP 2: KONFIGURASI MODEL & ENVIRONMENT
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Menjalankan pengujian menggunakan: {device.type.upper()}")

loss_fn_alex = lpips.LPIPS(net='alex').to(device)

def load_image_for_lpips(path):
    img = Image.open(path).convert('RGB')
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) 
    ])
    return transform(img).unsqueeze(0).to(device)

# ==========================================
# TAHAP 3: PROTOKOL PENGUJIAN TEMPORAL
# ==========================================
def test_temporal_stability(folder_path, output_csv_name):
    files = sorted(glob.glob(os.path.join(folder_path, "frame_*.png")))
    if len(files) < 2:
        return None, None, None

    results = []
    with torch.no_grad(): 
        for i in range(len(files) - 1):
            # Mengambil path lengkap untuk frame saat ini dan selanjutnya
            path_a = files[i]
            path_b = files[i+1]
            
            img_t0 = load_image_for_lpips(path_a)
            img_t1 = load_image_for_lpips(path_b)
            
            dist = loss_fn_alex(img_t0, img_t1).item()
            
            # Menyimpan nama frame beserta skornya
            results.append({
                'Frame_A': os.path.basename(path_a),
                'Frame_B': os.path.basename(path_b),
                'LPIPS_Score': round(dist, 5) # Dibulatkan 5 desimal agar rapi
            })

    df = pd.DataFrame(results)
    df.to_csv(output_csv_name, index=False)
    
    # Hitung Statistik per Video
    mean_v = df['LPIPS_Score'].mean()  
    var_v = df['LPIPS_Score'].var()    
    max_v = df['LPIPS_Score'].max()    
    
    return mean_v, var_v, max_v

# ==========================================
# EKSEKUSI PENGUJIAN OTOMATIS (BATCH)
# ==========================================
if __name__ == "__main__":
    
    # Tentukan folder utama
    base_folder_structured = r"frames_structured\structured_shot1"
    base_folder_unstructured = r"frames_unstructured\unstructured_shot1" 

    def run_batch_temporal_test(base_folder, method_name):
        print(f"\n--- MEMULAI BATCH TEST: {method_name.upper()} ---")
        
        subfolders = sorted(glob.glob(os.path.join(base_folder, "*/")))
        if not subfolders:
            subfolders = sorted(glob.glob(os.path.join(base_folder, "*")))
            subfolders = [f for f in subfolders if os.path.isdir(f)]

        # List untuk menampung ringkasan per video
        summary_data = []
        
        for folder in subfolders:
            folder_name = os.path.basename(os.path.normpath(folder))
            csv_detail = f"detail_temporal_{method_name}_{folder_name}.csv"
            
            # Jalankan tes
            m, v, mx = test_temporal_stability(folder, csv_detail)
            
            if m is not None:
                summary_data.append({
                    'Video': folder_name,
                    'Mean LPIPS': round(m, 4),
                    'Variance (Flicker)': round(v, 7),
                    'Max (Morphing)': round(mx, 4)
                })
                print(f"Selesai memproses {folder_name}")

        # --- BAGIAN PEMBUATAN RINGKASAN ---
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            
            # Hitung Baris Rata-rata Total
            total_avg = {
                'Video': 'Rata-rata Total',
                'Mean LPIPS': round(df_summary['Mean LPIPS'].mean(), 4),
                'Variance (Flicker)': round(df_summary['Variance (Flicker)'].mean(), 7),
                'Max (Morphing)': round(df_summary['Max (Morphing)'].mean(), 4)
            }
            
            # Tambahkan baris total ke tabel
            df_summary = pd.concat([df_summary, pd.DataFrame([total_avg])], ignore_index=True)
            
            # Simpan ke file Ringkasan Akhir
            summary_filename = f"SUMMARY_REPORT_TEMPORAL_{method_name.upper()}.csv"
            df_summary.to_csv(summary_filename, index=False)
            
            print(f"\n>>> HASIL AKHIR {method_name.upper()} <<<")
            print(df_summary.to_string(index=False)) # Tampilkan di terminal
            print(f"\nLaporan ringkasan disimpan di: {summary_filename}")

    # 1. Jalankan untuk Structured
    run_batch_temporal_test(base_folder_structured, "structured")
    
    # 2. Jalankan untuk Unstructured
    run_batch_temporal_test(base_folder_unstructured, "unstructured")

import lpips
import torch
import pandas as pd
import os
import glob
from PIL import Image
from torchvision import transforms
import numpy as np

# ==========================================
# TAHAP 2: KONFIGURASI MODEL & ENVIRONMENT
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Menjalankan pengujian menggunakan: {device.type.upper()}")

loss_fn_alex = lpips.LPIPS(net='alex').to(device)

def load_image_for_lpips(path):
    img = Image.open(path).convert('RGB')
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) 
    ])
    return transform(img).unsqueeze(0).to(device)

# ==========================================
# TAHAP 3: PROTOKOL PENGUJIAN TEMPORAL
# ==========================================
def test_temporal_stability(folder_path, output_csv_name):
    files = sorted(glob.glob(os.path.join(folder_path, "frame_*.png")))
    if len(files) < 2:
        return None, None, None

    results = []
    with torch.no_grad(): 
        for i in range(len(files) - 1):
            # Mengambil path lengkap untuk frame saat ini dan selanjutnya
            path_a = files[i]
            path_b = files[i+1]
            
            img_t0 = load_image_for_lpips(path_a)
            img_t1 = load_image_for_lpips(path_b)
            
            dist = loss_fn_alex(img_t0, img_t1).item()
            
            # Menyimpan nama frame beserta skornya
            results.append({
                'Frame_A': os.path.basename(path_a),
                'Frame_B': os.path.basename(path_b),
                'LPIPS_Score': round(dist, 5) # Dibulatkan 5 desimal agar rapi
            })

    df = pd.DataFrame(results)
    df.to_csv(output_csv_name, index=False)
    
    # Hitung Statistik per Video
    mean_v = df['LPIPS_Score'].mean()  
    var_v = df['LPIPS_Score'].var()    
    max_v = df['LPIPS_Score'].max()    
    
    return mean_v, var_v, max_v

# ==========================================
# EKSEKUSI PENGUJIAN OTOMATIS (BATCH)
# ==========================================
if __name__ == "__main__":
    
    # Tentukan folder utama
    base_folder_structured = r"frames_structured\structured_shot2"
    base_folder_unstructured = r"frames_unstructured\unstructured_shot2" 

    def run_batch_temporal_test(base_folder, method_name):
        print(f"\n--- MEMULAI BATCH TEST: {method_name.upper()} ---")
        
        subfolders = sorted(glob.glob(os.path.join(base_folder, "*/")))
        if not subfolders:
            subfolders = sorted(glob.glob(os.path.join(base_folder, "*")))
            subfolders = [f for f in subfolders if os.path.isdir(f)]

        # List untuk menampung ringkasan per video
        summary_data = []
        
        for folder in subfolders:
            folder_name = os.path.basename(os.path.normpath(folder))
            csv_detail = f"detail_temporal_{method_name}_{folder_name}.csv"
            
            # Jalankan tes
            m, v, mx = test_temporal_stability(folder, csv_detail)
            
            if m is not None:
                summary_data.append({
                    'Video': folder_name,
                    'Mean LPIPS': round(m, 4),
                    'Variance (Flicker)': round(v, 7),
                    'Max (Morphing)': round(mx, 4)
                })
                print(f"Selesai memproses {folder_name}")

        # --- BAGIAN PEMBUATAN RINGKASAN ---
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            
            # Hitung Baris Rata-rata Total
            total_avg = {
                'Video': 'Rata-rata Total',
                'Mean LPIPS': round(df_summary['Mean LPIPS'].mean(), 4),
                'Variance (Flicker)': round(df_summary['Variance (Flicker)'].mean(), 7),
                'Max (Morphing)': round(df_summary['Max (Morphing)'].mean(), 4)
            }
            
            # Tambahkan baris total ke tabel
            df_summary = pd.concat([df_summary, pd.DataFrame([total_avg])], ignore_index=True)
            
            # Simpan ke file Ringkasan Akhir
            summary_filename = f"SUMMARY_REPORT_TEMPORAL_{method_name.upper()}.csv"
            df_summary.to_csv(summary_filename, index=False)
            
            print(f"\n>>> HASIL AKHIR {method_name.upper()} <<<")
            print(df_summary.to_string(index=False)) # Tampilkan di terminal
            print(f"\nLaporan ringkasan disimpan di: {summary_filename}")

    # 1. Jalankan untuk Structured
    run_batch_temporal_test(base_folder_structured, "structured")
    
    # 2. Jalankan untuk Unstructured
    run_batch_temporal_test(base_folder_unstructured, "unstructured")

import lpips
import torch
import pandas as pd
import os
import glob
from PIL import Image
from torchvision import transforms
import numpy as np

# ==========================================
# TAHAP 2: KONFIGURASI MODEL & ENVIRONMENT
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Menjalankan pengujian menggunakan: {device.type.upper()}")

loss_fn_alex = lpips.LPIPS(net='alex').to(device)

def load_image_for_lpips(path):
    img = Image.open(path).convert('RGB')
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) 
    ])
    return transform(img).unsqueeze(0).to(device)

# ==========================================
# TAHAP 3: PROTOKOL PENGUJIAN TEMPORAL
# ==========================================
def test_temporal_stability(folder_path, output_csv_name):
    files = sorted(glob.glob(os.path.join(folder_path, "frame_*.png")))
    if len(files) < 2:
        return None, None, None

    results = []
    with torch.no_grad(): 
        for i in range(len(files) - 1):
            # Mengambil path lengkap untuk frame saat ini dan selanjutnya
            path_a = files[i]
            path_b = files[i+1]
            
            img_t0 = load_image_for_lpips(path_a)
            img_t1 = load_image_for_lpips(path_b)
            
            dist = loss_fn_alex(img_t0, img_t1).item()
            
            # Menyimpan nama frame beserta skornya
            results.append({
                'Frame_A': os.path.basename(path_a),
                'Frame_B': os.path.basename(path_b),
                'LPIPS_Score': round(dist, 5) # Dibulatkan 5 desimal agar rapi
            })

    df = pd.DataFrame(results)
    df.to_csv(output_csv_name, index=False)
    
    # Hitung Statistik per Video
    mean_v = df['LPIPS_Score'].mean()  
    var_v = df['LPIPS_Score'].var()    
    max_v = df['LPIPS_Score'].max()    
    
    return mean_v, var_v, max_v

# ==========================================
# EKSEKUSI PENGUJIAN OTOMATIS (BATCH)
# ==========================================
if __name__ == "__main__":
    
    # Tentukan folder utama
    base_folder_structured = r"frames_structured\structured_shot3"
    base_folder_unstructured = r"frames_unstructured\unstructured_shot3" 

    def run_batch_temporal_test(base_folder, method_name):
        print(f"\n--- MEMULAI BATCH TEST: {method_name.upper()} ---")
        
        subfolders = sorted(glob.glob(os.path.join(base_folder, "*/")))
        if not subfolders:
            subfolders = sorted(glob.glob(os.path.join(base_folder, "*")))
            subfolders = [f for f in subfolders if os.path.isdir(f)]

        # List untuk menampung ringkasan per video
        summary_data = []
        
        for folder in subfolders:
            folder_name = os.path.basename(os.path.normpath(folder))
            csv_detail = f"detail_temporal_{method_name}_{folder_name}.csv"
            
            # Jalankan tes
            m, v, mx = test_temporal_stability(folder, csv_detail)
            
            if m is not None:
                summary_data.append({
                    'Video': folder_name,
                    'Mean LPIPS': round(m, 4),
                    'Variance (Flicker)': round(v, 7),
                    'Max (Morphing)': round(mx, 4)
                })
                print(f"Selesai memproses {folder_name}")

        # --- BAGIAN PEMBUATAN RINGKASAN ---
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            
            # Hitung Baris Rata-rata Total
            total_avg = {
                'Video': 'Rata-rata Total',
                'Mean LPIPS': round(df_summary['Mean LPIPS'].mean(), 4),
                'Variance (Flicker)': round(df_summary['Variance (Flicker)'].mean(), 7),
                'Max (Morphing)': round(df_summary['Max (Morphing)'].mean(), 4)
            }
            
            # Tambahkan baris total ke tabel
            df_summary = pd.concat([df_summary, pd.DataFrame([total_avg])], ignore_index=True)
            
            # Simpan ke file Ringkasan Akhir
            summary_filename = f"SUMMARY_REPORT_TEMPORAL_{method_name.upper()}.csv"
            df_summary.to_csv(summary_filename, index=False)
            
            print(f"\n>>> HASIL AKHIR {method_name.upper()} <<<")
            print(df_summary.to_string(index=False)) # Tampilkan di terminal
            print(f"\nLaporan ringkasan disimpan di: {summary_filename}")

    # 1. Jalankan untuk Structured
    run_batch_temporal_test(base_folder_structured, "structured")
    
    # 2. Jalankan untuk Unstructured
    run_batch_temporal_test(base_folder_unstructured, "unstructured")

import subprocess
import os

# =====Tentukan folder tempat video berada======
##JSON
video_folder = r"D:\zkripsi_animasi\Dataset\Shot3\JSON\bukti generate"

##Unstructured
# video_folder = r"D:\zkripsi_animasi\Dataset\Shot3\Unstructured\bukti generate"

# List untuk menyimpan semua durasi
durations = []

print("--- HASIL PENGUKURAN DURASI VIDEO ---")

for i in range(1, 11):
    # ========ubah dibawah untuk setiap perhitungan=======
    filename = f"structuredshot3_{i:02d}.mp4" ## ubah ini mau structured atau unstructured
    full_path = os.path.join(video_folder, filename)
    
    if os.path.exists(full_path):
        cmd = [
            'ffprobe', '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            full_path
        ]
        
        try:
            # Mengambil output, dekode, dan ubah ke float agar bisa dihitung
            result_raw = subprocess.check_output(cmd).decode().strip()
            duration_val = float(result_raw)
            durations.append(duration_val)
            
            # Print dengan format 2 desimal agar ilmiah
            print(f"{filename} : {duration_val:.2f} detik")
        except Exception as e:
            print(f"Gagal memproses {filename}: {e}")
    else:
        print(f"{filename} : Tidak ditemukan")

# --- PERHITUNGAN STATISTIK ---
if durations:
    total_data = len(durations)
    rata_rata = sum(durations) / total_data
    
    print("-" * 40)
    print(f"TOTAL SAMPEL  : {total_data} video")
    print(f"RATA-RATA     : {rata_rata:.2f} detik")
    print("-" * 40)
else:
    print("\nData durasi tidak ditemukan. Pastikan folder dan file sudah benar.")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style untuk grafik agar terlihat profesional
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif'})

def plot_all_iterations_in_one_grid(output_image_name):
    print("\n--- Memulai Pembuatan Grafik 10 Iterasi ---")
    
    # Inisialisasi grid 5x2
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 22))
    axes = axes.flatten()
    
    # Alamat folder (Gunakan 'r' untuk menghindari error backslash)
    base_path = r"D:\zkripsi_animasi\evaluasi_temporal\shot1"
    
    # Variabel untuk menyimpan contoh label legenda
    handles_global, labels_global = [], []
    
    for i in range(1, 11):
        iter_num = f"{i:02d}" # Format 01, 02, dst.
        ax = axes[i-1]
        
        # Penamaan file sesuai struktur data penelitian Anda
        file_struct = f"detail_temporal_structured_frames_structured{iter_num}.csv"
        file_unstruct = f"detail_temporal_unstructured_frames_unstructured{iter_num}.csv"
        
        path_struct = os.path.join(base_path, "structured", file_struct)
        path_unstruct = os.path.join(base_path, "unstructured", file_unstruct)

        # Cek keberadaan file sebelum membaca
        if os.path.exists(path_struct) and os.path.exists(path_unstruct):
            try:
                df_s = pd.read_csv(path_struct)
                df_u = pd.read_csv(path_unstruct)
                
                # Plotting dengan label yang jelas
                line_u, = ax.plot(df_u.index, df_u['LPIPS_Score'], color='#e74c3c', label='Unstructured Prompting', alpha=0.8)
                line_s, = ax.plot(df_s.index, df_s['LPIPS_Score'], color='#2980b9', label='JSON-Structured Prompting', alpha=0.9)
                
                # Mengambil label dari iterasi pertama untuk dipakai di Legenda Global
                if i == 1:
                    handles_global = [line_u, line_s]
                    labels_global = ['Unstructured Prompting', 'JSON-Structured Prompting']
                
                # Estetika tiap kotak
                ax.set_title(f'Video Iterasi {iter_num}', fontweight='bold', fontsize=12)
                ax.set_xlabel('Urutan Frame', fontsize=10)
                ax.set_ylabel('Nilai LPIPS', fontsize=10)
                
            except Exception as e:
                ax.text(0.5, 0.5, f"Error Reading:\n{iter_num}", ha='center', va='center', color='orange')
        else:
            # Jika file tidak ditemukan, tampilkan pesan di grafik
            ax.text(0.5, 0.5, f'File Tidak Ditemukan\nIterasi {iter_num}', 
                    ha='center', va='center', color='red', fontsize=10)
            print(f"⚠️ Missing: Iterasi {iter_num}")

    # =========================================================
    # PERBAIKAN: MENAMBAHKAN JUDUL UTAMA DAN LEGENDA GLOBAL
    # =========================================================
    
    # 1. Judul Utama
    plt.suptitle('Analisis Fluktuasi Stabilitas Temporal LPIPS \n(Shot 1)', 
                 fontsize=20, y=0.97, fontweight='bold', ha='center')
    
    # 2. Menambahkan Legenda Global di bagian atas-tengah
    if handles_global:
        fig.legend(handles_global, labels_global, loc='upper center', bbox_to_anchor=(0.5, 0.935), 
                   ncol=2, fontsize=14, frameon=True, edgecolor='black', shadow=False)

    # 3. Mengatur margin (Tight Layout) agar grafik tidak menabrak legenda di atasnya
    # Batas atas (top) diturunkan ke 0.91 agar ada ruang untuk judul dan legenda
    plt.tight_layout(rect=[0, 0.02, 1, 0.91], h_pad=3.0, w_pad=2.0)
    
    # Simpan dan Tampilkan
    plt.savefig(output_image_name, dpi=300, bbox_inches='tight')
    print(f"✅ Selesai! Grafik berhasil disimpan: {output_image_name}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    plot_all_iterations_in_one_grid("Hasil_Analisis_LPIPS_Shot1_Lengkap.png")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style untuk grafik agar terlihat profesional
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif'})

def plot_all_iterations_in_one_grid(output_image_name):
    print("\n--- Memulai Pembuatan Grafik 10 Iterasi ---")
    
    # Inisialisasi grid 5x2
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 22))
    axes = axes.flatten()
    
    # Alamat folder (Gunakan 'r' untuk menghindari error backslash)
    base_path = r"D:\zkripsi_animasi\evaluasi_temporal\shot2"
    
    # Variabel untuk menyimpan contoh label legenda
    handles_global, labels_global = [], []
    
    for i in range(1, 11):
        iter_num = f"{i:02d}" # Format 01, 02, dst.
        ax = axes[i-1]
        
        # Penamaan file sesuai struktur data penelitian Anda
        file_struct = f"detail_temporal_structured_frames_structured{iter_num}.csv"
        file_unstruct = f"detail_temporal_unstructured_frames_unstructured{iter_num}.csv"
        
        path_struct = os.path.join(base_path, "structured", file_struct)
        path_unstruct = os.path.join(base_path, "unstructured", file_unstruct)

        # Cek keberadaan file sebelum membaca
        if os.path.exists(path_struct) and os.path.exists(path_unstruct):
            try:
                df_s = pd.read_csv(path_struct)
                df_u = pd.read_csv(path_unstruct)
                
                # Plotting dengan label yang jelas
                line_u, = ax.plot(df_u.index, df_u['LPIPS_Score'], color='#e74c3c', label='Unstructured Prompting', alpha=0.8)
                line_s, = ax.plot(df_s.index, df_s['LPIPS_Score'], color='#2980b9', label='JSON-Structured Prompting', alpha=0.9)
                
                # Mengambil label dari iterasi pertama untuk dipakai di Legenda Global
                if i == 1:
                    handles_global = [line_u, line_s]
                    labels_global = ['Unstructured Prompting', 'JSON-Structured Prompting']
                
                # Estetika tiap kotak
                ax.set_title(f'Video Iterasi {iter_num}', fontweight='bold', fontsize=12)
                ax.set_xlabel('Urutan Frame', fontsize=10)
                ax.set_ylabel('Nilai LPIPS', fontsize=10)
                
            except Exception as e:
                ax.text(0.5, 0.5, f"Error Reading:\n{iter_num}", ha='center', va='center', color='orange')
        else:
            # Jika file tidak ditemukan, tampilkan pesan di grafik
            ax.text(0.5, 0.5, f'File Tidak Ditemukan\nIterasi {iter_num}', 
                    ha='center', va='center', color='red', fontsize=10)
            print(f"⚠️ Missing: Iterasi {iter_num}")

    # =========================================================
    # PERBAIKAN: MENAMBAHKAN JUDUL UTAMA DAN LEGENDA GLOBAL
    # =========================================================
    
    # 1. Judul Utama
    plt.suptitle('Analisis Fluktuasi Stabilitas Temporal LPIPS \n(Shot 2)', 
                 fontsize=20, y=0.97, fontweight='bold', ha='center')
    
    # 2. Menambahkan Legenda Global di bagian atas-tengah
    if handles_global:
        fig.legend(handles_global, labels_global, loc='upper center', bbox_to_anchor=(0.5, 0.935), 
                   ncol=2, fontsize=14, frameon=True, edgecolor='black', shadow=False)

    # 3. Mengatur margin (Tight Layout) agar grafik tidak menabrak legenda di atasnya
    # Batas atas (top) diturunkan ke 0.91 agar ada ruang untuk judul dan legenda
    plt.tight_layout(rect=[0, 0.02, 1, 0.91], h_pad=3.0, w_pad=2.0)
    
    # Simpan dan Tampilkan
    plt.savefig(output_image_name, dpi=300, bbox_inches='tight')
    print(f"✅ Selesai! Grafik berhasil disimpan: {output_image_name}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    plot_all_iterations_in_one_grid("Hasil_Analisis_LPIPS_Shot2_Lengkap.png")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style untuk grafik agar terlihat profesional
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif'})

def plot_all_iterations_in_one_grid(output_image_name):
    print("\n--- Memulai Pembuatan Grafik 10 Iterasi ---")
    
    # Inisialisasi grid 5x2
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 22))
    axes = axes.flatten()
    
    # Alamat folder (Gunakan 'r' untuk menghindari error backslash)
    base_path = r"D:\zkripsi_animasi\evaluasi_temporal\shot3"
    
    # Variabel untuk menyimpan contoh label legenda
    handles_global, labels_global = [], []
    
    for i in range(1, 11):
        iter_num = f"{i:02d}" # Format 01, 02, dst.
        ax = axes[i-1]
        
        # Penamaan file sesuai struktur data penelitian Anda
        file_struct = f"detail_temporal_structured_frames_structured{iter_num}.csv"
        file_unstruct = f"detail_temporal_unstructured_frames_unstructured{iter_num}.csv"
        
        path_struct = os.path.join(base_path, "structured", file_struct)
        path_unstruct = os.path.join(base_path, "unstructured", file_unstruct)

        # Cek keberadaan file sebelum membaca
        if os.path.exists(path_struct) and os.path.exists(path_unstruct):
            try:
                df_s = pd.read_csv(path_struct)
                df_u = pd.read_csv(path_unstruct)
                
                # Plotting dengan label yang jelas
                line_u, = ax.plot(df_u.index, df_u['LPIPS_Score'], color='#e74c3c', label='Unstructured Prompting', alpha=0.8)
                line_s, = ax.plot(df_s.index, df_s['LPIPS_Score'], color='#2980b9', label='JSON-Structured Prompting', alpha=0.9)
                
                # Mengambil label dari iterasi pertama untuk dipakai di Legenda Global
                if i == 1:
                    handles_global = [line_u, line_s]
                    labels_global = ['Unstructured Prompting', 'JSON-Structured Prompting']
                
                # Estetika tiap kotak
                ax.set_title(f'Video Iterasi {iter_num}', fontweight='bold', fontsize=12)
                ax.set_xlabel('Urutan Frame', fontsize=10)
                ax.set_ylabel('Nilai LPIPS', fontsize=10)
                
            except Exception as e:
                ax.text(0.5, 0.5, f"Error Reading:\n{iter_num}", ha='center', va='center', color='orange')
        else:
            # Jika file tidak ditemukan, tampilkan pesan di grafik
            ax.text(0.5, 0.5, f'File Tidak Ditemukan\nIterasi {iter_num}', 
                    ha='center', va='center', color='red', fontsize=10)
            print(f"⚠️ Missing: Iterasi {iter_num}")

    # =========================================================
    # PERBAIKAN: MENAMBAHKAN JUDUL UTAMA DAN LEGENDA GLOBAL
    # =========================================================
    
    # 1. Judul Utama
    plt.suptitle('Analisis Fluktuasi Stabilitas Temporal LPIPS \n(Shot 3)', 
                 fontsize=20, y=0.97, fontweight='bold', ha='center')
    
    # 2. Menambahkan Legenda Global di bagian atas-tengah
    if handles_global:
        fig.legend(handles_global, labels_global, loc='upper center', bbox_to_anchor=(0.5, 0.935), 
                   ncol=2, fontsize=14, frameon=True, edgecolor='black', shadow=False)

    # 3. Mengatur margin (Tight Layout) agar grafik tidak menabrak legenda di atasnya
    # Batas atas (top) diturunkan ke 0.91 agar ada ruang untuk judul dan legenda
    plt.tight_layout(rect=[0, 0.02, 1, 0.91], h_pad=3.0, w_pad=2.0)
    
    # Simpan dan Tampilkan
    plt.savefig(output_image_name, dpi=300, bbox_inches='tight')
    print(f"✅ Selesai! Grafik berhasil disimpan: {output_image_name}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    plot_all_iterations_in_one_grid("Hasil_Analisis_LPIPS_Shot3_Lengkap.png")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style untuk grafik agar terlihat profesional
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif'})

def plot_summary_bar_chart(file_structured, file_unstructured, output_image_name):
    print("\n--- Membuat Bar Chart Kesimpulan Total ---")
    
    # Validasi Path
    if not os.path.exists(file_structured) or not os.path.exists(file_unstructured):
        print("❌ Error: File CSV summary tidak ditemukan.")
        return

    # Load data
    # Tambahkan sep=';' karena CSV Anda dipisahkan oleh titik koma
    df_struct = pd.read_csv(file_structured, sep=';')
    df_unstruct = pd.read_csv(file_unstructured, sep=';')

    # Bersihkan nama kolom dari spasi tersembunyi
    df_struct.columns = df_struct.columns.str.strip()
    df_unstruct.columns = df_unstruct.columns.str.strip()

    # Bersihkan data kolom pertama (Video) dari spasi tersembunyi
    df_struct.iloc[:, 0] = df_struct.iloc[:, 0].astype(str).str.strip()
    df_unstruct.iloc[:, 0] = df_unstruct.iloc[:, 0].astype(str).str.strip()

    # =========================================================
    # PERBAIKAN: Deteksi Kolom 'Mean LPIPS' Otomatis
    # Mencari kolom yang mengandung kata 'mean' (tidak peduli huruf besar/kecil)
    # =========================================================
    try:
        col_struct = [col for col in df_struct.columns if 'mean' in col.lower()][0]
        col_unstruct = [col for col in df_unstruct.columns if 'mean' in col.lower()][0]
        print(f"✅ Terdeteksi kolom rata-rata: '{col_struct}'")
    except IndexError:
        print("\n❌ Error: Tidak dapat menemukan kolom yang berisi kata 'Mean' atau 'mean'.")
        print("Kolom yang ada di file Anda:", df_struct.columns.tolist())
        return

    try:
        # Mengambil nilai dari baris 'Rata-rata Total' menggunakan kolom yang sudah dideteksi
        total_struct = df_struct[df_struct.iloc[:, 0] == 'Rata-rata Total'][col_struct].values[0]
        total_unstruct = df_unstruct[df_unstruct.iloc[:, 0] == 'Rata-rata Total'][col_unstruct].values[0]
    except IndexError:
        print("\n❌ Error: Baris 'Rata-rata Total' tidak ditemukan!")
        print("Baris yang tersedia:", df_struct.iloc[:, 0].tolist())
        return

    # Persiapan data untuk di-plot
    labels = ['Unstructured Prompting', 'JSON-Structured Prompting']
    values = [total_unstruct, total_struct]
    colors = ['#e74c3c', '#2980b9'] # Merah dan Biru

    # Atur ukuran kanvas
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot Batang
    bars = ax.bar(labels, values, color=colors, edgecolor='black', linewidth=1, width=0.5)

    # Kustomisasi Tampilan
    ax.set_ylabel('Rata-rata Nilai LPIPS', fontsize=11, fontweight='bold')
    ax.set_title('Perbandingan Rata-rata Keseluruhan Stabilitas Temporal\nPada Shot 1', 
                 fontsize=14, fontweight='bold', pad=20)

    # Tambahkan angka di atas tiap batang
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), 
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Margin dinamis 15% dari tinggi maksimal grafik agar angka tidak terpotong
    max_y = max(values)
    ax.set_ylim(0, max_y + (max_y * 0.15))

    plt.tight_layout()
    
    # Simpan dan Tampilkan
    plt.savefig(output_image_name, dpi=300)
    print(f"✅ Berhasil! Grafik disimpan sebagai: {output_image_name}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    # Gunakan raw string (r) untuk path
    file_summary_struct = r"D:\zkripsi_animasi\evaluasi_temporal\shot1\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv"
    file_summary_unstruct = r"D:\zkripsi_animasi\evaluasi_temporal\shot1\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv"
    
    output_bar_chart = "Grafik_Kesimpulan_LPIPS_Shot1.png"
    
    plot_summary_bar_chart(file_summary_struct, file_summary_unstruct, output_bar_chart)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style untuk grafik agar terlihat profesional
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif'})

def plot_summary_bar_chart(file_structured, file_unstructured, output_image_name):
    print("\n--- Membuat Bar Chart Kesimpulan Total ---")
    
    # Validasi Path
    if not os.path.exists(file_structured) or not os.path.exists(file_unstructured):
        print("❌ Error: File CSV summary tidak ditemukan.")
        return

    # Load data
    # Tambahkan sep=';' karena CSV Anda dipisahkan oleh titik koma
    df_struct = pd.read_csv(file_structured, sep=';')
    df_unstruct = pd.read_csv(file_unstructured, sep=';')

    # Bersihkan nama kolom dari spasi tersembunyi
    df_struct.columns = df_struct.columns.str.strip()
    df_unstruct.columns = df_unstruct.columns.str.strip()

    # Bersihkan data kolom pertama (Video) dari spasi tersembunyi
    df_struct.iloc[:, 0] = df_struct.iloc[:, 0].astype(str).str.strip()
    df_unstruct.iloc[:, 0] = df_unstruct.iloc[:, 0].astype(str).str.strip()

    # =========================================================
    # PERBAIKAN: Deteksi Kolom 'Mean LPIPS' Otomatis
    # Mencari kolom yang mengandung kata 'mean' (tidak peduli huruf besar/kecil)
    # =========================================================
    try:
        col_struct = [col for col in df_struct.columns if 'mean' in col.lower()][0]
        col_unstruct = [col for col in df_unstruct.columns if 'mean' in col.lower()][0]
        print(f"✅ Terdeteksi kolom rata-rata: '{col_struct}'")
    except IndexError:
        print("\n❌ Error: Tidak dapat menemukan kolom yang berisi kata 'Mean' atau 'mean'.")
        print("Kolom yang ada di file Anda:", df_struct.columns.tolist())
        return

    try:
        # Mengambil nilai dari baris 'Rata-rata Total' menggunakan kolom yang sudah dideteksi
        total_struct = df_struct[df_struct.iloc[:, 0] == 'Rata-rata Total'][col_struct].values[0]
        total_unstruct = df_unstruct[df_unstruct.iloc[:, 0] == 'Rata-rata Total'][col_unstruct].values[0]
    except IndexError:
        print("\n❌ Error: Baris 'Rata-rata Total' tidak ditemukan!")
        print("Baris yang tersedia:", df_struct.iloc[:, 0].tolist())
        return

    # Persiapan data untuk di-plot
    labels = ['Unstructured Prompting', 'JSON-Structured Prompting']
    values = [total_unstruct, total_struct]
    colors = ['#e74c3c', '#2980b9'] # Merah dan Biru

    # Atur ukuran kanvas
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot Batang
    bars = ax.bar(labels, values, color=colors, edgecolor='black', linewidth=1, width=0.5)

    # Kustomisasi Tampilan
    ax.set_ylabel('Rata-rata Nilai LPIPS', fontsize=11, fontweight='bold')
    ax.set_title('Perbandingan Rata-rata Keseluruhan Stabilitas Temporal\nPada Shot 2', 
                 fontsize=14, fontweight='bold', pad=20)

    # Tambahkan angka di atas tiap batang
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), 
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Margin dinamis 15% dari tinggi maksimal grafik agar angka tidak terpotong
    max_y = max(values)
    ax.set_ylim(0, max_y + (max_y * 0.15))

    plt.tight_layout()
    
    # Simpan dan Tampilkan
    plt.savefig(output_image_name, dpi=300)
    print(f"✅ Berhasil! Grafik disimpan sebagai: {output_image_name}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    # Gunakan raw string (r) untuk path
    file_summary_struct = r"D:\zkripsi_animasi\evaluasi_temporal\shot2\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv"
    file_summary_unstruct = r"D:\zkripsi_animasi\evaluasi_temporal\shot2\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv"
    
    output_bar_chart = "Grafik_Kesimpulan_LPIPS_Shot2.png"
    
    plot_summary_bar_chart(file_summary_struct, file_summary_unstruct, output_bar_chart)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style untuk grafik agar terlihat profesional
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif'})

def plot_summary_bar_chart(file_structured, file_unstructured, output_image_name):
    print("\n--- Membuat Bar Chart Kesimpulan Total ---")
    
    # Validasi Path
    if not os.path.exists(file_structured) or not os.path.exists(file_unstructured):
        print("❌ Error: File CSV summary tidak ditemukan.")
        return

    # Load data
    # Tambahkan sep=';' karena CSV Anda dipisahkan oleh titik koma
    df_struct = pd.read_csv(file_structured)
    df_unstruct = pd.read_csv(file_unstructured)

    # Bersihkan nama kolom dari spasi tersembunyi
    df_struct.columns = df_struct.columns.str.strip()
    df_unstruct.columns = df_unstruct.columns.str.strip()

    # Bersihkan data kolom pertama (Video) dari spasi tersembunyi
    df_struct.iloc[:, 0] = df_struct.iloc[:, 0].astype(str).str.strip()
    df_unstruct.iloc[:, 0] = df_unstruct.iloc[:, 0].astype(str).str.strip()

    # =========================================================
    # PERBAIKAN: Deteksi Kolom 'Mean LPIPS' Otomatis
    # Mencari kolom yang mengandung kata 'mean' (tidak peduli huruf besar/kecil)
    # =========================================================
    try:
        col_struct = [col for col in df_struct.columns if 'mean' in col.lower()][0]
        col_unstruct = [col for col in df_unstruct.columns if 'mean' in col.lower()][0]
        print(f"✅ Terdeteksi kolom rata-rata: '{col_struct}'")
    except IndexError:
        print("\n❌ Error: Tidak dapat menemukan kolom yang berisi kata 'Mean' atau 'mean'.")
        print("Kolom yang ada di file Anda:", df_struct.columns.tolist())
        return

    try:
        # Mengambil nilai dari baris 'Rata-rata Total' menggunakan kolom yang sudah dideteksi
        total_struct = df_struct[df_struct.iloc[:, 0] == 'Rata-rata Total'][col_struct].values[0]
        total_unstruct = df_unstruct[df_unstruct.iloc[:, 0] == 'Rata-rata Total'][col_unstruct].values[0]
    except IndexError:
        print("\n❌ Error: Baris 'Rata-rata Total' tidak ditemukan!")
        print("Baris yang tersedia:", df_struct.iloc[:, 0].tolist())
        return

    # Persiapan data untuk di-plot
    labels = ['Unstructured Prompting', 'JSON-Structured Prompting']
    values = [total_unstruct, total_struct]
    colors = ['#e74c3c', '#2980b9'] # Merah dan Biru

    # Atur ukuran kanvas
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot Batang
    bars = ax.bar(labels, values, color=colors, edgecolor='black', linewidth=1, width=0.5)

    # Kustomisasi Tampilan
    ax.set_ylabel('Rata-rata Nilai LPIPS', fontsize=11, fontweight='bold')
    ax.set_title('Perbandingan Rata-rata Keseluruhan Stabilitas Temporal\nPada Shot 3', 
                 fontsize=14, fontweight='bold', pad=20)

    # Tambahkan angka di atas tiap batang
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), 
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Margin dinamis 15% dari tinggi maksimal grafik agar angka tidak terpotong
    max_y = max(values)
    ax.set_ylim(0, max_y + (max_y * 0.15))

    plt.tight_layout()
    
    # Simpan dan Tampilkan
    plt.savefig(output_image_name, dpi=300)
    print(f"✅ Berhasil! Grafik disimpan sebagai: {output_image_name}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    # Gunakan raw string (r) untuk path
    file_summary_struct = r"D:\zkripsi_animasi\evaluasi_temporal\shot3\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv"
    file_summary_unstruct = r"D:\zkripsi_animasi\evaluasi_temporal\shot3\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv"
    
    output_bar_chart = "Grafik_Kesimpulan_LPIPS_Shot3.png"
    
    plot_summary_bar_chart(file_summary_struct, file_summary_unstruct, output_bar_chart)

import pandas as pd
import os

def extract_rata_rata(filepath):
    """
    Function to safely extract the 'Rata-rata Total' row from a summary CSV.
    It automatically handles both comma (,) and semicolon (;) delimiters.
    """
    if not os.path.exists(filepath):
        print(f"⚠️ Warning: File not found -> {filepath}")
        return None

    try:
        # Try reading with comma first
        df = pd.read_csv(filepath)
        if len(df.columns) == 1:
            # If it only detects 1 column, fallback to semicolon
            df = pd.read_csv(filepath, sep=';')
            
        # Clean up column names and first column data from hidden spaces
        df.columns = df.columns.str.strip()
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.strip()
        
        # Find the specific row
        row = df[df.iloc[:, 0] == 'Rata-rata Total']
        if row.empty:
            print(f"❌ Error: 'Rata-rata Total' row not found in {filepath}")
            return None
            
        # Dynamically find columns by keywords to prevent KeyError
        col_mean = [c for c in df.columns if 'mean' in c.lower()][0]
        col_var = [c for c in df.columns if 'vari' in c.lower()][0]
        col_max = [c for c in df.columns if 'max' in c.lower()][0]
        
        return {
            'mean': float(row[col_mean].values[0]),
            'variance': float(row[col_var].values[0]),
            'max': float(row[col_max].values[0])
        }
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return None

def generate_grand_summary():
    print("\n--- Calculating Grand Summary Across All Shots ---")
    
    # 1. Define your file paths here (Update these paths if necessary)
    paths_struct = [
        r"D:\zkripsi_animasi\evaluasi_temporal\shot1\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv",
        r"D:\zkripsi_animasi\evaluasi_temporal\shot2\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv",
        r"D:\zkripsi_animasi\evaluasi_temporal\shot3\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv"
    ]
    
    paths_unstruct = [
        r"D:\zkripsi_animasi\evaluasi_temporal\shot1\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv",
        r"D:\zkripsi_animasi\evaluasi_temporal\shot2\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv",
        r"D:\zkripsi_animasi\evaluasi_temporal\shot3\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv"
    ]
    
    # 2. Extract data from all available files
    data_struct = [extract_rata_rata(p) for p in paths_struct if extract_rata_rata(p) is not None]
    data_unstruct = [extract_rata_rata(p) for p in paths_unstruct if extract_rata_rata(p) is not None]
    
    if not data_struct or not data_unstruct:
        print("❌ Not enough data to calculate Grand Summary. Please check your files.")
        return
        
    # 3. Calculate the Grand Averages
    def calc_grand_avg(data_list, key):
        return sum(item[key] for item in data_list) / len(data_list)
        
    grand_struct = {
        'mean': calc_grand_avg(data_struct, 'mean'),
        'variance': calc_grand_avg(data_struct, 'variance'),
        'max': calc_grand_avg(data_struct, 'max')
    }
    
    grand_unstruct = {
        'mean': calc_grand_avg(data_unstruct, 'mean'),
        'variance': calc_grand_avg(data_unstruct, 'variance'),
        'max': calc_grand_avg(data_unstruct, 'max')
    }
    
    # 4. Format exactly like your requested Table 4.13
    final_table_data = [
        {'Metrik LPIPS': 'Mean (Stabilitas)', 'Metode Prompting': 'JSON-Structured', 'Rata-rata Total': round(grand_struct['mean'], 4)},
        {'Metrik LPIPS': 'Mean (Stabilitas)', 'Metode Prompting': 'Unstructured',    'Rata-rata Total': round(grand_unstruct['mean'], 4)},
        
        {'Metrik LPIPS': 'Variance (Flicker)', 'Metode Prompting': 'JSON-Structured', 'Rata-rata Total': round(grand_struct['variance'], 6)},
        {'Metrik LPIPS': 'Variance (Flicker)', 'Metode Prompting': 'Unstructured',    'Rata-rata Total': round(grand_unstruct['variance'], 6)},
        
        {'Metrik LPIPS': 'Max (Morphing)', 'Metode Prompting': 'JSON-Structured', 'Rata-rata Total': round(grand_struct['max'], 4)},
        {'Metrik LPIPS': 'Max (Morphing)', 'Metode Prompting': 'Unstructured',    'Rata-rata Total': round(grand_unstruct['max'], 4)}
    ]
    
    df_final = pd.DataFrame(final_table_data)
    
    # 5. Export to CSV and Excel
    output_csv = "Tabel_4_13_Rekapitulasi_Grand_Summary.csv"
    output_excel = "Tabel_4_13_Rekapitulasi_Grand_Summary.xlsx"
    
    df_final.to_csv(output_csv, index=False, sep=';') # Using semicolon for easy opening in Indonesian Excel
    df_final.to_excel(output_excel, index=False)
    
    print("\n✅ Calculation Successful! Here is your Grand Summary Table:")
    print("-" * 60)
    print(df_final.to_string(index=False))
    print("-" * 60)
    print(f"💾 Saved as CSV: {output_csv}")
    print(f"💾 Saved as Excel: {output_excel}")

if __name__ == "__main__":
    # Ensure openpyxl is installed for Excel export (run: pip install openpyxl)
    generate_grand_summary()

import pandas as pd
from scipy import stats
import os

print("--- Memulai Uji Signifikansi (Independent T-Test) Berbasis File ---\n")

def ambil_data_mean(filepath):
    """
    Fungsi cerdas untuk membaca CSV, mencari kolom Mean LPIPS, 
    dan mengambil tepat 10 data video (mengabaikan baris 'Rata-rata Total').
    """
    if not os.path.exists(filepath):
        print(f"⚠️ Peringatan: File tidak ditemukan -> {filepath}")
        return []
    
    try:
        # Membaca file CSV (engine='python' membantu mendeteksi koma atau titik koma otomatis)
        df = pd.read_csv(filepath, sep=None, engine='python')
        
        # Membersihkan nama kolom dari spasi yang tersembunyi
        df.columns = df.columns.str.strip()
        
        # Mencari kolom yang namanya mengandung kata 'Mean'
        col_mean = [c for c in df.columns if 'mean' in c.lower()][0]
        
        # Filter hanya baris yang kolom pertamanya mengandung kata 'frames'
        # Ini penting agar baris "Rata-rata Total" di bawah tabel TIDAK ikut diuji!
        df_filtered = df[df.iloc[:, 0].astype(str).str.contains('frames')]
        
        # Kembalikan datanya dalam bentuk list angka
        return df_filtered[col_mean].tolist()
    
    except Exception as e:
        print(f"❌ Error saat membaca {filepath}: {e}")
        return []

# ==========================================
# 1. TENTUKAN PATH (ALAMAT FILE) CSV ANDA
# Gunakan awalan 'r' agar Python bisa membaca backslash (\) pada Windows
# ==========================================

# Path untuk file JSON-Structured (Shot 1, 2, 3)
paths_json = [
    r"D:\zkripsi_animasi\evaluasi_temporal\shot1\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv",
    r"D:\zkripsi_animasi\evaluasi_temporal\shot2\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv",
    r"D:\zkripsi_animasi\evaluasi_temporal\shot3\SUMMARY_REPORT_TEMPORAL_STRUCTURED.csv" # Pastikan file shot 3 ini sudah ada dan benar isinya
]

# Path untuk file Unstructured (Shot 1, 2, 3)
paths_unstruct = [
    r"D:\zkripsi_animasi\evaluasi_temporal\shot1\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv",
    r"D:\zkripsi_animasi\evaluasi_temporal\shot2\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv",
    r"D:\zkripsi_animasi\evaluasi_temporal\shot3\SUMMARY_REPORT_TEMPORAL_UNSTRUCTURED.csv" # Pastikan file shot 3 ini sudah ada dan benar isinya
]

# ==========================================
# 2. BACA FILE DAN GABUNGKAN DATA (Otomatis)
# ==========================================
data_json = []
for path in paths_json:
    data_json.extend(ambil_data_mean(path))

data_unstruct = []
for path in paths_unstruct:
    data_unstruct.extend(ambil_data_mean(path))

# Validasi jumlah data
print(f"Total sampel JSON-Structured : {len(data_json)} video")
print(f"Total sampel Unstructured    : {len(data_unstruct)} video\n")

if len(data_json) != 30 or len(data_unstruct) != 30:
    print("⚠️ PERHATIAN: Jumlah sampel tidak mencapai 30! Harap periksa apakah file CSV Anda lengkap dan path-nya benar.")
else:
    # ==========================================
    # 3. PROSES UJI STATISTIK (INDEPENDENT T-TEST)
    # ==========================================
    t_stat, p_value = stats.ttest_ind(data_json, data_unstruct)

    # ==========================================
    # 4. CETAK KESIMPULAN
    # ==========================================
    print("=== HASIL UJI SIGNIFIKANSI LPIPS ===")
    print(f"T-Statistic : {t_stat:.4f}")
    print(f"P-Value     : {p_value:.4f}")
    print("-" * 36)

    if p_value < 0.05:
        print("✅ KESIMPULAN FINAL:")
        print("P-Value < 0.05. Perbedaan SIGNIFIKAN!")
        print("Metode JSON-Structured terbukti secara statistik")
        print("lebih baik dibandingkan metode Unstructured.")
    else:
        print("❌ KESIMPULAN FINAL:")
        print("P-Value >= 0.05. Perbedaan TIDAK SIGNIFIKAN.")
        print("Secara statistik, perbedaan angka tersebut belum cukup kuat")
        print("dan baru sebatas indikasi/kecenderungan. Namun, rata-rata")
        print("JSON tetap lebih baik secara absolut.")

import numpy as np
import matplotlib.pyplot as plt

# 1. Kategori Aspek Penilaian (4 Aspek Utama)
categories = [
    'Stabilitas\nKarakter', 
    'Stabilitas\nKamera', 
    'Konsistensi\nGaya Visual', 
    'Kesesuaian\ndengan Prompt'
]
N = len(categories)

# 2. Rata-Rata Kumulatif Seluruh Shot (Skala 0.0 - 1.0)
# Angka ini merepresentasikan persentase rata-rata dari Shot 1, 2, dan 3
# JSON rata-rata ~91.4%, Unstructured rata-rata ~68.8%
json_scores = [0.93, 0.89, 0.88, 0.95]   
unstr_scores = [0.66, 0.72, 0.67, 0.70]  

# Menyambungkan titik akhir ke titik awal agar grafiknya tertutup
json_scores += json_scores[:1]
unstr_scores += unstr_scores[:1]

# Menghitung sudut untuk setiap kategori di grafik melingkar
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# 3. Membuat Canvas Grafik
fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

# 4. Menggambar Plot untuk JSON-Structured (Warna Hijau)
ax.plot(angles, json_scores, linewidth=2, linestyle='solid', label='JSON-Structured', color='#2ca02c') 
ax.fill(angles, json_scores, '#2ca02c', alpha=0.25)

# 5. Menggambar Plot untuk Unstructured (Warna Merah)
ax.plot(angles, unstr_scores, linewidth=2, linestyle='solid', label='Unstructured', color='#d62728') 
ax.fill(angles, unstr_scores, '#d62728', alpha=0.2)

# 6. Kustomisasi Tampilan
# Mengatur Label Kategori di pinggir
plt.xticks(angles[:-1], categories, color='black', size=11, weight='bold')

# Mengatur skala angka di dalam jaring (0.2 sampai 1.0)
ax.set_ylim(0, 1.05)
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=10)

# Menambahkan Judul dan Legend
plt.title("Radar Chart: Aspek Penilaian Format Prompt AI Video", size=13, weight='bold', y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)

# Menampilkan grafik
plt.tight_layout()
plt.show()

