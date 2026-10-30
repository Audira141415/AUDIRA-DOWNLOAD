/**
 * AUDIRA DOWNLOAD MANAGER (ADM) : Anti-AI-Slop Engine & Interactive Simulator
 * Standards: Swiss Precision, Real Telemetry, Zero Fluff, Grounded in Kernel Code
 * Author: Agus Dwi Rianto (AUDIRA MDA / ASM)
 */

// Comprehensive i18n Dictionary (Indonesian & English)
const i18n = {
  id: {
    bannerText: "Rilis Resmi: Audira Download Manager v1.1.7 dengan akselerasi 32-koneksi paralel dan verifikasi SHA-256.",
    bannerLink: "Unduh Installer",
    navFeatures: "Fitur Arsitektur",
    navSimulator: "Simulasi 32-Segmen",
    navComparison: "Matriks Perbandingan",
    navPricing: "Paket Lisensi",
    navChecker: "Verifikasi Serial",
    navDownloads: "Unduhan Biner",
    navConsoleLogin: "Portal Fleet Admin",
    btnDownloads: "Unduh Klien",
    heroBadge: "Kernel Rust Mutakhir • 32 Segmen Simultan • Zero-Copy Sparse NTFS/ext4",
    heroTitle: "Akselerasi Download Turbo. <span>Nir-Jeda Merging.</span>",
    heroSubtitle: "Arsitektur pengunduh berkas multi-segmen berkinerja tinggi berbasis Rust & Tauri 2. Mengakselerasi kecepatan hingga 15× lipat, tahan crash dan pemadaman listrik, ekstraksi video 8K HDR, serta integrasi AI Hub Hugging Face.",
    btnHeroWin: "Unduh untuk Windows (23.4 MB)",
    btnHeroPro: "Beli Lisensi PRO Lifetime (Rp 99.000)",
    statConnVal: "32 Koneksi",
    statConnLbl: "Paralel Multi-Thread Turbo",
    statSpeedVal: "60.9 MB/s",
    statSpeedLbl: "Throughput Uji Rill Terverifikasi",
    statEngineVal: "100% Rust",
    statEngineLbl: "Memory-Safe tokio & reqwest",
    statMergeVal: "0 Detik",
    statMergeLbl: "Zero-Copy Sparse Pre-Allocation",
    simTitle: "Simulasi Real-Time Kernel Download Manager (Work-Stealing 32-Segmen)",
    simRestart: "Ulangi Simulasi",
    simPause: "Jeda",
    simResume: "Lanjutkan",
    tagFeatures: "Rekayasa Performa",
    titleFeatures: "Arsitektur Kernel Tingkat Rendah",
    descFeatures: "Diciptakan untuk memeras seluruh kapasitas bandwidth ISP tanpa membebani CPU, RAM, atau umur SSD.",
    feat1Title: "Dynamic Work-Stealing Multi-Connection",
    feat1Desc: "Membagi berkas menjadi 32 koneksi HTTP simultan. Ketika satu thread selesai lebih awal atau terhambat throttling server asal, thread tersebut otomatis membelah dua segmen terbesar yang tersisa sehingga seluruh 32 koneksi bekerja hingga byte terakhir.",
    feat2Title: "Zero-Copy Sparse File Pre-Allocation",
    feat2Desc: "Menghilangkan fase 'merging' sementara yang lambat. ADM langsung memesan ruang disk melalui OS native API (FSCTL_SET_SPARSE pada Windows NTFS dan fallocate pada Linux ext4/btrfs). Data langsung ditulis persis ke offset byte tujuan.",
    feat3Title: "Resiliensi Pemadaman Listrik (SQLite WAL)",
    feat3Desc: "Setiap blok byte yang berhasil diverifikasi dicatat secara atomik ke basis data SQLite Write-Ahead Logging (WAL). Jika laptop mati mendadak atau koneksi terputus, unduhan dilanjutkan persis di byte terakhir tanpa korupsi data.",
    feat4Title: "8K HDR & Audio Stream Grabber",
    feat4Desc: "Mendukung ekstraksi video dari 1.800+ portal (YouTube, TikTok, Bilibili) hingga resolusi 8K HDR 60fps dengan multiplexing audio-video lossless dan ekstraksi murni MP3 320kbps.",
    feat5Title: "Hugging Face AI Model Downloader",
    feat5Desc: "Pencarian dan pengunduhan bobot model LLM (GGUF, SafeTensors) langsung dari direktori aplikasi dengan verifikasi hash SHA-256 otomatis dan sinkronisasi ke folder model LM Studio.",
    feat6Title: "Integrasi Browser Native Messaging",
    feat6Desc: "Ekstensi untuk Chrome, Edge, Brave, Opera, dan Firefox berkomunikasi langsung dengan daemon Rust melalui pertukaran pesan stdin/stdout terenkripsi tanpa perantara server awan pihak ketiga.",
    tagComparison: "Matriks Perbandingan",
    titleComparison: "Perbandingan Rekayasa: ADM vs Solusi Konvensional",
    descComparison: "Mengapa para profesional IT dan power users memilih Audira Download Manager dibanding pengunduh warisan.",
    tagPricing: "Paket & Lisensi Komersial",
    titlePricing: "Pilihan Lisensi Resmi AUDIRA",
    descPricing: "Gunakan versi gratis untuk kebutuhan harian, atau tingkatkan ke Audira PRO untuk akselerasi 32-segmen tanpa kompromi.",
    tagChecker: "Validasi Lisensi",
    titleChecker: "Cek Keaslian & Pengikatan HWID Serial Key",
    descChecker: "Verifikasi status aktif, pemilik sah, dan masa berlaku lisensi langsung ke server otentikasi AUDIRA.",
    tagDownloads: "Berkas Instalasi Resmi",
    titleDownloads: "Unduh untuk Seluruh Platform",
    descDownloads: "Biner mandiri yang aman, bebas malware, dan ditandatangani secara digital.",
    tagFaq: "Knowledge Base & Tanya Jawab Teknis",
    titleFaq: "Jawaban Teknis Seputar Arsitektur ADM",
    descFaq: "Penjelasan mendalam seputar cara kerja kernel, enkripsi lisensi, dan konfigurasi ekstensi browser."
  },
  en: {
    bannerText: "Official Release: Audira Download Manager v1.1.7 featuring 32-connection parallel acceleration and SHA-256 integrity verification.",
    bannerLink: "Get Installer",
    navFeatures: "Core Architecture",
    navSimulator: "32-Segment Simulator",
    navComparison: "Feature Matrix",
    navPricing: "Licensing Plans",
    navChecker: "Verify Serial",
    navDownloads: "Platform Binaries",
    navConsoleLogin: "Admin Fleet Portal",
    btnDownloads: "Download Client",
    heroBadge: "Modern Rust Kernel • 32 Concurrent Segments • Zero-Copy Sparse NTFS/ext4",
    heroTitle: "Turbo-Charged Downloads. <span>Zero Merging Lag.</span>",
    heroSubtitle: "High-performance multi-segment download manager engine built in Rust & Tauri 2. Delivers up to 15× faster throughput, crash resilience against power outages, 8K HDR video extraction, and Hugging Face AI Hub integration.",
    btnHeroWin: "Download for Windows (23.4 MB)",
    btnHeroPro: "Purchase PRO Lifetime License ($7.00)",
    statConnVal: "32 Connections",
    statConnLbl: "Turbo Multi-Threaded Engine",
    statSpeedVal: "60.9 MB/s",
    statSpeedLbl: "Verified Real-World Benchmark",
    statEngineVal: "100% Rust",
    statEngineLbl: "Memory-Safe tokio & reqwest",
    statMergeVal: "0 Seconds",
    statMergeLbl: "Zero-Copy Sparse Pre-Allocation",
    simTitle: "Real-Time Download Kernel Simulation (32-Segment Work-Stealing)",
    simRestart: "Restart Simulation",
    simPause: "Pause",
    simResume: "Resume",
    tagFeatures: "Performance Engineering",
    titleFeatures: "Low-Level Kernel Architecture",
    descFeatures: "Built to utilize maximum ISP bandwidth without straining CPU, memory, or SSD lifespan.",
    feat1Title: "Dynamic Work-Stealing Multi-Connection",
    feat1Desc: "Splits file into 32 simultaneous HTTP segments. When one thread finishes early or suffers origin throttling, it dynamically bisects the largest unfinished segment so all 32 connections stay active until the final byte.",
    feat2Title: "Zero-Copy Sparse File Pre-Allocation",
    feat2Desc: "Eliminates slow temporary merging phases. ADM requests native OS sparse allocation (FSCTL_SET_SPARSE on Windows NTFS and fallocate on Linux ext4/btrfs). Data writes directly into exact final byte offsets.",
    feat3Title: "Power-Outage Resilience (SQLite WAL)",
    feat3Desc: "Every verified chunk byte is committed atomically into a SQLite Write-Ahead Logging (WAL) database. Abrupt power cuts or pulled cables will not corrupt downloads; resuming continues from the exact last byte.",
    feat4Title: "8K HDR & Audio Stream Grabber",
    feat4Desc: "Supports video extraction from 1,800+ portals (YouTube, TikTok, Bilibili) up to 8K HDR 60fps with lossless audio-video multiplexing or pure 320kbps MP3 audio stripping.",
    feat5Title: "Hugging Face AI Model Downloader",
    feat5Desc: "Search and download LLM weights (GGUF, SafeTensors) directly inside the app with automated SHA-256 hash verification and direct export to LM Studio directories.",
    feat6Title: "Browser Native Messaging Protocol",
    feat6Desc: "Extensions for Chrome, Edge, Brave, Opera, and Firefox communicate directly with the Rust daemon via encrypted stdin/stdout pipes with zero cloud telemetry.",
    tagComparison: "Feature Matrix",
    titleComparison: "Architectural Comparison: ADM vs Legacy Tools",
    descComparison: "Why IT professionals and developers choose Audira Download Manager over legacy download utilities.",
    tagPricing: "Commercial Plans",
    titlePricing: "Official AUDIRA Licensing",
    descPricing: "Use the Community Free edition for daily downloads, or upgrade to Audira PRO for unrestricted 32-segment turbo acceleration.",
    tagChecker: "License Verification",
    titleChecker: "Verify Serial Key Authenticity & HWID Binding",
    descChecker: "Check activation status, registered licensee, and validity directly against AUDIRA cryptographic authentication server.",
    tagDownloads: "Official Binaries",
    titleDownloads: "Available Across All Platforms",
    descDownloads: "Self-contained binaries, certified malware-free, and cryptographically signed.",
    tagFaq: "Technical Knowledge Base",
    titleFaq: "Technical FAQ on ADM Architecture",
    descFaq: "In-depth explanations of kernel internals, license cryptography, and browser extension setup."
  }
};

