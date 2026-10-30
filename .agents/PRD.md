# 📋 Product Requirements Document (PRD) — Audira Download Manager (ADM)

## 1. Visi Produk

Audira Download Manager (ADM) dirancang sebagai aplikasi pengunduh berkas (*download accelerator*) desktop generasi baru yang menggabungkan performa mesin native tingkat rendah (**Rust**) dengan kenyamanan tampilan visual modern (**React 19 + Tauri 2**). ADM menjadi produk komersial unggulan ekosistem **AUDIRA** untuk menggantikan download manager warisan masa lalu (*Internet Download Manager / IDM*) dengan pendekatan tanpa iklan, tanpa telemetri pihak ketiga, akselerasi hingga 32 koneksi simultan, serta integrasi khusus model AI (Hugging Face) dan video 8K streaming.

---

## 2. Model Bisnis & Lisensi Komersial (Free vs PRO)

| Fitur | Audira Free Edition | Audira Trial Edition (14 Hari) | Audira PRO (Berbayar) |
| :--- | :---: | :---: | :---: |
| **Batas Koneksi Paralel** | Maks. 6 koneksi simultan | Maks. 8 koneksi simultan | **Maks. 32 koneksi simultan (Turbo Work-Stealing)** |
| **Kecepatan Download** | Dibatasi / Standard | Tanpa batas kecepatan | **Maksimum Bandwidth (Full Line Speed)** |
| **Video & Audio Grabber** | Maksimal 1080p | Maksimal 1080p | **Resolusi 4K & 8K HDR + MP3 320kbps** |
| **Model AI Hugging Face** | 1 model per hari | Kuota terbatas | **Tanpa Batas (GGUF, SafeTensors, LoRA)** |
| **Scheduler & Auto Sleep/Shutdown** | ❌ Terkunci | ❌ Terkunci | **✅ Aktif Penuh** |
| **Machine ID Binding (HWID)** | Bebas | Bebas | **Terkunci Aman ke HWID Komputer** |
| **Dukungan Pengguna** | Dokumentasi & Komunitas | Komunitas | **Prioritas VIP WhatsApp (+62 821-1200-1600)** |

---

## 3. Alur Pengalaman Pengguna (User Flow)

1. **First-Run Experience**:
   - Pengguna disambut oleh *Welcome Wizard* bergaya Liquid Glass.
   - Otomatis mengaktifkan masa uji coba 14 hari (*Trial Period*).
   - Menampilkan status badge neon `[ TRIAL (14H) ⏳ ]` di bilah judul.
2. **Upgrade & Pembelian Lisensi**:
   - Pengguna mengklik badge lisensi atau menu *Aktivasi Lisensi PRO* di Settings.
   - Dialog menampilkan Machine HWID yang dapat disalin dengan satu klik.
   - Tombol *Beli Lisensi (WhatsApp)* mengarahkan langsung ke layanan penjualan AUDIRA (+62 821-1200-1600).
   - Pengguna menerima Serial Key resmi (format `ADM-LIFE-0-XXXXXXXXXXXXXXXX`) dan memasukkannya bersama Nama & Email.
   - Validasi kriptografis offline/online berjalan instan.
   - Badge seketika berubah menjadi `[ PRO ⭐ ]` berwarna emas neon dan seluruh batasan kecepatan/fitur terbuka penuh.
3. **Download Execution**:
   - Ekstensi browser (Chromium & Firefox) menangkap URL secara instan melalui Native Messaging (`id.my.audira.download.host`).
   - Mesin Rust menulis langsung ke file akhir (*sparse file NTFS* di Windows), menghilangkan waktu penggabungan berkas.

---

## 4. Metrik Kualitas & Reliabilitas

- **Crash Immunity**: Berkas tersimpan secara bertahap via SQLite WAL. Pemadaman listrik atau laptop mati tidak merusak berkas unduhan.
- **Resume Precision**: Validasi `If-Range` (ETag + Last-Modified) sebelum melanjutkan proses.
- **Memory Footprint**: Mengonsumsi RAM di bawah 80 MB saat berjalan di latar belakang (tray), jauh lebih efisien dibanding aplikasi berbasis Electron.

