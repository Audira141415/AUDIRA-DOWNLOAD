#!/usr/bin/env python3
"""
AUDIRA Download Manager (ADM) — Central Management Portal, Licensing Server & Landing Page
Port: 5060 (Configurable via --port, e.g. 5050 or 5060)
Author: Agus Dwi Rianto (AUDIRA) • Audira Multimedia Digital / Audira Sukses Mandiri
Website: https://audira.my.id • WhatsApp: +62 821-1200-1600
"""

import os
import sys
import json
import time
import sqlite3
import datetime
import threading
import hashlib
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# UTF-8 Console Safety on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Master Salt matching the Rust core engine for cryptographic offline & online validation
AUDIRA_SIGNING_SALT = "AUDIRA_ADM_KERNEL_SIGNING_KEY_2026_AGUS_DWI_RIANTO_MDA_ASM"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "adm_portal.sqlite3")

DEFAULT_ADMIN_USER = "audira"
DEFAULT_ADMIN_PASS = "Sigma1993"

PORT = int(os.environ.get("PORT", 5060))
if "--port" in sys.argv:
    idx = sys.argv.index("--port")
    if idx + 1 < len(sys.argv):
        PORT = int(sys.argv[idx + 1])

# ------------------------------------------------------------------------------
# Database & Licensing Engine
# ------------------------------------------------------------------------------

def get_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                tier TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                email TEXT NOT NULL,
                hwid TEXT DEFAULT '',
                expires_at INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                created_at TEXT NOT NULL,
                notes TEXT DEFAULT ''
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                plan TEXT NOT NULL,
                amount INTEGER NOT NULL,
                payment_method TEXT NOT NULL,
                license_key TEXT,
                status TEXT NOT NULL DEFAULT 'PENDING',
                created_at TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hwid TEXT NOT NULL,
                ip TEXT NOT NULL,
                app_version TEXT NOT NULL,
                last_seen TEXT NOT NULL
            );
        """)
    conn.close()

def compute_license_signature(tier_code, owner_name, email, expires_at):
    tier_clean = str(tier_code).upper().strip()
    owner_clean = str(owner_name).strip()
    email_clean = str(email).lower().strip()
    exp_str = str(expires_at).strip()

    h = hashlib.sha256()
    h.update(AUDIRA_SIGNING_SALT.encode("utf-8"))
    h.update(tier_clean.encode("utf-8"))
    h.update(owner_clean.encode("utf-8"))
    h.update(email_clean.encode("utf-8"))
    h.update(exp_str.encode("utf-8"))
    return h.hexdigest().upper()[:16]

def generate_adm_key(tier_type, owner_name, email, expires_at=0):
    t = str(tier_type).upper()
    tier_code = "YEAR" if "YEAR" in t or "ANNUAL" in t else "LIFE"
    sig = compute_license_signature(tier_code, owner_name, email, expires_at)
    return f"ADM-{tier_code}-{expires_at}-{sig}"

def verify_adm_key(key, owner_name, email):
    clean = str(key).strip().upper()
    parts = clean.split("-")
    if len(parts) < 4 or parts[0] != "ADM":
        return False, "Format Serial Key tidak valid (contoh: ADM-LIFE-0-XXXXXXXXXXXXXXXX)", None, 0

    tier_code = parts[1]
    try:
        expires_at = int(parts[2])
    except ValueError:
        return False, "Data masa aktif serial key rusak", None, 0

    provided_sig = parts[3]
    now = int(time.time())

    if expires_at > 0 and now > expires_at:
        return False, "Lisensi ini telah kedaluwarsa", None, expires_at

    expected_sig = compute_license_signature(tier_code, owner_name, email, expires_at)
    if provided_sig != expected_sig:
        return False, "Tanda tangan lisensi tidak cocok dengan Nama atau Email terdaftar", None, expires_at

    tier_name = "Pro Lifetime" if tier_code == "LIFE" else "Pro Annual"
    return True, "Lisensi Valid dan Resmi AUDIRA", tier_name, expires_at

# Seed sample license if empty
def seed_default_license():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM licenses")
    count = c.fetchone()[0]
    if count == 0:
        key = generate_adm_key("LIFE", "Agus Dwi Rianto", "agusdwirianto@gmail.com", 0)
        c.execute("""
            INSERT INTO licenses (key, tier, owner_name, email, hwid, expires_at, status, created_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            key, "LIFE", "Agus Dwi Rianto", "agusdwirianto@gmail.com", "", 0, "ACTIVE",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Founder Master Lifetime License"
        ))
        conn.commit()
    conn.close()

# ------------------------------------------------------------------------------
# HTTP Request Handler
# ------------------------------------------------------------------------------