let currentLang = localStorage.getItem("adm-lang") || "id";

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initLanguage();
  initMobileDrawer();
  initSimulator();
  initFaqAccordion();
  initLicenseChecker();
});

// Theme Management
function initTheme() {
  const toggleBtn = document.getElementById("themeToggle");
  const savedTheme = localStorage.getItem("adm-theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      const next = current === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("adm-theme", next);
      updateThemeIcon(next);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.getElementById("themeIcon");
  if (!icon) return;
  if (theme === "light") {
    icon.innerHTML = `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>`;
  } else {
    icon.innerHTML = `<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>`;
  }
}

// Language Switcher
function initLanguage() {
  const langToggle = document.getElementById("langToggle");
  const langLabel = document.getElementById("langLabel");

  applyLanguage(currentLang);

  if (langToggle) {
    langToggle.addEventListener("click", () => {
      currentLang = currentLang === "id" ? "en" : "id";
      localStorage.setItem("adm-lang", currentLang);
      applyLanguage(currentLang);
    });
  }
}

function applyLanguage(lang) {
  const dict = i18n[lang] || i18n.id;
  const langLabel = document.getElementById("langLabel");
  if (langLabel) langLabel.innerText = lang.toUpperCase();

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.innerHTML = dict[key];
    }
  });
}

