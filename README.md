# LPIPS Video Evaluation Platform

Aplikasi evaluasi stabilitas temporal video berbasis metrik **LPIPS (Learned Perceptual Image Patch Similarity)**. Dibangun untuk mendukung penelitian skripsi tentang perbandingan kualitas video yang dihasilkan oleh metode *JSON-Structured Prompting* vs *Unstructured Prompting* pada AI generatif animasi.

---

## Fitur Utama

- Upload video (.mp4, .avi, .mov) langsung dari browser
- Hitung metrik LPIPS antar-frame secara otomatis
- Tampilkan tiga metrik utama:
  - **Mean LPIPS** — indikator stabilitas temporal keseluruhan
  - **Variance** — indikator *flickering* (kedipan antar-frame)
  - **Max LPIPS** — indikator *morphing* ekstrem
- Visualisasi grafik fluktuasi LPIPS per pasang frame
- Tampilkan data mentah per frame (opsional)

---

## Struktur Proyek

```
app/
├── app.py                  # Aplikasi Streamlit (standalone, siap deploy)
├── requirements.txt        # Dependensi Python untuk deployment
├── extracted_code.py       # Script utilitas ekstraksi frame & analisis batch
│
├── backend/                # FastAPI backend (full-stack version)
│   ├── main.py             # Entry point FastAPI
│   ├── requirements.txt    # Dependensi backend
│   ├── core/
│   │   ├── config.py       # Konfigurasi aplikasi
│   │   └── database.py     # Setup SQLAlchemy + SQLite
│   ├── api/
│   │   └── routers/
│   │       ├── videos.py       # Endpoint upload & manajemen video
│   │       └── evaluations.py  # Endpoint evaluasi LPIPS & export Excel
│   ├── models/             # Model database SQLAlchemy
│   ├── schemas/            # Pydantic schemas
│   └── services/           # Business logic (video & LPIPS service)
│
└── frontend/               # React + Vite + TypeScript (full-stack version)
    ├── src/
    │   ├── App.tsx
    │   ├── pages/          # Halaman utama aplikasi
    │   ├── components/     # Komponen UI reusable
    │   ├── services/       # API calls ke backend
    │   └── store/          # State management (Zustand)
    ├── package.json
    └── vite.config.ts
```

---

## Cara Menjalankan

### Opsi 1: Streamlit (Paling Mudah)

```bash
# Install dependensi
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---

### Opsi 2: Full-Stack (FastAPI + React)

**Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API tersedia di `http://localhost:8000`  
Dokumentasi API: `http://localhost:8000/docs`

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Frontend tersedia di `http://localhost:5173`

---

## Deploy Online (Gratis)

Aplikasi Streamlit (`app.py`) dapat di-deploy gratis via **Streamlit Community Cloud**:

1. Fork atau clone repo ini ke akun GitHub kamu
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Login dengan GitHub
4. Klik **"New app"** → pilih repo ini → set main file: `app.py`
5. Klik **Deploy**

---

## Dependensi Utama

| Library | Fungsi |
|---|---|
| `streamlit` | UI framework web |
| `lpips` | Perhitungan metrik perseptual |
| `torch` / `torchvision` | Deep learning backbone (AlexNet) |
| `opencv-python-headless` | Pemrosesan video & frame |
| `numpy` / `matplotlib` | Komputasi & visualisasi |
| `fastapi` / `uvicorn` | REST API backend |
| `sqlalchemy` | ORM database |
| `react` / `vite` | Frontend UI |

---

## Metrik LPIPS

| Metrik | Interpretasi |
|---|---|
| **Mean LPIPS rendah** | Video stabil secara temporal |
| **Variance rendah** | Tidak ada flickering signifikan |
| **Max LPIPS rendah** | Tidak ada morphing ekstrem antar frame |

Nilai LPIPS berada di rentang `0.0` (identik) hingga `1.0` (sangat berbeda secara perseptual).

---

## Catatan

- Folder `backend/uploads/` dan `backend/frames/` tidak di-push ke GitHub (berisi data video penelitian berukuran besar)
- Database `lpips.db` dibuat otomatis saat backend pertama kali dijalankan
- Untuk deployment produksi, ganti SQLite dengan PostgreSQL

---

## Lisensi

MIT License — bebas digunakan untuk keperluan akademik dan penelitian.
