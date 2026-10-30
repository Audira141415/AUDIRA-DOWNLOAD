// Web links: opened in the user's browser (a new tab in the browser preview).

import { inTauri } from "./api";

/** AUDIRA Official Links & Support */
export const AUDIRA_WEBSITE_URL = "https://audira.my.id";
export const AUDIRA_WHATSAPP_URL = "https://wa.me/6282112001600?text=Halo%20AUDIRA,%20saya%20ingin%20membeli%20lisensi%20Audira%20Download%20Manager%20Pro";
export const AUDIRA_EMAIL_SUPPORT = "mailto:agusdwirianto@gmail.com";
export const REPO_URL = "https://audira.my.id";

export async function openUrl(url: string) {
  if (inTauri) {
    const opener = await import("@tauri-apps/plugin-opener");
    await opener.openUrl(url);
  } else {
    window.open(url, "_blank", "noopener");
  }
}