// Mobile Navigation Drawer
function initMobileDrawer() {
  const toggleBtn = document.getElementById("mobileNavToggle");
  const drawer = document.getElementById("mobileNavDrawer");

  if (!toggleBtn || !drawer) return;

  toggleBtn.addEventListener("click", () => {
    drawer.classList.toggle("open");
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && drawer.classList.contains("open")) {
      drawer.classList.remove("open");
    }
  });
}

function closeMobileDrawer() {
  const drawer = document.getElementById("mobileNavDrawer");
  if (drawer) drawer.classList.remove("open");
}

// -----------------------------------------------------------------------------
// Interactive 32-Segment Download Engine & Work-Stealing Simulator
// -----------------------------------------------------------------------------
let simInterval = null;
let simPaused = false;
const TOTAL_SEGMENTS = 32;
const FILE_SIZE_MB = 2680; // 2.68 GB Ubuntu ISO
let segments = [];
let downloadedBytes = 0;

function initSimulator() {
  const grid = document.getElementById("segmentsGrid");
  const sparseRow = document.getElementById("sparseBlocksRow");
  if (!grid) return;

  grid.innerHTML = "";
  if (sparseRow) sparseRow.innerHTML = "";
  segments = [];
  downloadedBytes = 0;

  for (let i = 0; i < TOTAL_SEGMENTS; i++) {
    const seg = {
      id: i + 1,
      total: FILE_SIZE_MB / TOTAL_SEGMENTS,
      downloaded: 0,
      speed: 1.2 + Math.random() * 1.4, // MB/s
      completed: false
    };
    segments.push(seg);

    // Create Cell
    const cell = document.createElement("div");
    cell.className = "segment-cell active";
    cell.id = `seg-cell-${i}`;
    cell.innerHTML = `
      <div class="segment-cell-fill" id="seg-fill-${i}" style="width: 0%;"></div>
      <span class="segment-cell-label">T${i + 1}</span>
    `;
    grid.appendChild(cell);

    // Create Sparse block
    if (sparseRow) {
      const blk = document.createElement("div");
      blk.className = "sparse-block";
      blk.id = `sparse-blk-${i}`;
      sparseRow.appendChild(blk);
    }
  }

  startSimulatorLoop();
}

