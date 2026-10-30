# 🚀 AUDIRA Download Manager (ADM) — Project Agent Hub

> **Audira Download Manager (ADM)** adalah aplikasi *High-Performance Multi-Connection Download Accelerator, 8K Video Sniffer, dan AI Model Downloader* generasi baru yang dilengkapi dengan sistem **Commercial Cryptographic Licensing (Audira PRO)**.

---

## 1. Identitas & Kepemilikan Resmi

- **Nama Produk**: **Audira Download Manager (ADM)**
- **Brand Ekosistem**: **AUDIRA**
- **Founder & Lead Architect**: **Agus Dwi Rianto**
- **Badan Usaha**: **Audira Multimedia Digital / Audira Sukses Mandiri**
- **Website Resmi**: [https://audira.my.id](https://audira.my.id)
- **Portal Pembelian / Halaman Produk**: [https://audira.my.id/download-manager](https://audira.my.id/download-manager)
- **Email Kontak**: [agusdwirianto@gmail.com](mailto:agusdwirianto@gmail.com)
- **WhatsApp Hotline & Billing**: [+62 821-1200-1600](https://wa.me/6282112001600)

---

## 2. Peta Dokumen Utama (`.agents/`)

| Dokumen | Deskripsi |
| :--- | :--- |
| **[`PRD.md`](file:///f:/AUDIRA-DOWNLOAD/.agents/PRD.md)** | Product Requirement Document: Visi produk, segmentasi Free vs PRO, use case, dan paywall flow. |
| **[`ARCHITECTURE.md`](file:///f:/AUDIRA-DOWNLOAD/.agents/ARCHITECTURE.md)** | Arsitektur teknis lengkap (Rust Engine, Tauri 2, React 19, SQLite WAL, IPC Axum, Browser Extension). |
| **[`DESIGN.md`](file:///f:/AUDIRA-DOWNLOAD/.agents/DESIGN.md)** | Pedoman desain antarmuka Liquid Glass & Cyber-Studio, tipografi, warna aksen, dan anti-slop rules. |
| **[`SECURITY.md`](file:///f:/AUDIRA-DOWNLOAD/.agents/SECURITY.md)** | Mekanisme proteksi kriptografi Ed25519/HMAC-SHA256, HWID Machine Binding, IPC Bearer auth, dan verifikasi hash. |
| **[`brain/INDEX.md`](file:///f:/AUDIRA-DOWNLOAD/.agents/brain/INDEX.md)** | Manifest Long-Term Memory (LTM) proyek AUDIRA-DOWNLOAD. |
| **[`rules/brain_sync_protocol.md`](file:///f:/AUDIRA-DOWNLOAD/.agents/rules/brain_sync_protocol.md)** | Protokol wajib sinkronisasi LTM setiap kali ada penambahan atau perubahan kode. |

---

## 3. Komando Utama

- **Build Sidecar**: `node scripts/build-sidecar.mjs --debug`
- **Build Browser Extension**: `npm run build --prefix extension`
- **Jalankan Aplikasi Desktop (Dev)**: `npm run tauri:dev --prefix app`
- **Build Installer Rilis**: `npm run tauri:build --prefix app`
- **Generator Kunci Lisensi Admin**: `node scripts/generate-adm-license.mjs "<Nama>" "<Email>" [LIFE|YEAR]`

