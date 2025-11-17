# 🗺️ Google Maps Lead Scraper - Improved Version v18

Scraper profesional untuk mengambil data bisnis dari Google Maps dengan fitur email extraction otomatis.

## 🚀 Fitur Baru

### ✅ Improvements dari Versi Sebelumnya:

1. **Logging System** - Tracking lengkap dengan file log
2. **Configuration Management** - Semua settings terpusat di `config.py`
3. **Retry Mechanism** - Auto retry dengan exponential backoff
4. **Progress Tracking** - Monitor progress secara real-time
5. **Helper Functions** - Code lebih clean dan maintainable
6. **Better Error Handling** - Error messages yang informatif
7. **Email Validation** - Validasi email yang lebih robust
8. **Type Hints** - Type safety untuk reduce bugs
9. **Graceful Shutdown** - Handle Ctrl+C dengan baik
10. **Modular Architecture** - Separated concerns
11. **🆕 Data Validation** - 4 mode filtering untuk quality control
12. **🆕 Statistics Report** - Detailed analytics setelah scraping

### 🎯 Fitur Utama:

- ✅ Scraping data bisnis dari Google Maps
- ✅ Email extraction dari website bisnis (3 metode)
- ✅ Export ke CSV dengan encoding UTF-8-sig (Excel-friendly)
- ✅ Auto-scroll dengan detection end of list
- ✅ Headless mode support
- ✅ Anti-stuck mechanism untuk website lambat
- ✅ **🆕 Data validation dengan 4 mode** (STRICT/MODERATE/LENIENT/NONE)
- ✅ **🆕 Detailed statistics report** dengan breakdown skip reasons

## 📦 Instalasi

```bash
# Clone atau download project

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Cara Penggunaan

### Basic Usage:

```bash
python gmaps_scraper.py
```

Kemudian ikuti prompt:
1. Masukkan kata kunci pencarian (contoh: "travel agent di Jakarta")
2. Masukkan maksimal scroll (default: 15)
3. **🆕 Pilih validation mode (1-4)**:
   - **STRICT** - Semua field wajib (~10-20% data)
   - **MODERATE** - Minimal: nama, website, email (~20-30% data) [RECOMMENDED]
   - **LENIENT** - Minimal: nama, telepon (~80-90% data)
   - **NONE** - Simpan semua (~100% data)
4. Pilih headless mode atau tidak (y/n)

### Programmatic Usage:

```python
from gmaps_scraper import GoogleMapsScraper

scraper = GoogleMapsScraper(headless=False)
output_file, success_count = scraper.run(
    query="travel agent di Jakarta",
    max_scrolls=15
)

print(f"Data saved to: {output_file}")
print(f"Total: {success_count} records")
```

## 📁 Struktur Project

```
gmaps_scraper/
├── gmaps_scraper.py       # Main scraper (improved v18)
├── config.py              # Configuration management
├── utils.py               # Helper functions
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── VALIDATION_GUIDE.md    # 🆕 Data validation guide
├── QUICKSTART.md          # Quick start guide
├── IMPROVEMENTS.md        # v17 vs v18 comparison
├── scraper.log            # Log file (auto-generated)
└── results/               # Output folder (auto-generated)
    └── *.csv              # CSV results
```

## 🔧 Konfigurasi

Edit `config.py` untuk customize behavior:

```python
# Contoh: Ubah timeout
ScraperConfig.PAGE_LOAD_TIMEOUT = 60  # detik

# Contoh: Ubah max retries
ScraperConfig.MAX_RETRIES = 5

