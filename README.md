# Ninja Income Bot

Bot otomatis untuk klaim hadiah harian dari Ninja Heroes New Era (Kageherostudio).

## ✨ Fitur

- ✅ Login otomatis dengan kredensial email/password
- ✅ Pilih server tertentu (Server 49)
- ✅ Klaim hadiah harian secara otomatis
- ✅ Logging lengkap untuk debugging
- ✅ Support scheduling harian via cron

## 📋 Requirements

- Python 3.7+
- `requests` library
- `beautifulsoup4` library
- `python-dotenv` library

## 🚀 Instalasi

### 1. Install dependencies

```bash
pip3 install requests beautifulsoup4 python-dotenv --break-system-packages
```

### 2. Konfigurasi kredensial

Buat file `.env` dengan isi:

```env
NH_EMAIL=your-email@example.com
NH_PASSWORD=your-password-here
NH_SERVER=49
```

> **PENTING**: Jangan commit file `.env` ke repository! File ini sudah masuk `.gitignore`.

### 3. Test run

```bash
python3 bot.py
```

Output yang diharapkan:
```
[2026-07-26 11:46:01] === Ninja Income Daily Claim ===
[2026-07-26 11:46:01] Login response: {'message': 'success', 'data': 'Login is successful'}
Login berhasil!
Menemukan server: 'Server 49 - K46 [Lv. 4]' dengan value '49'
Mengklaim: Iron Bar x3 (ID: 1265, Period: 43, Server: 49)
Claim response: {'message': 'success', 'data': 'Ninja income is successfully claimed'}
Berhasil mengklaim hadiah!
```

## ⏰ Automasi Harian (Cron)

Untuk menjalankan bot setiap hari secara otomatis:

### Menggunakan Crontab

```bash
# Edit crontab
crontab -e

# Tambahkan baris ini untuk run setiap hari jam 9 pagi
0 9 * * * cd /opt/dev/projects/ninja-income-bot && /usr/bin/python3 bot.py >> logs/claim.log 2>&1
```

### Menggunakan Systemd Timer (Opsional)

Lihat file `install-systemd.sh` untuk setup systemd timer.

## 📁 Struktur Project

```
ninja-income-bot/
├── bot.py              # Script utama
├── .env                # Kredensial (JANGAN COMMIT!)
├── .env.example        # Contoh konfigurasi
├── README.md           # Dokumentasi ini
├── install-cron.sh     # Script install cron job
├── install-systemd.sh  # Script install systemd timer
└── logs/               # Folder untuk log (auto-created)
```

## 🔧 Troubleshooting

### Login gagal

- Pastikan email dan password benar di `.env`
- Cek koneksi internet
- Pastikan akun tidak di-ban atau sedang maintenance

### Server tidak ditemukan

- Pastikan `NH_SERVER` di `.env` sesuai dengan server Anda
- Script akan menampilkan list server yang tersedia jika tidak cocok

### Hadiah sudah diklaim

- Bot hanya bisa klaim sekali per hari
- Tunggu reset harian di server game

## ⚠️ Catatan Penting

1. **Keamanan**: File `.env` berisi kredensial sensitif. Jangan share atau commit ke repository public.
2. **Rate Limit**: Jangan spam request ke server. Bot sudah didesain untuk sekali klaim per run.
3. **Terms of Service**: Pastikan bot ini tidak melanggar ToS game. Bot ini hanya untuk akun pribadi Anda.
4. **Hadiah Distribution**: Item akan didistribusikan setelah 3x24 jam sesuai kebijakan Kageherostudio.

## 📝 Changelog

### v1.0.0 (2026-07-26)
- Initial release
- Login otomatis
- Pilih server otomatis
- Klaim hadiah harian
- Support environment variable via .env

## 📄 License

MIT License - Gunakan untuk keperluan pribadi Anda.

## 🙏 Credits

Dibuat dengan bantuan Hermes AI Agent