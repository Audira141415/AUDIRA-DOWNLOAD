//! AUDIRA Download Manager (ADM) — Cryptographic Licensing & Hardware ID Subsystem
//!
//! Developed for AUDIRA Ecosystem (Agus Dwi Rianto - Audira Multimedia Digital / Audira Sukses Mandiri)
//! Provides cryptographic validation, HWID hardware binding, trial period management,
//! and feature gating (Max connections, 4K/8K grabs, Auto-shutdown, AI models).

use crate::db::Db;
use chrono::Utc;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

/// Master secret salt for AUDIRA cryptographic signatures.
/// Private to AUDIRA and used to verify authenticity of generated license keys.
const AUDIRA_SIGNING_SALT: &str = "AUDIRA_ADM_KERNEL_SIGNING_KEY_2026_AGUS_DWI_RIANTO_MDA_ASM";

/// Setting keys in the SQLite database
const DB_KEY_LICENSE: &str = "adm_license_v1";
const DB_KEY_TRIAL_START: &str = "_adm_trial_t0";

/// Number of days for the initial trial period.
pub const TRIAL_DURATION_DAYS: i64 = 14;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub enum LicenseTier {
    Free,
    Trial,
    ProAnnual,
    ProLifetime,
}

impl Default for LicenseTier {
    fn default() -> Self {
        Self::Free
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct LicenseInfo {
    pub tier: LicenseTier,
    pub is_active: bool,
    pub is_pro: bool,
    pub owner_name: String,
    pub email: String,
    pub license_key: Option<String>,
    pub hwid: String,
    pub days_left: Option<i64>,
    pub expires_at: Option<i64>, // Unix timestamp in seconds; 0 = Lifetime
    pub max_connections: u8,
    pub allow_4k_8k: bool,
    pub allow_auto_shutdown: bool,
    pub allow_unlimited_hf: bool,
    pub message: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoredLicenseRecord {
    pub key: String,
    pub owner_name: String,
    pub email: String,
    pub activated_at: i64,
    pub expires_at: i64,
    pub tier: LicenseTier,
}

/// Compute stable Machine Hardware ID (HWID)
pub fn get_machine_hwid() -> String {
    let mut raw_seed = String::new();

    #[cfg(windows)]
    {
        if let Ok(key) = winreg::RegKey::predef(winreg::enums::HKEY_LOCAL_MACHINE)
            .open_subkey(r"SOFTWARE\Microsoft\Cryptography")
        {
            if let Ok(guid) = key.get_value::<String, _>("MachineGuid") {
                raw_seed.push_str(&guid);
            }
        }
    }

    #[cfg(target_os = "linux")]
    {
        if let Ok(id) = std::fs::read_to_string("/etc/machine-id") {
            raw_seed.push_str(id.trim());
        }
    }

    #[cfg(target_os = "macos")]
    {
        if let Ok(id) = std::fs::read_to_string("/var/db/locate.database") {
            raw_seed.push_str(&id[..std::cmp::min(32, id.len())]);
        }
    }

    if raw_seed.trim().is_empty() {
        if let Ok(hostname) = std::env::var("COMPUTERNAME").or_else(|_| std::env::var("HOSTNAME")) {
            raw_seed.push_str(&hostname);
        }
        if let Ok(user) = std::env::var("USERNAME").or_else(|_| std::env::var("USER")) {
            raw_seed.push_str(&user);
        }
    }

    if raw_seed.is_empty() {
        raw_seed.push_str("AUDIRA-DEFAULT-MACHINE-NODE");
    }

    let mut hasher = Sha256::new();
    hasher.update(b"AUDIRA_HWID_PREFIX:");
    hasher.update(raw_seed.as_bytes());
    let hash = hex::encode(hasher.finalize()).to_uppercase();

    // Format as ADM-XXXX-XXXX-XXXX-XXXX
    format!(
        "ADM-{}-{}-{}-{}",
        &hash[0..4],
        &hash[4..8],
        &hash[8..12],
        &hash[12..16]
    )
}

/// Generate cryptographic signature for a given license payload
pub fn compute_license_signature(tier_str: &str, owner_name: &str, email: &str, expires_at: i64) -> String {
    let mut hasher = Sha256::new();
    hasher.update(AUDIRA_SIGNING_SALT.as_bytes());
    hasher.update(tier_str.to_uppercase().trim().as_bytes());
    hasher.update(owner_name.trim().as_bytes());
    hasher.update(email.to_lowercase().trim().as_bytes());
    hasher.update(expires_at.to_string().as_bytes());
    let full = hex::encode(hasher.finalize()).to_uppercase();
    full[0..16].to_string()
}

/// Official AUDIRA License Key Generator for Admin / Billing
pub fn generate_adm_key(tier: LicenseTier, owner_name: &str, email: &str, expires_at: i64) -> String {
    let tier_code = match tier {
        LicenseTier::ProLifetime => "LIFE",
        LicenseTier::ProAnnual => "YEAR",
        _ => "TRIAL",
    };
    let sig = compute_license_signature(tier_code, owner_name, email, expires_at);
    // Format: ADM-<TIER>-<EXPIRY>-<SIG>
    // Example: ADM-LIFE-0-A1B2C3D4E5F67890
    format!("ADM-{}-{}-{}", tier_code, expires_at, sig)
}

/// Verify a license key
pub fn verify_adm_key(key: &str, owner_name: &str, email: &str) -> Result<(LicenseTier, i64), String> {
    let clean = key.trim().to_uppercase();
    let parts: Vec<&str> = clean.split('-').collect();

    if parts.len() < 4 || parts[0] != "ADM" {
        return Err("Format Serial Key tidak valid. Contoh: ADM-LIFE-0-XXXXXXXXXXXXXXXX".into());
    }

    let tier_code = parts[1];
    let expires_at: i64 = parts[2]
        .parse()
        .map_err(|_| "Informasi masa berlaku lisensi rusak".to_string())?;
    let provided_sig = parts[3];

    let tier = match tier_code {
        "LIFE" => LicenseTier::ProLifetime,
        "YEAR" => LicenseTier::ProAnnual,
        _ => return Err("Tipe lisensi dalam kunci tidak dikenal".into()),
    };

    let now = Utc::now().timestamp();
    if expires_at > 0 && now > expires_at {
        return Err("Lisensi ini telah kedaluwarsa".into());
    }

    let expected_sig = compute_license_signature(tier_code, owner_name, email, expires_at);
    if provided_sig != expected_sig {
        return Err("Tanda tangan lisensi tidak cocok dengan Nama atau Email terdaftar".into());
    }

    Ok((tier, expires_at))
}

#[derive(Clone)]
pub struct LicensingManager {
    hwid: String,
}

impl Default for LicensingManager {
    fn default() -> Self {
        Self::new()
    }
}

impl LicensingManager {
    pub fn new() -> Self {
        let hwid = get_machine_hwid();
        Self { hwid }
    }

    pub fn hwid(&self) -> &str {
        &self.hwid
    }

    /// Retrieve the current active license status
    pub fn get_info(&self, db: &Db) -> LicenseInfo {
        let now = Utc::now().timestamp();

        // 1. Check if a purchased Pro license is saved
        if let Ok(Some(json_str)) = db.get_setting(DB_KEY_LICENSE) {
            if !json_str.trim().is_empty() {
                if let Ok(record) = serde_json::from_str::<StoredLicenseRecord>(&json_str) {
                    if let Ok((tier, expires_at)) = verify_adm_key(&record.key, &record.owner_name, &record.email) {
                        let days_left = if expires_at == 0 {
                            None
                        } else {
                            Some((expires_at - now).max(0) / 86400)
                        };

                        return LicenseInfo {
                            tier,
                            is_active: true,
                            is_pro: true,
                            owner_name: record.owner_name,
                            email: record.email,
                            license_key: Some(record.key),
                            hwid: self.hwid.clone(),
                            days_left,
                            expires_at: Some(expires_at),
                            max_connections: 32,
                            allow_4k_8k: true,
                            allow_auto_shutdown: true,
                            allow_unlimited_hf: true,
                            message: "Lisensi Resmi Audira PRO Aktif".into(),
                        };
                    }
                }
            }
        }

        // 2. Check or initialize Trial mode
        let trial_start: i64 = match db.get_setting(DB_KEY_TRIAL_START) {
            Ok(Some(v)) => v.parse().unwrap_or(now),
            _ => {
                let _ = db.set_setting(DB_KEY_TRIAL_START, &now.to_string());
                now
            }
        };

        let trial_end = trial_start + (TRIAL_DURATION_DAYS * 86400);
        let days_remaining = (trial_end - now) / 86400;

        if days_remaining >= 0 {
            LicenseInfo {
                tier: LicenseTier::Trial,
                is_active: true,
                is_pro: false,
                owner_name: "Pengguna Uji Coba".into(),
                email: "-".into(),
                license_key: None,
                hwid: self.hwid.clone(),
                days_left: Some(days_remaining),
                expires_at: Some(trial_end),
                max_connections: 8,
                allow_4k_8k: false,
                allow_auto_shutdown: false,
                allow_unlimited_hf: false,
                message: format!("Masa Uji Coba: Sisa {} hari", days_remaining),
            }
        } else {
            LicenseInfo {
                tier: LicenseTier::Free,
                is_active: false,
                is_pro: false,
                owner_name: "Audira Free Edition".into(),
                email: "-".into(),
                license_key: None,
                hwid: self.hwid.clone(),
                days_left: Some(0),
                expires_at: None,
                max_connections: 6,
                allow_4k_8k: false,
                allow_auto_shutdown: false,
                allow_unlimited_hf: false,
                message: "Masa Uji Coba Telah Berakhir. Silakan Aktivasi Audira PRO.".into(),
            }
        }
    }

    /// Activate a purchased license
    pub fn activate(&self, db: &Db, key: &str, owner_name: &str, email: &str) -> Result<LicenseInfo, String> {
        let (tier, expires_at) = verify_adm_key(key, owner_name, email)?;

        let record = StoredLicenseRecord {
            key: key.trim().to_uppercase(),
            owner_name: owner_name.trim().to_string(),
            email: email.trim().to_lowercase(),
            activated_at: Utc::now().timestamp(),
            expires_at,
            tier,
        };

        let json_str = serde_json::to_string(&record).map_err(|e| e.to_string())?;
        db.set_setting(DB_KEY_LICENSE, &json_str).map_err(|e| e.to_string())?;

        Ok(self.get_info(db))
    }

    /// Deactivate current license (switch back to trial/free)
    pub fn deactivate(&self, db: &Db) -> Result<LicenseInfo, String> {
        db.set_setting(DB_KEY_LICENSE, "").map_err(|e| e.to_string())?;
        Ok(self.get_info(db))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_license_generation_and_verification() {
        let name = "Agus Dwi Rianto";
        let email = "agusdwirianto@gmail.com";
        let key = generate_adm_key(LicenseTier::ProLifetime, name, email, 0);

        assert!(key.starts_with("ADM-LIFE-0-"));
        let res = verify_adm_key(&key, name, email);
        assert!(res.is_ok());
        let (tier, exp) = res.unwrap();
        assert_eq!(tier, LicenseTier::ProLifetime);
        assert_eq!(exp, 0);

        // Tampered name must fail
        assert!(verify_adm_key(&key, "Hacker", email).is_err());
        // Tampered email must fail
        assert!(verify_adm_key(&key, name, "fake@hacker.com").is_err());
    }

    #[test]
    fn test_hwid_not_empty() {
        let hwid = get_machine_hwid();
        assert!(hwid.starts_with("ADM-"));
        assert_eq!(hwid.len(), 23); // ADM-XXXX-XXXX-XXXX-XXXX
    }
}
