<div align="center">

# 🗺️ GMAPS-LEAD-SCRAPER

<h3>Accelerate Lead Generation with Smarter Data Insights</h3>

<p>
    <a href="https://github.com/rotiawan/gmaps-scraper/commits/main">
        <img src="https://img.shields.io/github/last-commit/rotiawan/gmaps-scraper?style=flat-square&logo=git&logoColor=white&color=blue" alt="last commit">
    </a>
    <a href="https://github.com/rotiawan/gmaps-scraper/search?l=python">
        <img src="https://img.shields.io/github/languages/top/rotiawan/gmaps-scraper?style=flat-square&color=blue" alt="python percentage">
    </a>
    <a href="https://github.com/rotiawan/gmaps-scraper">
        <img src="https://img.shields.io/github/languages/count/rotiawan/gmaps-scraper?style=flat-square&color=blue" alt="languages">
    </a>
</p>

<h3>Built with the tools and technologies:</h3>

<p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white" alt="Selenium">
    <img src="https://img.shields.io/badge/WebDriver_Manager-FF6C37?style=for-the-badge&logo=google-chrome&logoColor=white" alt="WebDriver Manager">
</p>

</div>

---

## 📝 Deskripsi

**Google Maps Lead Scraper v18** adalah tool otomatis berbasis Python yang dirancang khusus untuk membantu tim **Business Development (Bisdev)**, sales, marketing, dan peneliti pasar mengumpulkan data prospek klien secara efisien dan terstruktur dari Google Maps.

Tool ini mampu mengekstrak informasi lengkap bisnis termasuk **email address** dari website yang ditemukan!

---