function startSimulatorLoop() {
  if (simInterval) clearInterval(simInterval);

  simInterval = setInterval(() => {
    if (simPaused) return;

    let allCompleted = true;
    let currentTotalSpeed = 0;

    segments.forEach((seg, idx) => {
      if (!seg.completed) {
        allCompleted = false;
        seg.downloaded += seg.speed * 0.12;
        currentTotalSpeed += seg.speed;

        if (seg.downloaded >= seg.total) {
          seg.downloaded = seg.total;
          seg.completed = true;
          markSegmentComplete(idx);

          // Work-Stealing: Find segment with most bytes remaining and steal half
          stealWorkFromLargest(idx);
        }

        const pct = Math.min(100, (seg.downloaded / seg.total) * 100);
        const fill = document.getElementById(`seg-fill-${idx}`);
        if (fill) fill.style.width = `${pct.toFixed(1)}%`;
      }
    });

    // Update aggregate stats
    const totalDownloaded = segments.reduce((acc, s) => acc + s.downloaded, 0);
    const overallPct = (totalDownloaded / FILE_SIZE_MB) * 100;
    const mbDownloadedEl = document.getElementById("simDownloadedMb");
    const pctEl = document.getElementById("simPercent");
    const speedEl = document.getElementById("simSpeedVal");
    const etaEl = document.getElementById("simEtaVal");
    const overallBar = document.getElementById("simOverallBar");

    if (mbDownloadedEl) mbDownloadedEl.innerText = `${totalDownloaded.toFixed(1)} MB / ${FILE_SIZE_MB} MB`;
    if (pctEl) pctEl.innerText = `${overallPct.toFixed(1)}%`;
    if (overallBar) overallBar.style.width = `${overallPct.toFixed(1)}%`;
    if (speedEl) speedEl.innerText = `${currentTotalSpeed.toFixed(1)} MB/s`;

    if (currentTotalSpeed > 0 && etaEl) {
      const remSec = Math.max(0, Math.round((FILE_SIZE_MB - totalDownloaded) / currentTotalSpeed));
      etaEl.innerText = `${remSec}s`;
    }

    if (allCompleted) {
      clearInterval(simInterval);
      if (speedEl) speedEl.innerText = "0.0 MB/s (Selesai)";
      if (etaEl) etaEl.innerText = "0s";
      showSparseZeroDelayNotice();
    }
  }, 120);
}

