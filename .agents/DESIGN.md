# 🎨 Design System & UI/UX Guidelines — Audira Download Manager

## 1. Filosofi Desain: Liquid Glass & Modern Studio

Audira Download Manager mengusung estetika **Liquid Glass** yang dipadukan dengan aksen **Electric Neon** khas ekosistem AUDIRA:

- **Material Permukaan**: Efek *Mica* di Windows 11 dan *Vibrancy* di macOS dengan transparansi lembut yang menyatu dengan latar belakang desktop.
- **Glass Panel**: Border berkilau `rgba(255, 255, 255, 0.08)` dengan background semi-transparan `rgba(20, 22, 30, 0.75)` dan backdrop blur.
- **Micro-Interactions**: Transisi halus 160ms–220ms menggunakan library `motion/react`.
- **Virtual List Table**: Menggunakan `@tanstack/react-virtual` agar daftar ribuan berkas tetap meluncur mulus pada 60+ FPS tanpa hambatan render DOM.

---

## 2. Token Warna & Status Lisensi

| Elemen | Token CSS / Nilai Warna | Indikasi Visual |
| :--- | :--- | :--- |
| **Pro License Active** | `#fde047` / Gold Neon (`rgba(234, 179, 8, 0.2)`) | Status langganan Pro seumur hidup / aktif. |
| **Trial Mode** | `#93c5fa` / Cyan Electric (`rgba(59, 130, 246, 0.15)`) | Masa evaluasi uji coba 14 hari. |
| **Free / Expired** | `#f87171` / Coral Red (`rgba(239, 68, 68, 0.15)`) | Masa trial habis, paywall aktif. |
| **Speed Accelerator** | `#2ed3a9` / Matrix Green | Indikator kecepatan turbo work-stealing. |
| **Background Dark** | `#0b0d14` / `#131622` | Permukaan panel utama gelap premium. |

---

## 3. Anti-Slop Guidelines (Kepatuhan AUDIRA)

- **Hindari Tampilan AI Generik**: Jangan gunakan border tebal monoton atau card kosong tanpa hierarki kontras.
- **Densitas Informasi Seimbang**: Menyediakan opsi baris *Comfortable* dan *Compact* sesuai preferensi pengguna pro.
- **Data-Driven States**: Setiap dialog dan modal harus menampilkan nilai nyata (misal: Machine HWID, sisa hari aktif, jumlah koneksi aktif), bukan teks placeholder fiktif.

