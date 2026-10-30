# 🛡️ Security & Licensing Integrity — Audira Download Manager

## 1. Proteksi Lisensi Kriptografis

1. **Anti-Keygen Asymmetric Secrecy**:
   Kunci lisensi divalidasi menggunakan formula kriptografi tanda tangan SHA-256 yang diperkuat *salt* rahasia inti AUDIRA. Pihak ketiga tidak dapat membuat generator serial key yang sah tanpa memiliki kunci induk resmi milik Founder Agus Dwi Rianto.
2. **Machine ID Binding (HWID)**:
   Mencegah pembajakan lisensi massal dengan mengaitkan kunci aktivasi ke identitas perangkat keras (Machine GUID + Hardware hash).
3. **Penyimpanan Status Terenkripsi**:
   Status lisensi tersimpan di SQLite lokal (`adm_license_v1`) dan diverifikasi ulang setiap kali aplikasi dibuka. Jika berkas database diubah secara ilegal, validasi tanda tangan otomatis gagal dan aplikasi beralih ke mode Free.

---

## 2. Keamanan IPC & Komunikasi Browser

1. **Local Loopback Only**:
   Server IPC (`axum`) hanya terikat pada `127.0.0.1` dan menolak seluruh lalu lintas jaringan eksternal.
2. **Bearer Token 256-Bit**:
   Setiap pertukaran data antara browser extension dan aplikasi desktop diotentikasi melalui token acak 256-bit yang disimpan di direktori data pengguna (`ipc.json`).
3. **Integritas Binary Pihak Ketiga**:
   Pemasangan dan pembaruan otomatis alat eksternal (`yt-dlp` dan `ffmpeg`) selalu divalidasi checksum SHA-256 resminya sebelum dieksekusi di komputer pengguna.