function markSegmentComplete(idx) {
  const cell = document.getElementById(`seg-cell-${idx}`);
  if (cell) {
    cell.classList.remove("active");
    cell.classList.add("completed");
  }
  const blk = document.getElementById(`sparse-blk-${idx}`);
  if (blk) {
    blk.classList.add("written");
  }
}

function stealWorkFromLargest(idleIdx) {
  let largestIdx = -1;
  let maxRem = 0;

  segments.forEach((s, idx) => {
    if (!s.completed) {
      const rem = s.total - s.downloaded;
      if (rem > maxRem && rem > 15) {
        maxRem = rem;
        largestIdx = idx;
      }
    }
  });

  if (largestIdx !== -1) {
    // Bisect remaining slice
    const half = maxRem / 2;
    segments[largestIdx].total -= half;

    // Reactivate idle worker on the stolen slice
    segments[idleIdx].total = half;
    segments[idleIdx].downloaded = 0;
    segments[idleIdx].completed = false;
    segments[idleIdx].speed = 1.4 + Math.random() * 1.5;

    const idleCell = document.getElementById(`seg-cell-${idleIdx}`);
    if (idleCell) {
      idleCell.classList.remove("completed");
      idleCell.classList.add("active");
    }
  }
}

function showSparseZeroDelayNotice() {
  const notice = document.getElementById("simSparseNotice");
  if (notice) {
    notice.style.display = "inline-flex";
  }
}

function toggleSimPause() {
  simPaused = !simPaused;
  const btn = document.getElementById("simPauseBtn");
  if (btn) {
    btn.innerText = simPaused ? (currentLang === "en" ? "Resume" : "Lanjutkan") : (currentLang === "en" ? "Pause" : "Jeda");
  }
}

function restartSim() {
  simPaused = false;
  const notice = document.getElementById("simSparseNotice");
  if (notice) notice.style.display = "none";
  initSimulator();
}

// -----------------------------------------------------------------------------
// FAQ Accordion
// -----------------------------------------------------------------------------
function initFaqAccordion() {
  const triggers = document.querySelectorAll(".faq-trigger");
  triggers.forEach(btn => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".faq-item");
      const isExpanded = btn.getAttribute("aria-expanded") === "true";

      // Close all other items
      document.querySelectorAll(".faq-item").forEach(other => {
        if (other !== item) {
          other.classList.remove("active");
          const otherBtn = other.querySelector(".faq-trigger");
          if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
        }
      });

      if (isExpanded) {
        item.classList.remove("active");
        btn.setAttribute("aria-expanded", "false");
      } else {
        item.classList.add("active");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });
}

// -----------------------------------------------------------------------------
// License Verification Engine (Online REST API + Offline Crypto Fallback)
// -----------------------------------------------------------------------------
const AUDIRA_SIGNING_SALT = "AUDIRA_ADM_KERNEL_SIGNING_KEY_2026_AGUS_DWI_RIANTO_MDA_ASM";

async function sha256Hex(str) {
  const buf = new TextEncoder().encode(str);
  const hashBuf = await crypto.subtle.digest("SHA-256", buf);
  const arr = Array.from(new Uint8Array(hashBuf));
  return arr.map(b => b.toString(16).padStart(2, "0")).join("").toUpperCase();
}

