#!/usr/bin/env python3
"""
Ninja Heroes New Era - Daily Reward Claimer (multi akun)
https://kageherostudio.com/event/?event=daily

Format akun (pilih salah satu):

A) .env bernomor (cocok untuk PC / Termux):
   NH_EMAIL_1=akun1@mail.com
   NH_PASSWORD_1=passwordnya
   NH_SERVER_1=46
   NH_EMAIL_2=akun2@mail.com
   NH_PASSWORD_2=passwordnya
   NH_SERVER_2=49

B) NH_ACCOUNTS, satu akun per baris dengan format email|password|server
   (cocok untuk 1 GitHub Secret):
   akun1@mail.com|passwordnya|46
   akun2@mail.com|passwordnya|49

C) Format lama tetap jalan: NH_EMAIL, NH_PASSWORD, NH_SERVER
"""

import os
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_URL = "https://kageherostudio.com/event"
LOGIN_URL = f"{BASE_URL}/index_.php?act=login"
CHECK_LOGIN_URL = f"{BASE_URL}/index_.php?act=check_login"
DAILY_URL = f"{BASE_URL}/index_.php?act=daily"
EVENT_URL = f"{BASE_URL}/?event=daily"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': EVENT_URL,
}

DELAY_ANTAR_AKUN = 5  # detik


def mask(email):
    """a***@mail.com supaya aman di log"""
    if "@" not in email:
        return email[:2] + "***"
    user, dom = email.split("@", 1)
    return f"{user[:2]}***@{dom}"


def load_accounts():
    accounts = []

    # Format B: NH_ACCOUNTS
    raw = os.getenv("NH_ACCOUNTS", "").strip()
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) != 3:
            print(f"PERINGATAN: baris NH_ACCOUNTS dilewati (format harus email|password|server)")
            continue
        accounts.append(tuple(p.strip() for p in parts))

    # Format A: NH_EMAIL_1, NH_EMAIL_2, ...
    for i in range(1, 51):
        email = os.getenv(f"NH_EMAIL_{i}", "").strip()
        if not email:
            continue
        accounts.append((email, os.getenv(f"NH_PASSWORD_{i}", ""), os.getenv(f"NH_SERVER_{i}", "").strip()))

    # Format C: lama
    email = os.getenv("NH_EMAIL", "").strip()
    if email:
        accounts.append((email, os.getenv("NH_PASSWORD", ""), os.getenv("NH_SERVER", "").strip()))

    return [a for a in accounts if a[0] and a[1] and a[2]]


def login(session, email, password):
    session.get(EVENT_URL)
    r = session.post(LOGIN_URL, data={'txtuserid': email, 'txtpassword': password})
    try:
        resp = r.json()
        print(f"[{datetime.now()}] Login response:", resp)
        return resp.get('message') == 'success'
    except Exception as e:
        print(f"Error parsing login response: {e}")
        print(r.text[:300])
        return False


def get_server_id(session, target_server):
    r = session.post(CHECK_LOGIN_URL)
    try:
        resp = r.json()
        if resp.get('message') != 'success':
            print("Belum login, coba login dulu.")
            return None
    except Exception:
        pass

    r = session.get(EVENT_URL)
    if r.status_code != 200:
        print(f"Gagal mengambil halaman event: {r.status_code}")
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    select = soup.find('select', {'name': 'selserver'})
    if not select:
        print("Dropdown server tidak ditemukan.")
        return None

    target = target_server.strip()
    options = [(o.get('value'), o.get_text(strip=True)) for o in select.find_all('option') if o.get('value')]

    # Prioritas 1: value dropdown persis sama
    for val, text in options:
        if val == target:
            print(f"Menemukan server: '{text}' dengan value '{val}'")
            return val

    # Prioritas 2: teks "Server <angka>" persis
    pattern = re.compile(rf"Server\s*{re.escape(target)}(?!\d)", re.IGNORECASE)
    for val, text in options:
        if pattern.search(text):
            print(f"Menemukan server: '{text}' dengan value '{val}'")
            return val

    print("Tidak menemukan server yang cocok. Opsi yang tersedia:")
    for val, text in options:
        print(f"  value='{val}', text='{text}'")
    return None


def claim_daily(session, server_id):
    """True = berhasil, None = tidak ada yang diklaim, False = gagal"""
    r = session.get(EVENT_URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    item = soup.find('div', class_='dailyClaim reward-star')
    if not item:
        item = None
        for div in soup.find_all('div', class_='dailyClaim'):
            if 'grayscale' not in div.get('class', []):
                item = div
                break

    if not item:
        print("Tidak ada hadiah yang bisa diklaim hari ini (kemungkinan sudah diklaim).")
        return None

    item_id = item.get('data-id')
    period_id = item.get('data-period')
    print(f"Mengklaim: {item.get('data-name')} (ID: {item_id}, Period: {period_id}, Server: {server_id})")

    r = session.post(DAILY_URL, data={'itemId': item_id, 'periodId': period_id, 'selserver': server_id})
    try:
        resp = r.json()
        print("Claim response:", resp)
        return resp.get('message') == 'success'
    except Exception as e:
        print(f"Error claiming: {e}")
        print(r.text[:300])
        return False


def run_account(email, password, server):
    """Return True jika sukses/tidak ada klaim, False jika gagal."""
    session = requests.Session()   # sesi terpisah per akun, cookie tidak tercampur
    session.headers.update(HEADERS)

    if not login(session, email, password):
        print("Login gagal!")
        return False
    print("Login berhasil!")

    server_id = get_server_id(session, server)
    if not server_id:
        print("Gagal mendapatkan ID server.")
        return False

    result = claim_daily(session, server_id)
    if result is True:
        print("Berhasil mengklaim hadiah!")
        return True
    if result is None:
        return True
    print("Gagal mengklaim hadiah.")
    return False


def main():
    accounts = load_accounts()
    if not accounts:
        print("ERROR: tidak ada akun. Isi NH_EMAIL/NH_PASSWORD/NH_SERVER, "
              "NH_EMAIL_1.., atau NH_ACCOUNTS (lihat bagian atas bot.py)")
        return 1

    print(f"[{datetime.now()}] === Ninja Income Daily Claim | {len(accounts)} akun ===")
    hasil = []
    for n, (email, password, server) in enumerate(accounts, 1):
        print(f"\n--- Akun {n}/{len(accounts)}: {mask(email)} (server {server}) ---")
        try:
            ok = run_account(email, password, server)
        except Exception as e:   # satu akun error tidak boleh menghentikan akun lain
            print(f"Error tak terduga: {type(e).__name__}: {e}")
            ok = False
        hasil.append((mask(email), ok))
        if n < len(accounts):
            time.sleep(DELAY_ANTAR_AKUN)

    print("\n=== RINGKASAN ===")
    for email, ok in hasil:
        print(f"  {'OK   ' if ok else 'GAGAL'}  {email}")
    return 0 if all(ok for _, ok in hasil) else 1


if __name__ == "__main__":
    sys.exit(main())
