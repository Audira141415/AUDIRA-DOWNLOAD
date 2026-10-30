# 🔄 Brain Sync Protocol — Audira Download Manager

Setiap kali agent AI melakukan perubahan struktural, menambah fitur baru, memodifikasi alur lisensi, atau memperbarui konfigurasi build di proyek `AUDIRA-DOWNLOAD`:

1. **Wajib Memperbarui Dokumen Terkait**:
   - Jika mengubah logika backend Rust: perbarui `crates/prism-core/src/licensing.rs` atau `jobs.rs`, dan catat di `.agents/ARCHITECTURE.md`.
   - Jika menambah UI baru: perbarui `.agents/DESIGN.md` dan `.agents/brain/FEATURE_CATALOG.md`.
   - Jika mengubah skema lisensi: sinkronkan generator `scripts/generate-adm-license.mjs` dan dokumentasi `.agents/SECURITY.md`.
2. **Uji Coba Wajib**:
   - Jalankan `cargo test -p prism-core licensing` untuk memastikan integritas formula kriptografi.
   - Jalankan `npm run typecheck --prefix app` untuk memastikan kesesuaian tipe antarmuka TypeScript.
3. **Penyelarasan Identitas Resmi**:
   - Selalu pertahankan atribusi resmi: **Agus Dwi Rianto (AUDIRA)**, organisasi **Audira Multimedia Digital / Audira Sukses Mandiri**, website **https://audira.my.id**, kontak **agusdwirianto@gmail.com**, WhatsApp **+62 821-1200-1600**.

