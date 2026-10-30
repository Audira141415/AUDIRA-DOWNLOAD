# 📦 Feature Catalog — Audira Download Manager (ADM)

## 1. Akselerasi Multi-Koneksi (Work-Stealing)
- **Hingga 32 Koneksi Paralel (Pro)**: Membagi berkas unduhan menjadi segmen dinamis. Jika salah satu koneksi selesai atau terhambat, segmen terbesar lainnya otomatis dibelah dua (*dynamic midpoint split*).
- **Straight-to-Disk (Sparse File)**: Menulis berkas secara langsung ke offset akhir di hard disk via sparse file NTFS di Windows dan `fallocate` di Linux tanpa fase perakitan (*merging*) sementara yang lambat.
- **Auto-Throttling Per-Host**: Menyesuaikan koneksi secara cerdas jika server sumber memberlakukan limit HTTP 429 atau 503.

## 2. Sistem Lisensi Komersial (Audira PRO)
- **Modal Aktivasi Lisensi**: Input serial key, nama pemilik, dan email dengan feedback visual instan.
- **Machine HWID Copying**: Salin identifier hardware dengan 1 klik untuk pendaftaran lisensi terkunci.
- **Fitur Gating**:
  - Batas koneksi: 6 koneksi (Free), 8 koneksi (Trial 14 hari), 32 koneksi (Pro).
  - Akses Video 4K/8K & konversi audio murni MP3 320kbps.
  - Penjadwal unduhan malam hari dengan aksi otomatis matikan komputer (*shutdown / hibernate*).

## 3. Video & Audio Sniffer Terintegrasi
- **1.800+ Platform Didukung**: YouTube, Vimeo, TikTok, Bilibili, dan ribuan portal lainnya via `yt-dlp` terkelola.
- **Ekstraksi Multi-Format**: MP4, MKV, WebM, MP3, M4A, Opus, FLAC, WAV lengkap dengan subtitle, bab (*chapters*), dan thumbnail.

## 4. Pengunduh Model AI (Hugging Face)
- **Cari & Unduh Model LLM**: Menemukan model GGUF, SafeTensors, dan bobot AI langsung dari antarmuka aplikasi.
- **Verifikasi SHA-256 Otomatis**: Memastikan bobot model tidak korup sebelum diimpor ke LM Studio atau Ollama.

## 5. Integrasi Browser Multi-Platform
- **Ekstensi Manifest V3**: Menangkap tautan unduhan dari Chrome, Edge, Brave, Opera, Vivaldi, dan Firefox.
- **Native Host IPC**: Komunikasi berkecepatan tinggi via stdio JSON ke loopback HTTP Axum dengan pengamanan Bearer Token 256-bit.

