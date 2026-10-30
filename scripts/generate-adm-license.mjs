// scripts/generate-adm-license.mjs
// Official License Key Generator for Audira Download Manager (ADM)
// Exclusive to Agus Dwi Rianto (AUDIRA Ecosystem)

import { createHash } from "node:crypto";

const AUDIRA_SIGNING_SALT = "AUDIRA_ADM_KERNEL_SIGNING_KEY_2026_AGUS_DWI_RIANTO_MDA_ASM";

export function generateAdmKey(tier, ownerName, email, expiresAt = 0) {
  const tierCode = String(tier).toUpperCase() === "YEAR" || String(tier).toUpperCase() === "ANNUAL" ? "YEAR" : "LIFE";

  const hasher = createHash("sha256");
  hasher.update(AUDIRA_SIGNING_SALT);
  hasher.update(tierCode);
  hasher.update(ownerName.trim());
  hasher.update(email.toLowerCase().trim());
  hasher.update(expiresAt.toString());

  const full = hasher.digest("hex").toUpperCase();
  const sig = full.slice(0, 16);

  return `ADM-${tierCode}-${expiresAt}-${sig}`;
}

// Parse both positional and flag-based arguments
const args = process.argv.slice(2);
let name = "";
let email = "";
let tier = "LIFE";
let expires = "0";

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--name" && args[i + 1]) {
    name = args[++i];
  } else if (a === "--email" && args[i + 1]) {
    email = args[++i];
  } else if (a === "--tier" && args[i + 1]) {
    tier = args[++i];
  } else if (a === "--expires" && args[i + 1]) {
    expires = args[++i];
  } else if (!a.startsWith("--")) {
    if (!name) name = a;
    else if (!email) email = a;
    else if (tier === "LIFE" && (a.toUpperCase() === "YEAR" || a.toUpperCase() === "LIFE")) tier = a;
    else if (expires === "0") expires = a;
  }
}

if (!name || !email) {
  console.log(`
=== AUDIRA DOWNLOAD MANAGER (ADM) — LICENSE GENERATOR ===
Penggunaan:
  node scripts/generate-adm-license.mjs "<Owner Name>" "<Email>" [LIFE|YEAR] [expiresAt]
  node scripts/generate-adm-license.mjs --name "<Owner Name>" --email "<Email>" --tier [LIFE|YEAR]

Contoh Pembuatan Kunci Lifetime:
  node scripts/generate-adm-license.mjs "Agus Dwi Rianto" "agusdwirianto@gmail.com" LIFE
  node scripts/generate-adm-license.mjs --name "Agus Dwi Rianto" --email "agus@audira.my.id" --tier LIFE
  `);
  process.exit(1);
}

const key = generateAdmKey(tier, name, email, Number(expires));
console.log(`\n======================================================`);
console.log(`⭐ KUNCI LISENSI RESMI AUDIRA DOWNLOAD MANAGER PRO ⭐`);
console.log(`======================================================`);
console.log(`Pemilik      : ${name}`);
console.log(`Email        : ${email}`);
console.log(`Tipe Paket   : ${tier.toUpperCase() === "YEAR" ? "Pro Annual" : "Pro Lifetime"}`);
console.log(`Berlaku s/d  : ${expires === "0" ? "Selamanya (Permanen)" : new Date(Number(expires) * 1000).toLocaleDateString("id-ID")}`);
console.log(`Serial Key   : ${key}`);
console.log(`======================================================\n`);
