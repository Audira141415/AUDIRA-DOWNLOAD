# 🏛️ System Architecture — Audira Download Manager (ADM)

```mermaid
flowchart TD
    subgraph Browser["Browser Extension (MV3)"]
        CS["Content Script / Sniffer"]
        SW["Background Service Worker"]
        CS --> SW
    end

    subgraph NativeBridge["Native Messaging Host"]
        NH["prism-native-host.exe (Rust)"]
        SW <-->|stdio JSON| NH
    end

    subgraph DesktopApp["Audira Download Manager (Tauri 2 + Rust)"]
        IPC["Axum HTTP IPC (127.0.0.1 + Bearer Token)"]
        NH <-->|Loopback HTTP| IPC
        
        MGR["Core Manager (prism-core)"]
        IPC --> MGR
        
        DB[("SQLite WAL (prism.db)")]
        LIC["Licensing Manager (HMAC-SHA256 / Ed25519)"]
        ENG["Engine (Multi-segment HTTP/FTP/HLS/DASH)"]
        VID["Video Service (yt-dlp + ffmpeg)"]
        TOR["Torrent Engine (librqbit)"]
        
        MGR --> DB
        MGR --> LIC
        MGR --> ENG
        MGR --> VID
        MGR --> TOR
    end

    subgraph UI["React 19 + TypeScript + Vite UI"]
        VIEW["Liquid Glass UI (Zustand + Motion)"]
        MODAL["LicenseModal & Paywall Gatekeeper"]
        VIEW <-->|Tauri IPC Commands & Events| MGR
    end
```

---

## 1. Komponen Inti Monorepo

| Modul | Path | Bahasa | Fungsi Utama |
| :--- | :--- | :--- | :--- |
| **`crates/prism-engine`** | `crates/prism-engine/` | Rust | Mesin pengunduh multi-segmen paralel (work-stealing), token-bucket speed limiter, sparse writer NTFS. |
| **`crates/prism-core`** | `crates/prism-core/` | Rust | Logika bisnis, database SQLite, manajer antrean/penjadwal, dan **submodul lisensi kriptografis (`licensing.rs`)**. |
| **`crates/prism-native-host`** | `crates/prism-native-host/` | Rust | Binary jembatan Native Messaging browser dengan aplikasi desktop. |
| **`crates/prism-video`** | `crates/prism-video/` | Rust | Manajemen binary `yt-dlp` dan `ffmpeg` otomatis untuk ekstraksi audio/video streaming. |
| **`crates/prism-torrent`** | `crates/prism-torrent/` | Rust | Dukungan berkas torrent dan magnet links via `librqbit`. |
| **`app/`** | `app/` | TS / React 19 | Antarmuka desktop modern (Tauri 2) dengan modal aktivasi lisensi, tabel unduhan tervirtualisasi, dan sistem tema. |
| **`extension/`** | `extension/` | TS / MV3 | Ekstensi browser multi-browser (Chrome, Edge, Brave, Opera, Firefox). |

---

## 2. Arsitektur Mesin Lisensi (`crates/prism-core/src/licensing.rs`)

1. **Machine HWID**:
   Mengambil identifier unik perangkat (Windows: `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`; Linux: `/etc/machine-id`; macOS: hardware ID hash). Diformat sebagai `ADM-XXXX-XXXX-XXXX-XXXX`.
2. **Signature Formula**:
   ```
   Signature = SHA256(AUDIRA_SECRET_SALT + TIER + OWNER_NAME + EMAIL + EXPIRES_AT)[0..16]
   Key Format = ADM-<TIER>-<EXPIRES_AT>-<SIGNATURE>
   ```
3. **Enforcement Gate**:
   - `spawn_engine`: Membatasi jumlah koneksi per unduhan sesuai `license.maxConnections`.
   - `scheduler`: Mengunci aksi otomatis shutdown/sleep jika `!license.isPro`.
   - `video_probe`: Membatasi opsi kualitas resolusi di atas 1080p jika `!license.isPro`.