class AdmPortalHandler(BaseHTTPRequestHandler):
    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors()
        self.end_headers()

    def send_json(self, data, code=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html_text, code=200):
        body = html_text.encode("utf-8")
        self.send_response(code)
        self.send_cors()
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def check_admin(self):
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Basic "):
            import base64
            try:
                dec = base64.b64decode(auth[6:]).decode("utf-8")
                u, p = dec.split(":", 1)
                if u == DEFAULT_ADMIN_USER and p == DEFAULT_ADMIN_PASS:
                    return True
            except Exception:
                pass
        return False

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. API: Server Health & Stats
        if path == "/api/v1/stats":
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM licenses WHERE status='ACTIVE'")
            active_licenses = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM orders WHERE status='PAID'")
            paid_orders = c.fetchone()[0]
            conn.close()
            return self.send_json({
                "success": True,
                "service": "Audira Download Manager Central Licensing Portal",
                "version": "1.1.7",
                "active_licenses": active_licenses,
                "paid_orders": paid_orders,
                "author": "Agus Dwi Rianto (AUDIRA)",
                "status": "ONLINE"
            })

        # 2. API: List Licenses (Admin only)
        if path == "/api/v1/licenses":
            if not self.check_admin():
                return self.send_json({"error": "Unauthorized. Admin credentials required."}, 401)
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM licenses ORDER BY id DESC")
            rows = [dict(r) for r in c.fetchall()]
            conn.close()
            return self.send_json({"success": True, "licenses": rows})

        # 3. Static Web Assets & Landing Pages
        web_root = os.path.join(os.path.dirname(BASE_DIR), 'web')
        if not os.path.exists(web_root):
            web_root = os.path.join(BASE_DIR, 'web')

        clean_path = path.lstrip('/')
        if path in ['/', '/index.html']:
            file_target = os.path.join(web_root, 'index.html')
        elif path in ['/portal', '/admin', '/admin.html']:
            file_target = os.path.join(web_root, 'admin.html')
        else:
            file_target = os.path.join(web_root, clean_path)

        if os.path.exists(file_target) and os.path.isfile(file_target):
            mime = 'text/plain'
            if file_target.endswith('.html'): mime = 'text/html; charset=utf-8'
            elif file_target.endswith('.css'): mime = 'text/css; charset=utf-8'
            elif file_target.endswith('.js'): mime = 'application/javascript; charset=utf-8'
            elif file_target.endswith('.svg'): mime = 'image/svg+xml'
            elif file_target.endswith('.png'): mime = 'image/png'
            elif file_target.endswith('.jpg') or file_target.endswith('.jpeg'): mime = 'image/jpeg'
            elif file_target.endswith('.ico'): mime = 'image/x-icon'
            elif file_target.endswith('.json'): mime = 'application/json; charset=utf-8'

            try:
                with open(file_target, 'rb') as sf:
                    data = sf.read()
                self.send_response(200)
                self.send_cors()
                self.send_header('Content-Type', mime)
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception:
                pass

        if path in ['/', '/index.html', '/portal', '/admin']:
            return self.send_html(render_portal_html())

        self.send_response(404)
        self.send_cors()
        self.end_headers()
        self.wfile.write(b'Not Found')

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b""
        try:
            body = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except Exception:
            body = {}

        # 1. API: Verify License (Used by Desktop App or Landing Page Checker)
        if path == "/api/v1/license/verify":
            key = body.get("key", "")
            owner_name = body.get("owner_name", "")
            email = body.get("email", "")

            valid, msg, tier, exp = verify_adm_key(key, owner_name, email)
            if not valid:
                return self.send_json({"valid": False, "message": msg}, 400)

            # Check if revoked in database
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT status FROM licenses WHERE key=?", (key.strip().upper(),))
            row = c.fetchone()
            conn.close()

            if row and row["status"] == "REVOKED":
                return self.send_json({"valid": False, "message": "Lisensi ini telah dicabut oleh administrator."}, 403)

            return self.send_json({
                "valid": True,
                "message": msg,
                "tier": tier,
                "expires_at": exp,
                "is_lifetime": exp == 0,
                "owner_name": owner_name,
                "email": email
            })

        # 2. API: Activate License & HWID Binding (Used by Desktop App)
        if path == "/api/v1/license/activate":
            key = body.get("key", "").strip().upper()
            owner_name = body.get("owner_name", "").strip()
            email = body.get("email", "").strip()
            hwid = body.get("hwid", "").strip()
            app_version = body.get("version", "1.1.7")

            valid, msg, tier, exp = verify_adm_key(key, owner_name, email)
            if not valid:
                return self.send_json({"success": False, "message": msg}, 400)

            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM licenses WHERE key=?", (key,))
            existing = c.fetchone()

            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_ip = (self.headers.get("X-Real-IP") or self.client_address[0]).replace("::ffff:", "")

            if existing:
                if existing["status"] == "REVOKED":
                    conn.close()
                    return self.send_json({"success": False, "message": "Lisensi telah dicabut."}, 403)
                # Update HWID if empty
                if not existing["hwid"] and hwid:
                    c.execute("UPDATE licenses SET hwid=? WHERE key=?", (hwid, key))
            else:
                # Store freshly activated valid key
                c.execute("""
                    INSERT INTO licenses (key, tier, owner_name, email, hwid, expires_at, status, created_at, notes)
                    VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE', ?, 'Online Activation via Client App')
                """, (key, "LIFE" if "LIFE" in key else "YEAR", owner_name, email, hwid, exp, now_str))

            # Record telemetry
            if hwid:
                c.execute("""
                    INSERT INTO telemetry (hwid, ip, app_version, last_seen)
                    VALUES (?, ?, ?, ?)
                """, (hwid, client_ip, app_version, now_str))

            conn.commit()
            conn.close()

            return self.send_json({
                "success": True,
                "message": "Lisensi Audira PRO berhasil diaktifkan dan dicatat pada server AUDIRA.",
                "tier": tier,
                "owner_name": owner_name,
                "email": email,
                "hwid": hwid
            })

        # 3. API: Generate New License (Admin only)
        if path == "/api/v1/license/generate":
            if not self.check_admin():
                return self.send_json({"error": "Unauthorized. Admin credentials required."}, 401)

            owner = body.get("owner_name", "").strip()
            email = body.get("email", "").strip()
            tier = body.get("tier", "LIFE").strip().upper()
            exp = int(body.get("expires_at", 0))
            notes = body.get("notes", "Generated from Web Portal")

            if not owner or not email:
                return self.send_json({"error": "Nama Pemilik dan Email wajib diisi"}, 400)

            key = generate_adm_key(tier, owner, email, exp)
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = get_db()
            c = conn.cursor()
            c.execute("""
                INSERT INTO licenses (key, tier, owner_name, email, hwid, expires_at, status, created_at, notes)
                VALUES (?, ?, ?, ?, '', ?, 'ACTIVE', ?, ?)
            """, (key, tier, owner, email, exp, now_str, notes))
            conn.commit()
            conn.close()

            return self.send_json({
                "success": True,
                "key": key,
                "tier": "Pro Lifetime" if tier == "LIFE" else "Pro Annual",
                "owner_name": owner,
                "email": email,
                "expires_at": exp,
                "created_at": now_str
            })

        # 4. API: Revoke / Unrevoke License (Admin only)
        if path == "/api/v1/license/toggle_status":
            if not self.check_admin():
                return self.send_json({"error": "Unauthorized. Admin credentials required."}, 401)
            key = body.get("key", "").strip().upper()
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT status FROM licenses WHERE key=?", (key,))
            row = c.fetchone()
            if not row:
                conn.close()
                return self.send_json({"error": "Key tidak ditemukan"}, 404)
            new_status = "REVOKED" if row["status"] == "ACTIVE" else "ACTIVE"
            c.execute("UPDATE licenses SET status=? WHERE key=?", (new_status, key))
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "key": key, "new_status": new_status})

        self.send_response(404)
        self.send_cors()
        self.end_headers()
        self.wfile.write(b"Not Found")

