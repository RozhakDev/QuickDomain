# QuickDomain Pro: Pindai Domain Secepat Kilat ⚡

![QuickDomain - Logo](https://github.com/user-attachments/assets/8af84482-05ca-4825-a896-3f003128f11b)

**QuickDomain Pro** adalah alat baris perintah (CLI) berbasis Python yang dirancang untuk memeriksa status HTTP/HTTPS dari daftar domain secara massal dengan kecepatan tinggi. Dibangun dengan arsitektur asinkronus menggunakan `asyncio` dan `aiohttp`, proyek ini mengutamakan performa, kebersihan kode, dan kemudahan penggunaan. Cocok untuk pengembang, administrator sistem, atau peneliti keamanan siber yang perlu memvalidasi domain secara efisien. 😎

Proyek ini adalah rekayasa ulang dari versi sebelumnya, kini dengan pendekatan **Object-Oriented Programming (OOP)**, logging profesional dalam Bahasa Indonesia, dan antarmuka CLI yang intuitif menggunakan `argparse`. QuickDomain Pro juga jadi studi kasus keren buat kamu yang pengen belajar praktik terbaik dalam pengembangan perangkat lunak Python! 💻

## ✨ Fitur Utama

- **Pemindaian Super Cepat**: Manfaatkan `asyncio` dan `aiohttp` untuk menangani ribuan domain secara bersamaan.
- **Ekstraksi Domain Cerdas**: Deteksi dan ekstrak domain valid dari berbagai format file (`.txt`, `.json`, atau data tidak terstruktur) dengan regex.
- **Logging Profesional**: Hasilkan log yang rapi, berwarna di konsol, dan tersimpan ke file untuk analisis lebih lanjut.
- **Arsitektur Bersih**: Kode modular dengan pemisahan tanggung jawab antara ekstraksi, pemindaian, dan logging.
- **Kontrol Konkurensi**: Atur jumlah permintaan simultan dengan semaphore untuk mencegah pemblokiran IP.
- **Antarmuka CLI Intuitif**: Gunakan `argparse` untuk opsi fleksibel, cocok untuk otomatisasi atau penggunaan manual.

## 🏗️ Struktur Proyek

```plaintext
quickdomain_pro/
│
├── results/                    # Direktori untuk menyimpan file log hasil pemindaian
│
├── quickdomain/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── extractor.py        # Kelas untuk ekstraksi domain
│   │   └── scanner.py          # Kelas untuk pemindaian domain
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py           # Modul untuk konfigurasi logging
│   │
│   └── __init__.py
│
├── .gitignore                  # Mengabaikan file yang tidak perlu dilacak
├── main.py                     # Titik masuk utama aplikasi
├── README.md                   # Dokumentasi proyek (yang lagi kamu baca ini!)
└── requirements.txt            # Daftar dependensi Python
```

## 🚀 Instalasi

### Persyaratan

- **Python**: Versi 3.8 atau lebih baru.
- **Sistem Operasi**: Windows, macOS, atau Linux.

### Langkah-langkah

1. **Clone Repositori**  
   Salin proyek ke mesin lokalmu:
   
   ```bash
   git clone https://github.com/RozhakDev/QuickDomain.git
   cd QuickDomain
   ```

2. **Buat Virtual Environment** (Disarankan)  
   Buat dan aktifkan lingkungan virtual untuk menjaga dependensi tetap rapi:
   
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Instal Dependensi**  
   Instal semua library yang dibutuhkan:
   
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Penggunaan

Jalankan QuickDomain Pro melalui `main.py` dengan argumen yang diperlukan. Berikut sintaks dasarnya:

```bash
python main.py --file <path_ke_file_domain> [opsi_lainnya]
```

### Contoh Perintah

- **Scan domain dengan pengaturan default**:
  
  ```bash
  python main.py --file domains.txt
  ```
  
  Memindai domain dari `domains.txt` dengan protokol `http` dan `https`, konkurensi 100, dan timeout 10 detik.

- **Scan dengan konkurensi tinggi**:
  
  ```bash
  python main.py --file data.json --concurrency 200
  ```
  
  Memindai domain dari file JSON dengan 200 koneksi simultan.

- **Scan hanya dengan HTTPS dan output kustom**:
  
  ```bash
  python main.py --file domains.txt --protocols https --output hasil_aman.log
  ```
  
  Memindai hanya protokol HTTPS dan menyimpan log ke `hasil_aman.log`.

### Opsi Argumen

| Argumen               | Deskripsi                                                           | Default                            |
| --------------------- | ------------------------------------------------------------------- | ---------------------------------- |
| `-f`, `--file`        | (Wajib) Path ke file input berisi daftar domain (.txt, .json, dll). | -                                  |
| `-o`, `--output`      | Nama file untuk menyimpan log hasil pemindaian.                     | `results/scan_log_{timestamp}.log` |
| `-c`, `--concurrency` | Jumlah permintaan asinkron yang berjalan bersamaan.                 | 100                                |
| `-p`, `--protocols`   | Protokol yang akan diperiksa (`http`, `https`).                     | `http https`                       |
| `-t`, `--timeout`     | Waktu tunggu (detik) untuk setiap permintaan.                       | 10                                 |

## 🤝 Kontribusi

Kami sangat terbuka untuk kontribusi! 😊 Jika kamu punya ide untuk fitur baru, perbaikan bug, atau optimasi kode, ikuti langkah ini:

1. Fork repositori ini.
2. Buat branch baru (`git checkout -b fitur/ide-kamu`).
3. Commit perubahanmu (`git commit -m "Menambahkan fitur X"`).
4. Push ke branch (`git push origin fitur/ide-kamu`).
5. Buat Pull Request dan ceritain apa yang kamu ubah.

## 📜 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE). Silakan gunakan, modifikasi, dan bagikan sesukamu! 😄