async function verifyClientCrypto(key, ownerName, email) {
  const clean = key.trim().toUpperCase();
  const parts = clean.split("-");
  if (parts.length < 4 || parts[0] !== "ADM") {
    return { valid: false, message: "Format Serial Key tidak valid (contoh: ADM-LIFE-0-XXXXXXXXXXXXXXXX)" };
  }

  const tierCode = parts[1];
  const expiresAt = parseInt(parts[2], 10);
  const providedSig = parts[3];

  if (isNaN(expiresAt)) {
    return { valid: false, message: "Struktur tanggal kedaluwarsa serial rusak." };
  }

  const nowSec = Math.floor(Date.now() / 1000);
  if (expiresAt > 0 && nowSec > expiresAt) {
    return { valid: false, message: "Kunci lisensi ini telah kedaluwarsa." };
  }

  // Compute expected HMAC signature
  const input = AUDIRA_SIGNING_SALT + tierCode + ownerName.trim() + email.toLowerCase().trim() + expiresAt.toString();
  const fullHash = await sha256Hex(input);
  const expectedSig = fullHash.slice(0, 16);

  if (providedSig !== expectedSig) {
    return { valid: false, message: "Tanda tangan lisensi tidak cocok dengan Nama atau Email terdaftar." };
  }

  return {
    valid: true,
    message: "Lisensi Valid dan Terdaftar Resmi di AUDIRA Ecosystem",
    tier: tierCode === "LIFE" ? "Audira PRO Lifetime" : "Audira PRO Annual",
    expires_at: expiresAt,
    is_lifetime: expiresAt === 0,
    owner_name: ownerName,
    email: email
  };
}

function initLicenseChecker() {
  const form = document.getElementById("checkForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const key = document.getElementById("chkKey").value.trim().toUpperCase();
    const ownerName = document.getElementById("chkName").value.trim();
    const email = document.getElementById("chkEmail").value.trim();
    const resultBox = document.getElementById("checkResult");
    const btn = document.getElementById("btnCheck");

    btn.innerText = currentLang === "en" ? "Verifying..." : "Memvalidasi...";
    btn.disabled = true;
    resultBox.style.display = "none";

    let verificationResult = null;

    // 1. Try Live Server API
    try {
      const resp = await fetch("/api/v1/license/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key, owner_name: ownerName, email })
      });
      const data = await resp.json();
      if (resp.ok && data.valid) {
        verificationResult = data;
      } else {
        verificationResult = { valid: false, message: data.message || "Data lisensi tidak cocok." };
      }
    } catch (err) {
      // 2. Offline Cryptographic Fallback (runs authentic SHA-256 in browser)
      verificationResult = await verifyClientCrypto(key, ownerName, email);
    }

    resultBox.style.display = "block";
    btn.disabled = false;
    btn.innerText = currentLang === "en" ? "Verify License Status" : "Cek Status Lisensi";

    if (verificationResult && verificationResult.valid) {
      resultBox.style.background = "rgba(16, 185, 129, 0.1)";
      resultBox.style.border = "1px solid rgba(16, 185, 129, 0.35)";
      resultBox.style.color = "#34d399";
      resultBox.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; font-weight:700; margin-bottom:8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          ${currentLang === "en" ? "OFFICIALLY VERIFIED LICENSE" : "LISENSI RESMI & TERVALIDASI"}
        </div>
        <div style="font-size:13px; line-height:1.6; color:var(--color-text-body);">
          ${currentLang === "en" ? "Plan" : "Paket"}: <b>${verificationResult.tier}</b><br>
          ${currentLang === "en" ? "Licensee" : "Pemilik"}: <b>${verificationResult.owner_name}</b> (${verificationResult.email})<br>
          ${currentLang === "en" ? "Validity" : "Masa Aktif"}: <b>${verificationResult.is_lifetime ? (currentLang === "en" ? "Permanent (Lifetime)" : "Permanen (Seumur Hidup)") : new Date(verificationResult.expires_at * 1000).toLocaleDateString()}</b><br>
          Status: <span style="color:#10b981; font-weight:600;">${verificationResult.message}</span>
        </div>
      `;
    } else {
      resultBox.style.background = "rgba(244, 63, 94, 0.1)";
      resultBox.style.border = "1px solid rgba(244, 63, 94, 0.35)";
      resultBox.style.color = "#fb7185";
      resultBox.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; font-weight:700; margin-bottom:6px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          ${currentLang === "en" ? "VERIFICATION FAILED" : "VALIDASI GAGAL"}
        </div>
        <div style="font-size:13px; color:var(--color-text-body);">${verificationResult ? verificationResult.message : "Data tidak valid."}</div>
      `;
    }
  });
}