# Contoh: Enable headless di code
options = ScraperConfig.get_chrome_options()
# Uncomment baris headless di config.py
```

## 📊 Output Format

CSV file dengan kolom:

| Kolom | Deskripsi | Max Length |
|-------|-----------|------------|
| namaTravel | Nama bisnis | 256 chars |
| alamat | Alamat lengkap | 512 chars |
| kota | Nama kota (extracted) | 100 chars |
| telepon | Nomor telepon | 50 chars |
| deskripsi | Kategori bisnis | 512 chars |
| websiteUrl | URL website | 256 chars |
| logoUrl | URL logo/gambar | 256 chars |
| email | Email address (jika ditemukan) | 256 chars |
| mapUrl | Google Maps URL | 512 chars |

**🆕 Note:** Field otomatis di-truncate jika melebihi max length.

## 🎨 Email Detection Methods

1. **Mailto Links** - Paling akurat, cari tag `<a href="mailto:...">`
2. **Regex Pattern** - Scan page source dengan regex
3. **Visible Elements** - Scan footer, contact section, dll

## 🔍 Data Validation Modes

**🆕 Feature baru v18:** Filter data berdasarkan completeness

| Mode | Required Fields | Data Saved | Use Case |
|------|----------------|------------|----------|
| **STRICT** | All 9 fields | ~10-20% | Premium leads |
| **MODERATE** ⭐ | nama, website, email | ~20-30% | Email marketing |
| **LENIENT** | nama, telepon | ~80-90% | Cold calling |
| **NONE** | No filter | ~100% | Raw data |

📖 **Detailed guide:** Lihat `VALIDATION_GUIDE.md` untuk penjelasan lengkap.

## ⚙️ Advanced Features

### 1. Graceful Shutdown
Tekan `Ctrl+C` untuk stop dengan aman. Data yang sudah di-scrape akan tersimpan.

### 2. Logging
Check `scraper.log` untuk detailed logs:
```bash
tail -f scraper.log  # Monitor real-time
```

### 3. Custom Selectors
Edit `ScraperConfig.SELECTORS` di `config.py` jika Google Maps update struktur HTML.

## 🐛 Troubleshooting

### Chrome Driver Error
```bash
# Update Chrome ke versi terbaru
# atau install manual ChromeDriver
```

### Website Timeout
```python
# Increase timeout di config.py
ScraperConfig.EMAIL_PAGE_LOAD_TIMEOUT = 20  # detik
```

### Email Tidak Ditemukan
- Pastikan website punya contact page
- Beberapa website pakai JavaScript rendering (sulit di-scrape)
- Coba manual check di browser

### Encoding Issues di Excel
File sudah menggunakan UTF-8-sig, tapi jika masih ada masalah:
1. Buka CSV dengan Notepad
2. Save As → Encoding: UTF-8 with BOM

## 📈 Performance Tips

1. **Kurangi scroll** untuk hasil lebih cepat
2. **Enable headless** untuk save resources
3. **Adjust timeouts** di config.py sesuai koneksi internet
4. **Batch processing** - scrape di malam hari untuk koneksi lebih stabil

## 🔐 Best Practices

- ⚠️ Jangan scrape terlalu aggressive (respect rate limits)
- ⚠️ Gunakan data sesuai terms of service
- ⚠️ Pastikan Chrome sudah terupdate
- ⚠️ Check log file untuk troubleshooting

## 📝 Changelog

### v18 (2025-11-17) - Major Improvements
- ✅ Complete refactoring dengan modular architecture
- ✅ Added config.py untuk centralized configuration
- ✅ Added utils.py dengan helper functions
- ✅ Logging system dengan file output
- ✅ Retry mechanism dengan exponential backoff
- ✅ Progress tracking yang lebih informatif
- ✅ Better error handling dan validation
- ✅ Type hints untuk code quality
- ✅ Graceful shutdown handler
- ✅ Email validation yang lebih robust
- ✅ **🆕 Data validation dengan 4 modes** (STRICT/MODERATE/LENIENT/NONE)
- ✅ **🆕 Field length truncation** otomatis
- ✅ **🆕 Detailed statistics report** dengan skip reasons
- ✅ **🆕 Data quality control** untuk ensure lead quality

### v17 (Previous)
- Email hunter feature
- Basic error handling

## 🤝 Contributing

Improvements suggestions:
1. Fork repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

## 📄 License

Free to use for learning purposes. Commercial usage - please consult.

## 👨‍💻 Author

Improved Version - 2025
Original concept with major improvements

---

**Happy Scraping! 🎉**

Jika ada pertanyaan atau issues, check log file atau create an issue.

