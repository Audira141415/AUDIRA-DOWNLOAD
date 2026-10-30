import { useState } from "react";
import { Modal } from "./Modal";
import { Icon } from "../design/icons";
import { useApp } from "../lib/store";
import { activateLicense, deactivateLicense } from "../lib/api";
import { AUDIRA_WHATSAPP_URL, openUrl } from "../lib/links";

export function LicenseModal() {
  const isOpen = useApp((st) => st.isLicenseModalOpen);
  const setOpen = useApp((st) => st.setLicenseModalOpen);
  const license = useApp((st) => st.license);
  const setLicense = useApp((st) => st.setLicense);

  const [key, setKey] = useState("");
  const [ownerName, setOwnerName] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [copiedHwid, setCopiedHwid] = useState(false);

  if (!license) return null;

  const handleCopyHwid = async () => {
    try {
      await navigator.clipboard.writeText(license.hwid);
      setCopiedHwid(true);
      setTimeout(() => setCopiedHwid(false), 2000);
    } catch {
      // fallback
    }
  };

  const handleActivate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!key.trim() || !ownerName.trim() || !email.trim()) {
      setError("Semua kolom (Serial Key, Nama, Email) wajib diisi!");
      return;
    }
    setError(null);
    setSuccess(null);
    setLoading(true);

    try {
      const updated = await activateLicense({
        key: key.trim(),
        ownerName: ownerName.trim(),
        email: email.trim(),
      });
      setLicense(updated);
      setSuccess("Selamat! Lisensi Audira PRO berhasil diaktifkan.");
      setKey("");
    } catch (err) {
      setError(typeof err === "string" ? err : "Gagal memverifikasi lisensi. Pastikan Serial Key, Nama, dan Email sesuai.");
    } finally {
      setLoading(false);
    }
  };

  const handleDeactivate = async () => {
    if (!window.confirm("Apakah Anda yakin ingin menonaktifkan lisensi ini di komputer ini?")) return;
    setLoading(true);
    try {
      const updated = await deactivateLicense();
      setLicense(updated);
      setSuccess("Lisensi berhasil dinonaktifkan.");
    } catch (err) {
      setError(typeof err === "string" ? err : "Gagal menonaktifkan lisensi.");
    } finally {
      setLoading(false);
    }
  };

  const isPro = license.isPro;

  return (
    <Modal
      open={isOpen}
      onClose={() => {
        setOpen(false);
        setError(null);
        setSuccess(null);
      }}
      title="Aktivasi Lisensi Audira PRO"
      icon={<Icon name="shield" size={18} />}
      width={520}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "16px", padding: "4px 0" }}>
        {/* Status Badge Banner */}
        <div
          style={{
            padding: "12px 16px",
            borderRadius: "8px",
            border: isPro ? "1px solid rgba(234, 179, 8, 0.4)" : "1px solid rgba(59, 130, 246, 0.3)",
            background: isPro
              ? "linear-gradient(135deg, rgba(234, 179, 8, 0.15), rgba(245, 158, 11, 0.05))"
              : "linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.05))",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div>
            <div style={{ fontSize: "14px", fontWeight: "bold", color: isPro ? "#fbbf24" : "#60a5fa" }}>
              {isPro ? "⭐ AUDIRA PRO AKTIF" : license.tier === "trial" ? "⏳ MASA UJI COBA (TRIAL)" : "⚡ FREE EDITION"}
            </div>
            <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "2px" }}>
              {isPro
                ? `Terdaftar atas nama: ${license.ownerName} (${license.email})`
                : license.message}
            </div>
          </div>
          {isPro && (
            <button
              type="button"
              className="btn btn--ghost"
              style={{ fontSize: "12px", padding: "4px 8px" }}
              onClick={handleDeactivate}
              disabled={loading}
            >
              Nonaktifkan
            </button>
          )}
        </div>

        {/* Feature Matrix summary */}
        <div
          style={{
            fontSize: "12px",
            padding: "10px 14px",
            background: "rgba(255, 255, 255, 0.03)",
            borderRadius: "6px",
            border: "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          <div style={{ fontWeight: 600, marginBottom: "6px", color: "var(--text-primary)" }}>
            Keuntungan Audira PRO:
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px", color: "var(--text-secondary)" }}>
            <div>✔ Hingga 32 Koneksi Paralel</div>
            <div>✔ Video Grabber 4K/8K HDR</div>
            <div>✔ Unlimited Download Queues</div>
            <div>✔ Model AI Hugging Face</div>
            <div>✔ Auto Sleep & PC Shutdown</div>
            <div>✔ Prioritas WhatsApp Support</div>
          </div>
        </div>

        {/* Machine HWID Box */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "8px 12px",
            background: "rgba(0, 0, 0, 0.2)",
            borderRadius: "6px",
            fontSize: "12px",
            border: "1px solid rgba(255, 255, 255, 0.05)",
          }}
        >
          <div>
            <span style={{ color: "var(--text-tertiary)" }}>Machine HWID: </span>
            <span style={{ fontFamily: "monospace", fontWeight: "bold", color: "var(--text-primary)" }}>
              {license.hwid}
            </span>
          </div>
          <button
            type="button"
            className="btn btn--ghost"
            style={{ fontSize: "11px", padding: "2px 8px" }}
            onClick={handleCopyHwid}
          >
            {copiedHwid ? "Tersalin! ✔" : "Salin HWID"}
          </button>
        </div>

        {/* Feedback Alert */}
        {error && (
          <div
            style={{
              padding: "8px 12px",
              borderRadius: "6px",
              background: "rgba(239, 68, 68, 0.15)",
              border: "1px solid rgba(239, 68, 68, 0.3)",
              color: "#fca5a5",
              fontSize: "12px",
            }}
          >
            {error}
          </div>
        )}
        {success && (
          <div
            style={{
              padding: "8px 12px",
              borderRadius: "6px",
              background: "rgba(34, 197, 94, 0.15)",
              border: "1px solid rgba(34, 197, 94, 0.3)",
              color: "#86efac",
              fontSize: "12px",
            }}
          >
            {success}
          </div>
        )}

        {/* Activation Form */}
        {!isPro && (
          <form onSubmit={handleActivate} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <div>
              <label style={{ fontSize: "12px", fontWeight: 500, display: "block", marginBottom: "4px" }}>
                Serial License Key:
              </label>
              <input
                type="text"
                className="input"
                placeholder="ADM-LIFE-0-XXXXXXXXXXXXXXXX"
                value={key}
                onChange={(e) => setKey(e.target.value)}
                style={{ width: "100%", fontFamily: "monospace", textTransform: "uppercase" }}
                disabled={loading}
              />
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
              <div>
                <label style={{ fontSize: "12px", fontWeight: 500, display: "block", marginBottom: "4px" }}>
                  Nama Pemilik:
                </label>
                <input
                  type="text"
                  className="input"
                  placeholder="Contoh: Agus Dwi Rianto"
                  value={ownerName}
                  onChange={(e) => setOwnerName(e.target.value)}
                  style={{ width: "100%" }}
                  disabled={loading}
                />
              </div>
              <div>
                <label style={{ fontSize: "12px", fontWeight: 500, display: "block", marginBottom: "4px" }}>
                  Email Terdaftar:
                </label>
                <input
                  type="email"
                  className="input"
                  placeholder="nama@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  style={{ width: "100%" }}
                  disabled={loading}
                />
              </div>
            </div>

            <div style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
              <button type="submit" className="btn btn--primary" style={{ flex: 1 }} disabled={loading}>
                {loading ? "Memvalidasi..." : "Aktivasi Sekarang"}
              </button>
              <button
                type="button"
                className="btn btn--accent"
                onClick={() => void openUrl(AUDIRA_WHATSAPP_URL)}
                style={{ display: "flex", alignItems: "center", gap: "6px" }}
              >
                <span>Beli Lisensi (WhatsApp)</span>
              </button>
            </div>
          </form>
        )}
      </div>
    </Modal>
  );
}