# ------------------------------------------------------------------------------
# High-Fidelity Landing Page & Web Portal HTML
# ------------------------------------------------------------------------------

def render_portal_html():
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Audira Download Manager (ADM) — Kecepatan Turbo 32 Segmen & AI Media Downloader</title>
  <meta name="description" content="Audira Download Manager adalah aplikasi download manager generasi baru dengan akselerasi multi-segmen hingga 32 koneksi, penangkap video 8K, dan dukungan model AI.">
  <link rel="icon" href="https://audira.my.id/favicon.ico">
  <style>
    :root {{
      --bg: #07090e;
      --card-bg: rgba(18, 22, 34, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent: #6366f1;
      --accent-glow: rgba(99, 102, 241, 0.35);
      --gold: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.35);
      --cyan: #06b6d4;
      --green: #10b981;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      line-height: 1.6;
      overflow-x: hidden;
      background-image:
        radial-gradient(circle at 15% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 70%, rgba(6, 182, 212, 0.1) 0%, transparent 45%);
    }}
    a {{ color: inherit; text-decoration: none; }}
    .container {{ max-width: 1180px; margin: 0 auto; padding: 0 24px; }}

    /* Header Nav */
    header {{
      position: sticky; top: 0; z-index: 50;
      backdrop-filter: blur(16px);
      background: rgba(7, 9, 14, 0.8);
      border-bottom: 1px solid var(--card-border);
    }}
    .nav {{
      display: flex; justify-content: space-between; align-items: center;
      height: 70px;
    }}
    .brand {{
      display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 19px; letter-spacing: -0.5px;
    }}
    .brand-tile {{
      width: 36px; height: 36px; border-radius: 10px;
      background: linear-gradient(135deg, #6366f1, #3b82f6);
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 0 20px var(--accent-glow);
    }}
    .nav-links {{ display: flex; gap: 24px; font-size: 14px; font-weight: 500; align-items: center; }}
    .nav-links a:hover {{ color: var(--cyan); }}
    .btn {{
      padding: 9px 18px; border-radius: 8px; font-size: 14px; font-weight: 600;
      cursor: pointer; transition: all 0.2s ease; border: none; display: inline-flex; align-items: center; gap: 8px;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff;
      box-shadow: 0 4px 16px var(--accent-glow);
    }}
    .btn-primary:hover {{ transform: translateY(-1px); box-shadow: 0 6px 22px var(--accent-glow); }}
    .btn-gold {{
      background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; font-weight: 700;
      box-shadow: 0 4px 16px var(--gold-glow);
    }}
    .btn-gold:hover {{ transform: translateY(-1px); box-shadow: 0 6px 22px var(--gold-glow); }}
    .btn-outline {{
      background: transparent; border: 1px solid var(--card-border); color: var(--text);
    }}
    .btn-outline:hover {{ background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.2); }}

    /* Hero */
    .hero {{ padding: 90px 0 60px; text-align: center; }}
    .badge {{
      display: inline-flex; align-items: center; gap: 8px;
      padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600;
      background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.3);
      color: #a5b4fc; margin-bottom: 24px;
    }}
    h1 {{
      font-size: 52px; font-weight: 800; line-height: 1.15; letter-spacing: -1.5px;
      margin-bottom: 20px;
    }}
    h1 span {{
      background: linear-gradient(135deg, #60a5fa, #a855f7, #f59e0b);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .hero-lead {{
      font-size: 18px; color: var(--text-muted); max-width: 680px; margin: 0 auto 36px;
    }}
    .hero-cta {{ display: flex; justify-content: center; gap: 16px; margin-bottom: 48px; }}

    /* Benchmark Visualizer */
    .bench-box {{
      background: var(--card-bg); border: 1px solid var(--card-border);
      border-radius: 16px; padding: 28px; backdrop-filter: blur(20px);
      max-width: 820px; margin: 0 auto 80px; text-align: left;
    }}
    .bench-title {{ font-size: 15px; font-weight: 700; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
    .bench-row {{ margin-bottom: 16px; }}
    .bench-label {{ display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; margin-bottom: 6px; }}
    .bench-bar-wrap {{ height: 12px; background: rgba(255, 255, 255, 0.05); border-radius: 6px; overflow: hidden; }}
    .bench-bar {{ height: 100%; border-radius: 6px; transition: width 1s ease-in-out; }}
    .bar-browser {{ width: 14%; background: #64748b; }}
    .bar-legacy {{ width: 65%; background: #0284c7; }}
    .bar-audira {{ width: 100%; background: linear-gradient(90deg, #6366f1, #10b981); box-shadow: 0 0 12px rgba(16, 185, 129, 0.5); }}

    /* Features Grid */
    .section-title {{ text-align: center; font-size: 34px; font-weight: 800; margin-bottom: 14px; letter-spacing: -1px; }}
    .section-sub {{ text-align: center; color: var(--text-muted); margin-bottom: 48px; font-size: 16px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; margin-bottom: 80px; }}
    .card {{
      background: var(--card-bg); border: 1px solid var(--card-border);
      border-radius: 14px; padding: 26px; backdrop-filter: blur(16px);
      transition: all 0.25s ease;
    }}
    .card:hover {{ border-color: rgba(99, 102, 241, 0.4); transform: translateY(-3px); }}
    .card-icon {{
      width: 44px; height: 44px; border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; margin-bottom: 16px;
      background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3);
    }}
    .card h3 {{ font-size: 18px; font-weight: 700; margin-bottom: 8px; }}
    .card p {{ font-size: 14px; color: var(--text-muted); }}

    /* Pricing Section */
    .pricing-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; max-width: 960px; margin: 0 auto 90px; }}
    .price-card {{
      background: var(--card-bg); border: 1px solid var(--card-border);
      border-radius: 16px; padding: 32px; text-align: left; position: relative;
    }}
    .price-card.featured {{
      border: 2px solid var(--gold);
      background: linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(18, 22, 34, 0.85) 100%);
      box-shadow: 0 0 35px rgba(245, 158, 11, 0.15);
    }}
    .ribbon {{
      position: absolute; top: 16px; right: 16px;
      background: var(--gold); color: #000; font-size: 11px; font-weight: 800;
      padding: 4px 10px; border-radius: 12px; text-transform: uppercase;
    }}
    .price {{ font-size: 38px; font-weight: 800; margin: 16px 0; }}
    .price span {{ font-size: 15px; color: var(--text-muted); font-weight: 500; }}
    .price-list {{ list-style: none; margin: 24px 0; font-size: 14px; display: flex; flexDirection: column; gap: 10px; }}
    .price-list li {{ display: flex; align-items: center; gap: 8px; color: var(--text-muted); }}
    .price-list li b {{ color: var(--text); }}

    /* License Checker Tool */
    .tool-box {{
      background: var(--card-bg); border: 1px solid var(--card-border);
      border-radius: 16px; padding: 32px; max-width: 720px; margin: 0 auto 90px; text-align: left;
    }}
    .form-group {{ margin-bottom: 16px; }}
    .form-group label {{ display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; }}
    .input {{
      width: 100%; padding: 11px 14px; border-radius: 8px;
      background: rgba(0, 0, 0, 0.3); border: 1px solid var(--card-border);
      color: #fff; font-size: 14px; outline: none;
    }}
    .input:focus {{ border-color: var(--accent); }}

    /* Admin Drawer */
    #adminPanel {{
      display: none; background: #0a0d14; border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px; padding: 32px; margin-bottom: 80px;
    }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 13px; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--card-border); text-align: left; }}
    th {{ color: var(--text-muted); font-weight: 600; }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--card-border); padding: 48px 0;
      color: var(--text-muted); font-size: 14px; text-align: center;
    }}
    .footer-links {{ display: flex; justify-content: center; gap: 24px; margin-bottom: 16px; }}
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="container nav">
      <div class="brand">
        <div class="brand-tile">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><path d="M12 2v13m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg>
        </div>
        <span>AUDIRA <span style="color:#60a5fa">DOWNLOAD</span></span>
      </div>
      <div class="nav-links">
        <a href="#fitur">Fitur</a>
        <a href="#kecepatan">Kecepatan</a>
        <a href="#harga">Lisensi PRO</a>
        <a href="#checker">Cek Serial Key</a>
        <button class="btn btn-outline" onclick="toggleAdminPanel()">Portal Admin</button>
        <a href="#harga" class="btn btn-gold">Beli Lisensi PRO</a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero container">
    <div class="badge">
      <span>🚀 AUDIIRA DOWNLOAD MANAGER (ADM) v1.1.7 IS LIVE</span>
    </div>
    <h1>
      Download File Berkecepatan Turbo.<br>
      <span>32 Koneksi Paralel. Bebas Iklan.</span>
    </h1>
    <p class="hero-lead">
      Pengunduh berkas modern berbasis Rust & Tauri 2. Mengakselerasi kecepatan hingga 15× lipat, pemulih unduhan tahan pemadaman listrik, penangkap video streaming 8K HDR, serta hub model AI lokal.
    </p>
    <div class="hero-cta">
      <a href="https://github.com/FortoGraphy/prism-download-manager/releases" class="btn btn-primary" style="font-size:16px; padding:12px 28px;">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
        Unduh Gratis (Windows/Mac/Linux)
      </a>
      <a href="https://wa.me/6282112001600?text=Halo%20AUDIRA,%20saya%20ingin%20membeli%20lisensi%20Audira%20Download%20Manager%20Pro" target="_blank" class="btn btn-gold" style="font-size:16px; padding:12px 28px;">
        ⭐ Beli Lisensi PRO Lifetime
      </a>
    </div>

    <!-- Live Benchmark Visualizer -->
    <div class="bench-box" id="kecepatan">
      <div class="bench-title">
        <span>📊 Perbandingan Kecepatan Nyata (Server Ber-Throttle 1 GiB)</span>
        <span style="color:var(--green); font-size:13px;">✔ Verified SHA-256</span>
      </div>
      <div class="bench-row">
        <div class="bench-label">
          <span>Browser Normal (1 Koneksi Single-Thread)</span>
          <span>4.0 MiB/s</span>
        </div>
        <div class="bench-bar-wrap"><div class="bench-bar bar-browser"></div></div>
      </div>
      <div class="bench-row">
        <div class="bench-label">
          <span>Internet Download Manager / aria2c</span>
          <span>32.0 MiB/s</span>
        </div>
        <div class="bench-bar-wrap"><div class="bench-bar bar-legacy"></div></div>
      </div>
      <div class="bench-row">
        <div class="bench-label">
          <span style="color:#a7f3d0">⚡ Audira Download Manager PRO (32 Segmen Turbo)</span>
          <span style="color:#a7f3d0">60.9 MiB/s (15× Lebih Cepat)</span>
        </div>
        <div class="bench-bar-wrap"><div class="bench-bar bar-audira"></div></div>
      </div>
    </div>
  </section>

  <!-- Feature Grid -->
  <section class="container" id="fitur">
    <h2 class="section-title">Fitur Kelas Industri</h2>
    <p class="section-sub">Diciptakan untuk kecepatan maksimal tanpa kompromi privasi.</p>
    <div class="grid-3">
      <div class="card">
        <div class="card-icon">⚡</div>
        <h3>Dynamic Work-Stealing</h3>
        <p>Membagi unduhan hingga 32 koneksi simultan. Jika salah satu server lambat, bagian terbesar tersisa otomatis dipecah dua sehingga kecepatan tetap di puncak hingga byte terakhir.</p>
      </div>
      <div class="card">
        <div class="card-icon">💾</div>
        <h3>Zero-Copy Sparse Writing</h3>
        <p>Data langsung ditulis ke posisi akhir berkas pada hard disk (sparse file NTFS). Menghilangkan proses perakitan berkas sementara (*merging*) yang lambat saat download selesai.</p>
      </div>
      <div class="card">
        <div class="card-icon">🎬</div>
        <h3>8K Video & Audio Grabber</h3>
        <p>Mendukung 1.800+ portal streaming (YouTube, TikTok, Bilibili, dll.). Ekstraksi resolusi hingga 8K HDR, subtitle multi-bahasa, atau diekstrak murni menjadi MP3 320kbps.</p>
      </div>
      <div class="card">
        <div class="card-icon">🤖</div>
        <h3>AI Model Hub (Hugging Face)</h3>
        <p>Pencarian dan pengunduhan bobot model LLM (GGUF, SafeTensors) langsung dari aplikasi dengan verifikasi hash SHA-256 dan integrasi ke folder LM Studio.</p>
      </div>
      <div class="card">
        <div class="card-icon">🛡️</div>
        <h3>Tahan Crash & Padam Listrik</h3>
        <p>Titik resume disimpan berkala di SQLite WAL. Anda dapat mematikan laptop atau mencabut kabel sewaktu-waktu dan melanjutkan tepat di posisi terakhir tanpa berkas korup.</p>
      </div>
      <div class="card">
        <div class="card-icon">🌐</div>
        <h3>Ekstensi Browser Terintegrasi</h3>
        <p>Tersedia untuk Google Chrome, Microsoft Edge, Brave, Opera, Vivaldi, dan Mozilla Firefox dengan transmisi Native Messaging berkecepatan tinggi.</p>
      </div>
    </div>
  </section>

  <!-- Pricing Table -->
  <section class="container" id="harga">
    <h2 class="section-title">Pilihan Paket & Lisensi Resmi</h2>
    <p class="section-sub">Gunakan versi gratis selamanya atau upgrade ke Audira PRO untuk performa tanpa batas.</p>
    <div class="pricing-grid">
      <!-- Free -->
      <div class="price-card">
        <h3>Free Edition</h3>
        <p style="color:var(--text-muted); font-size:13px;">Untuk kebutuhan pengunduhan sehari-hari.</p>
        <div class="price">Rp 0 <span>/ selamanya</span></div>
        <ul class="price-list">
          <li>✔ Maksimal 6 koneksi simultan</li>
          <li>✔ Resume berkas terputus</li>
          <li>✔ Video grabber hingga 1080p</li>
          <li>✔ Ekstensi browser lengkap</li>
          <li>✖ Fitur 32 koneksi paralel turbo</li>
          <li>✖ Ekstraksi video 4K / 8K HDR</li>
          <li>✖ Penjadwal otomatis shutdown PC</li>
        </ul>
        <a href="#fitur" class="btn btn-outline" style="width:100%; justify-content:center;">Unduh Versi Gratis</a>
      </div>

      <!-- Pro Lifetime -->
      <div class="price-card featured">
        <div class="ribbon">Paling Populer</div>
        <h3 style="color:var(--gold);">Audira PRO Lifetime</h3>
        <p style="color:var(--text-muted); font-size:13px;">Lisensi permanen sekali bayar untuk seumur hidup.</p>
        <div class="price" style="color:var(--gold);">Rp 99.000 <span>/ 1x bayar</span></div>
        <ul class="price-list">
          <li>✔ <b>32 Koneksi Paralel Simultan Turbo</b></li>
          <li>✔ <b>Kecepatan Penuh Tanpa Throttling</b></li>
          <li>✔ <b>Video Grabber 4K & 8K HDR + MP3 320k</b></li>
          <li>✔ <b>Pengunduh AI Hugging Face Tanpa Kuota</b></li>
          <li>✔ <b>Auto Sleep & PC Shutdown On Finish</b></li>
          <li>✔ <b>Kunci Lisensi Terikat HWID Mesin</b></li>
          <li>✔ <b>Dukungan Prioritas VIP via WhatsApp</b></li>
        </ul>
        <a href="https://wa.me/6282112001600?text=Halo%20AUDIRA,%20saya%20ingin%20membeli%20Lisensi%20Audira%20Download%20Manager%20PRO%20Lifetime%20(Rp%2099.000)" target="_blank" class="btn btn-gold" style="width:100%; justify-content:center;">
          Beli Lisensi PRO via WhatsApp
        </a>
      </div>
    </div>
  </section>

  <!-- License Key Checker Tool -->
  <section class="container" id="checker">
    <div class="tool-box">
      <h3 style="margin-bottom:8px; font-size:20px;">🔍 Cek Keaslian & Validitas Serial Key</h3>
      <p style="font-size:13px; color:var(--text-muted); margin-bottom:20px;">
        Verifikasi keabsahan lisensi resmi Audira Download Manager Anda secara langsung ke server kriptografi AUDIRA.
      </p>
      <form id="checkForm" onsubmit="handleVerifyLicense(event)">
        <div class="form-group">
          <label>Serial Key Lisensi:</label>
          <input type="text" id="chkKey" class="input" placeholder="ADM-LIFE-0-XXXXXXXXXXXXXXXX" required style="font-family:monospace; text-transform:uppercase;">
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;" class="form-group">
          <div>
            <label>Nama Pemilik Terdaftar:</label>
            <input type="text" id="chkName" class="input" placeholder="Contoh: Agus Dwi Rianto" required>
          </div>
          <div>
            <label>Email Terdaftar:</label>
            <input type="email" id="chkEmail" class="input" placeholder="nama@email.com" required>
          </div>
        </div>
        <button type="submit" class="btn btn-primary" id="btnCheck">Cek Status Lisensi</button>
      </form>
      <div id="checkResult" style="display:none; margin-top:16px; padding:14px; border-radius:8px; font-size:13px;"></div>
    </div>
  </section>

  <!-- Admin Console & Generator (Toggled) -->
  <section class="container" id="adminPanel">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <h2>👑 AUDIRA Central Fleet & License Management Console</h2>
      <button class="btn btn-outline" onclick="toggleAdminPanel()">Tutup Panel</button>
    </div>

    <!-- Generator Box -->
    <div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:12px; margin-bottom:24px; border:1px solid var(--card-border);">
      <h3 style="font-size:16px; margin-bottom:12px; color:var(--gold);">⚡ Buat Serial Key Baru (Admin Generator)</h3>
      <form id="genForm" onsubmit="handleGenerateKey(event)" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)) 140px; gap:12px; align-items:end;">
        <div>
          <label style="font-size:12px; display:block; margin-bottom:4px;">Nama Pembeli:</label>
          <input type="text" id="genName" class="input" placeholder="Agus Dwi Rianto" required>
        </div>
        <div>
          <label style="font-size:12px; display:block; margin-bottom:4px;">Email Pembeli:</label>
          <input type="email" id="genEmail" class="input" placeholder="user@gmail.com" required>
        </div>
        <div>
          <label style="font-size:12px; display:block; margin-bottom:4px;">Tipe Paket:</label>
          <select id="genTier" class="input">
            <option value="LIFE">Pro Lifetime (0 Exp)</option>
            <option value="YEAR">Pro Annual (1 Tahun)</option>
          </select>
        </div>
        <button type="submit" class="btn btn-gold" style="height:42px;">Generate</button>
      </form>
      <div id="genResult" style="display:none; margin-top:12px; padding:12px; background:rgba(16, 185, 129, 0.15); border:1px solid rgba(16, 185, 129, 0.4); border-radius:6px; font-family:monospace;"></div>
    </div>

    <!-- Active Licenses Table -->
    <h3 style="font-size:16px; margin-bottom:8px;">Daftar Lisensi Terdaftar di Database:</h3>
    <button class="btn btn-outline" style="font-size:12px; padding:4px 10px; margin-bottom:12px;" onclick="loadLicensesTable()">Refresh Data</button>
    <div style="overflow-x:auto;">
      <table id="licTable">
        <thead>
          <tr>
            <th>ID</th>
            <th>Serial Key</th>
            <th>Tipe</th>
            <th>Pemilik</th>
            <th>Email</th>
            <th>Machine HWID</th>
            <th>Status</th>
            <th>Tanggal Dibuat</th>
          </tr>
        </thead>
        <tbody id="licBody">
          <tr><td colspan="8">Klik tombol Refresh untuk memuat daftar lisensi...</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <div class="container">
      <div class="footer-links">
        <a href="https://audira.my.id">Portal Resmi AUDIRA</a>
        <a href="https://wa.me/6282112001600">WhatsApp Billing (+62 821-1200-1600)</a>
        <a href="mailto:agusdwirianto@gmail.com">Email Dukungan Teknis</a>
      </div>
      <p><b>Audira Download Manager (ADM)</b> adalah produk resmi ekosistem teknologi <b>AUDIRA</b>.</p>
      <p style="margin-top:4px;">Lead Architect & Founder: <b>Agus Dwi Rianto</b> • Badan Usaha: <b>Audira Multimedia Digital / Audira Sukses Mandiri</b></p>
      <p style="margin-top:8px; font-size:12px; color:#64748b;">© 2026 Agus Dwi Rianto (AUDIRA). Hak Cipta Dilindungi Undang-Undang.</p>
    </div>
  </footer>

  <script>
    function toggleAdminPanel() {{
      const p = document.getElementById("adminPanel");
      if (p.style.display === "block") {{
        p.style.display = "none";
      }} else {{
        p.style.display = "block";
        p.scrollIntoView({{ behavior: "smooth" }});
        loadLicensesTable();
      }}
    }}

    async function handleVerifyLicense(e) {{
      e.preventDefault();
      const btn = document.getElementById("btnCheck");
      const res = document.getElementById("checkResult");
      btn.innerText = "Memvalidasi...";
      res.style.display = "none";

      try {{
        const resp = await fetch("/api/v1/license/verify", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            key: document.getElementById("chkKey").value.trim(),
            owner_name: document.getElementById("chkName").value.trim(),
            email: document.getElementById("chkEmail").value.trim()
          }})
        }});
        const data = await resp.json();
        res.style.display = "block";
        if (resp.ok && data.valid) {{
          res.style.background = "rgba(16, 185, 129, 0.15)";
          res.style.border = "1px solid rgba(16, 185, 129, 0.4)";
          res.style.color = "#a7f3d0";
          res.innerHTML = `<b>✔ LISENSI RESMI & TERVALIDASI</b><br>
            Tipe: <b>${{data.tier}}</b><br>
            Pemilik: ${{data.owner_name}}<br>
            Email: ${{data.email}}<br>
            Status: ${{data.message}}`;
        }} else {{
          res.style.background = "rgba(239, 68, 68, 0.15)";
          res.style.border = "1px solid rgba(239, 68, 68, 0.4)";
          res.style.color = "#fca5a5";
          res.innerHTML = `<b>❌ VALIDASI GAGAL</b><br>${{data.message || "Data lisensi tidak cocok"}}`;
        }}
      }} catch (err) {{
        res.style.display = "block";
        res.style.background = "rgba(239, 68, 68, 0.15)";
        res.style.color = "#fca5a5";
        res.innerHTML = "Gagal menghubungi server validasi.";
      }} finally {{
        btn.innerText = "Cek Status Lisensi";
      }}
    }}

    async function handleGenerateKey(e) {{
      e.preventDefault();
      const res = document.getElementById("genResult");
      res.style.display = "none";

      try {{
        const resp = await fetch("/api/v1/license/generate", {{
          method: "POST",
          headers: {{
            "Content-Type": "application/json",
            "Authorization": "Basic " + btoa("audira:Sigma1993")
          }},
          body: JSON.stringify({{
            owner_name: document.getElementById("genName").value.trim(),
            email: document.getElementById("genEmail").value.trim(),
            tier: document.getElementById("genTier").value,
            expires_at: document.getElementById("genTier").value === "YEAR" ? Math.floor(Date.now()/1000 + 365*86400) : 0
          }})
        }});
        const data = await resp.json();
        if (resp.ok && data.success) {{
          res.style.display = "block";
          res.innerHTML = `<b>Kunci Berhasil Dibuat:</b> <span style="color:#fde047">${{data.key}}</span><br>
            <span style="font-size:12px; color:#cbd5e1;">Atas Nama: ${{data.owner_name}} (${{data.email}}) | ${{data.tier}}</span>`;
          loadLicensesTable();
        }} else {{
          alert(data.error || "Gagal membuat kunci");
        }}
      }} catch (err) {{
        alert("Gagal menghubungi server generator");
      }}
    }}

    async function loadLicensesTable() {{
      const tbody = document.getElementById("licBody");
      try {{
        const resp = await fetch("/api/v1/licenses", {{
          headers: {{ "Authorization": "Basic " + btoa("audira:Sigma1993") }}
        }});
        const data = await resp.json();
        if (resp.ok && data.licenses) {{
          if (data.licenses.length === 0) {{
            tbody.innerHTML = "<tr><td colspan='8'>Belum ada lisensi tersimpan.</td></tr>";
            return;
          }}
          tbody.innerHTML = data.licenses.map(l => `
            <tr>
              <td>#${{l.id}}</td>
              <td><b style="font-family:monospace; color:#60a5fa">${{l.key}}</b></td>
              <td><span style="color:${{l.tier==='LIFE'?'#f59e0b':'#38bdf8'}}">${{l.tier==='LIFE'?'Lifetime':'Annual'}}</span></td>
              <td>${{l.owner_name}}</td>
              <td>${{l.email}}</td>
              <td style="font-family:monospace; font-size:11px;">${{l.hwid || '<i>Belum Terikat</i>'}}</td>
              <td><span style="color:${{l.status==='ACTIVE'?'#10b981':'#ef4444'}}">${{l.status}}</span></td>
              <td>${{l.created_at}}</td>
            </tr>
          `).join("");
        }}
      }} catch (err) {{
        tbody.innerHTML = "<tr><td colspan='8'>Gagal memuat data dari server.</td></tr>";
      }}
    }}
  </script>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------

def run_server(port=None):
    global PORT
    if port is not None:
        PORT = port
    init_db()
    seed_default_license()

    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, AdmPortalHandler)
    msg = f"""
========================================================================
 AUDIRA DOWNLOAD MANAGER (ADM) - CENTRAL LICENSING PORTAL & SERVER
========================================================================
 Web Portal & Landing Page : http://localhost:{PORT}/
 Admin Management Console  : http://localhost:{PORT}/portal
 REST API Endpoint         : http://localhost:{PORT}/api/v1/license/verify
 Database Storage          : {DB_PATH}
 Author & Lead Architect   : Agus Dwi Rianto (AUDIRA Ecosystem)
 WhatsApp Billing Hotline  : +62 821-1200-1600
========================================================================
Server aktif dan siap melayani permintaan...
    """
    try:
        print(msg)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server dimatikan dengan aman.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