## 📜 Daftar Isi
- [Deskripsi](#-deskripsi)
- [Fitur Unggulan](#-fitur-unggulan)
- [Prasyarat](#-prasyarat)
- [Instalasi](#️-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [Output](#-output)
- [Tips & Best Practices](#-tips--best-practices)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Struktur Project](#-struktur-project)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#️-disclaimer)

---

## ✨ Fitur Unggulan

### Core Features
* **🚀 Otomatisasi Penuh**: Input keyword, script akan otomatis membuka browser, searching, dan scrolling hasil
* **📧 Email Extraction**: Mengunjungi website bisnis dan mengekstrak email menggunakan 3 metode:
  - Mencari `mailto:` links (paling akurat)
  - Pattern matching dengan regex di page source
  - Scanning visible text elements (footer, contact section)
* **🧠 Logika Scroll Cerdas**: Deteksi otomatis akhir halaman untuk efisiensi scraping
* **🎯 Multi-Selector Strategy**: Kombinasi selector untuk maksimalkan data yang terkumpul
* **📱 Phone & Website Parsing**: Deteksi berbagai format nomor telepon dan filter URL asli

### Data Quality & Validation
* **✅ 4 Validation Modes**:
  - **STRICT**: Semua field wajib (~10-20% data tersimpan)
  - **MODERATE**: Minimal nama + website + email (~20-30% data tersimpan) ⭐ RECOMMENDED
  - **LENIENT**: Minimal nama + telepon (~80-90% data tersimpan)
  - **NONE**: Simpan semua data tanpa filter (~100% data tersimpan)
* **🔄 Retry Mechanism**: Auto-retry dengan exponential backoff untuk handle error
* **📊 Progress Tracking**: Real-time progress bar dengan statistik detail

### Technical Features
* **🪵 Logging System**: Comprehensive logging ke console & file (`scraper.log`)
* **⚙️ Configuration Management**: Centralized config untuk easy customization
* **🛡️ Error Handling**: Graceful shutdown (Ctrl+C), auto cleanup resources
* **📂 Smart Output**: Penamaan file dinamis dengan timestamp, contoh: `travel_agent_jakarta_20251117.csv`
* **🔇 Headless Mode**: Opsi untuk run tanpa UI browser (background mode)

---

## 📋 Prasyarat

* Python 3.7+
* Google Chrome terinstall di komputermu.

---

## ⚙️ Instalasi

1.  **Clone repository ini:**
    ```bash
    git clone https://github.com/rotiawan/gmaps-scraper.git
    ```

2.  **Masuk ke direktori proyek:**
    ```bash
    cd gmaps-scraper
    cd gmaps_scraper
    ```

3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```
    
    **Library yang digunakan:**
    - `selenium` - Browser automation
    - `webdriver-manager` - Auto-download ChromeDriver
    
    > 💡 **Tip**: Gunakan virtual environment untuk isolasi dependencies:
    > ```bash
    > python -m venv venv
    > venv\Scripts\activate  # Windows
    > source venv/bin/activate  # Linux/Mac
    > ```

---

## 🚀 Cara Menjalankan

1.  **Masuk ke direktori gmaps_scraper:**
    ```bash
    cd gmaps_scraper
    ```

2.  **Jalankan script:**
    ```bash
    python gmaps_scraper.py
    ```

3.  **Ikuti prompt interaktif:**
    
    a. **Kata kunci pencarian**
    ```
    📍 Masukkan kata kunci pencarian (contoh: 'travel agent di Jakarta'):
    ```
    
    b. **Maksimal scroll** (default: 20)
    ```
    📜 Maksimal scroll (default: 20, Enter = default):
    ```
    
    c. **Pilih Validation Mode** (menentukan filter data yang akan disimpan)
    ```
    🔍 Pilih Data Validation Mode:
       1. STRICT   - Semua field wajib terisi (~10-20% data tersimpan)
       2. MODERATE - Minimal: nama, website, email (~20-30% data tersimpan) [RECOMMENDED]
       3. LENIENT  - Minimal: nama, telepon (~80-90% data tersimpan)
       4. NONE     - Simpan semua data tanpa filter (~100% data tersimpan)
    Pilih mode (1-4, default: 2):
    ```
    
    d. **Headless Mode** (opsional, untuk run tanpa UI browser)
    ```
    🔇 Jalankan headless mode? (y/n, default: n):
    ```

4.  **Proses scraping berjalan:**
    - Browser akan otomatis membuka dan mencari di Google Maps
    - Script akan scroll hasil pencarian
    - Setiap bisnis akan dikunjungi untuk ekstrak detail + email dari website
    - Progress bar real-time akan menampilkan status

⚠️ **CATATAN PENTING:**
- Proses akan **lebih lambat** karena mengunjungi setiap website untuk ekstrak email
- Waktu estimasi: ~3-5 detik per bisnis (tergantung kecepatan website target)
- Gunakan **Ctrl+C** untuk graceful shutdown (data akan tetap tersimpan)

---

## 📁 Output

Hasil scraping akan tersimpan dalam file **CSV** di folder `results/` dengan format:

```
gmaps_scraper/results/travel_agent_jakarta_20251117_142530.csv
```

### Kolom Data:
| Kolom | Deskripsi | Contoh |
|-------|-----------|--------|
| `namaTravel` | Nama bisnis | PT. Alam Indah Travel |
| `alamat` | Alamat lengkap | Jl. Sudirman No. 123, Jakarta |
| `kota` | Nama kota (auto-extract dari alamat) | Jakarta |
| `telepon` | Nomor telepon | +62 21 1234567 |
| `deskripsi` | Kategori/jenis bisnis | Travel agency |
| `websiteUrl` | URL website | https://example.com |
| `logoUrl` | URL logo/gambar bisnis | https://lh3.googleusercontent.com/... |
| `email` | Email (extracted dari website) | info@example.com |
| `mapUrl` | Link Google Maps | https://www.google.com/maps/place/... |

### Contoh Output:
```csv
namaTravel,alamat,kota,telepon,deskripsi,websiteUrl,logoUrl,email,mapUrl
"PT Travel Mandiri","Jl. Thamrin No.1, Jakarta Pusat","Jakarta","+62 21 12345678","Travel agency","https://travelmandiri.com","https://...","info@travelmandiri.com","https://maps.google.com/..."
```

### Statistik Akhir:
Setelah selesai, akan ditampilkan summary lengkap:
```
📊 ===== DATA STATISTICS =====
✅ Total Data Disimpan   : 25
📋 Total Data Diproses   : 100
⏭️  Total Data Di-skip    : 75

🔍 SKIP BREAKDOWN:
   • Missing email        : 45 (60.0%)
   • Missing website      : 20 (26.7%)
   • Missing name         : 10 (13.3%)
===============================
```

---

## 💡 Tips & Best Practices

### Untuk Hasil Maksimal:
1. **Gunakan keyword spesifik**: Tambahkan lokasi untuk hasil lebih relevan
   - ✅ `"travel umroh di Jakarta Selatan"`
   - ❌ `"travel"`

2. **Pilih validation mode sesuai kebutuhan**:
   - Butuh lead berkualitas tinggi dengan email? → **MODERATE**
   - Butuh banyak lead dengan telepon? → **LENIENT**
   - Research/analisis data lengkap? → **NONE**

3. **Max scroll recommendation**:
   - Quick test: `5-10` scroll
   - Normal usage: `20-30` scroll (~100-150 bisnis)
   - Comprehensive: `50+` scroll (bisa ratusan bisnis)

4. **Performance tips**:
   - Gunakan headless mode untuk scraping besar (lebih cepat)
   - Close aplikasi berat lainnya selama scraping
   - Pastikan koneksi internet stabil

---

## 🔧 Customization

Script ini sangat modular! Anda bisa customize di `config.py`:

```python
# Timeout settings
PAGE_LOAD_TIMEOUT = 30  # Timeout untuk load halaman
EMAIL_PAGE_LOAD_TIMEOUT = 10  # Timeout untuk scan email

# Scroll behavior
SCROLL_PAUSE_TIME = 2  # Delay antar scroll

# Validation rules
VALIDATION_RULES = {
    'STRICT': ['namaTravel', 'alamat', 'telepon', 'websiteUrl', 'email'],
    'MODERATE': ['namaTravel', 'websiteUrl', 'email'],
    'LENIENT': ['namaTravel', 'telepon'],
    'NONE': []
}
```

---

## 🐛 Troubleshooting

### Browser tidak terbuka
- Pastikan Chrome terinstall
- Update Chrome ke versi terbaru
- Coba hapus cache webdriver: `rm -rf ~/.wdm/` (Linux/Mac) atau `rmdir /s %USERPROFILE%\.wdm\` (Windows)

### Email tidak terdeteksi
- Website target mungkin tidak mencantumkan email
- Email dalam format gambar (tidak bisa di-scrape)
- Website terlalu lambat load (timeout)
- Solusi: Coba mode LENIENT untuk fokus ke telepon

### Script stuck/hang
- Tekan **Ctrl+C** untuk graceful shutdown
- Data yang sudah di-scrape tetap tersimpan
- Check `scraper.log` untuk detail error

### Data hasil sedikit
- Pilih validation mode lebih lenient (LENIENT atau NONE)
- Tingkatkan max scroll
- Keyword terlalu spesifik, coba lebih general

---

## 📊 Struktur Project

```
gmaps-scraper/
├── gmaps_scraper/
│   ├── gmaps_scraper.py    # Main script
│   ├── config.py           # Configuration & settings
│   ├── utils.py            # Helper functions & utilities
│   ├── requirements.txt    # Python dependencies
│   ├── results/            # Output CSV files
│   ├── scraper.log         # Log file (auto-generated)
│   ├── QUICKSTART.md       # Quick start guide
│   ├── IMPROVEMENTS.md     # Changelog & improvements
│   └── VALIDATION_GUIDE.md # Validation modes guide
└── README.md               # This file
```

---

## 🤝 Contributing

Contributions are welcome! Jika Anda menemukan bug atau punya ide fitur baru:

1. Fork repository ini
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

Project ini dibuat untuk keperluan edukasi dan bisnis development. Gunakan dengan bijak dan patuhi Terms of Service dari Google Maps.

---

## ⚠️ Disclaimer

* Tool ini dibuat untuk keperluan **research dan bisnis development** yang legitimate
* Pengguna bertanggung jawab penuh atas penggunaan tool ini
* Pastikan mematuhi **Google Maps Terms of Service** dan robots.txt website target
* Struktur HTML Google Maps dan website dapat berubah sewaktu-waktu
* Gunakan dengan rate limiting yang wajar untuk menghindari IP blocking
* **JANGAN** gunakan untuk spam, harassment, atau aktivitas ilegal

---

<div align="center">
