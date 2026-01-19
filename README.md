<div align="center">

# 🗺️ GOOGLE MAPS LEAD SCRAPER

<h3>Tool Otomatis untuk Generate Lead Bisnis dari Google Maps</h3>

<p>
    <img src="https://img.shields.io/badge/Version-18.0.0-blue?style=for-the-badge" alt="version">
    <img src="https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge&logo=python" alt="python">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="license">
</p>

<p>
    <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white" alt="Selenium">
    <img src="https://img.shields.io/badge/Chrome-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Chrome">
</p>

</div>

---

## 📑 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Arsitektur & Struktur](#-arsitektur--struktur)
- [Cara Kerja](#-cara-kerja)
- [Fitur Unggulan](#-fitur-unggulan)
- [Prasyarat](#-prasyarat)
- [Instalasi](#%EF%B8%8F-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
  - [Mode Interaktif](#1-mode-interaktif)
  - [Mode Programmatic](#2-mode-programmatic-python-code)
- [Validation Modes](#-validation-modes)
- [Output Data](#-output-data)
- [Konfigurasi](#%EF%B8%8F-konfigurasi)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 Tentang Proyek

**Google Maps Lead Scraper v18** adalah tool profesional berbasis Python yang dirancang untuk tim **Business Development**, Sales, Marketing, dan Research untuk mengumpulkan data prospek bisnis secara otomatis dari Google Maps.

Tool ini tidak hanya mengekstrak informasi dasar (nama, alamat, telepon), tetapi juga **mengunjungi website bisnis** untuk mengekstrak **alamat email** menggunakan 3 metode cerdas.

### 🎯 Use Cases

- **Sales & Marketing**: Kumpulkan database prospek dengan email untuk cold email campaigns
- **Business Development**: Analisis kompetitor dan mapping pasar
- **Market Research**: Riset industri dan trend pasar lokal
- **B2B Lead Generation**: Generate qualified leads dengan filter kualitas data

### ⭐ Kenapa Pilih Tool Ini?

- ✅ **Modular & Professional**: Clean code dengan arsitektur yang solid
- ✅ **Email Extraction**: Ekstrak email otomatis dari website bisnis
- ✅ **Quality Control**: 4 mode validasi untuk kontrol kualitas data
- ✅ **Comprehensive Logging**: Track semua aktivitas untuk debugging
- ✅ **Error Handling**: Robust error handling dengan auto-retry
- ✅ **Statistics Report**: Laporan lengkap hasil scraping
- ✅ **Configurable**: Mudah di-customize sesuai kebutuhan

---

## 🏗️ Arsitektur & Struktur

### Struktur Project

```
Gmaps-Lead-Scraper/
│
├── README.md                    # Dokumentasi utama
├── setup.py                     # Package setup untuk instalasi
├── MANIFEST.in                  # Manifest file untuk packaging
│
└── gmaps_scraper/               # Package utama
    │
    ├── __init__.py              # Package initialization & exports
    ├── gmaps_scraper.py         # ⭐ Main scraper (GoogleMapsScraper class)
    ├── config.py                # ⚙️  Configuration management
    ├── constants.py             # 📋 Centralized constants
    ├── utils.py                 # 🛠️  Helper functions & utilities
    ├── exceptions.py            # ⚠️  Custom exception classes
    ├── test_utils.py            # 🧪 Unit tests untuk utils
    └── requirements.txt         # Python dependencies
```

### Penjelasan Setiap Modul

#### 1. `gmaps_scraper.py` - Main Scraper

**Kelas Utama:**

- **`GoogleMapsScraper`**: Class utama untuk scraping Google Maps
  - Setup WebDriver (Chrome)
  - Searching & scrolling hasil
  - Collecting business links
  - Scraping detail setiap bisnis
  - Export ke CSV dengan statistics

- **`EmailFinder`**: Class khusus untuk ekstrak email dari website
  - Metode 1: Mencari `mailto:` links
  - Metode 2: Regex pattern matching di page source
  - Metode 3: Scan visible elements (footer, contact section)

**Flow:**
```
Setup Driver → Search Query → Scroll Results → 
Collect Links → Scrape Details → Find Email → 
Validate Data → Save to CSV
```

#### 2. `config.py` - Configuration Management

**Class:** `ScraperConfig`

Centralized configuration dengan kategorisasi:
- **Selenium Settings**: Timeout, wait times
- **Scraping Settings**: Scroll behavior, delays
- **Email Finder Settings**: Email validation rules
- **Retry Settings**: Max retries, backoff factor
- **CSV Settings**: Headers, encoding
- **Data Validation Settings**: Validation modes & rules
- **XPath/CSS Selectors**: Selector strategy untuk scraping

**Key Methods:**
- `get_chrome_options()`: Generate Chrome options anti-detection
- `create_output_dir()`: Create folder output otomatis
- `validate_config()`: Validasi config saat startup
- `get_validation_modes_info()`: Info lengkap validation modes

#### 3. `constants.py` - Constants Module

Menghindari magic numbers/strings di codebase dengan define:
- URL constants (Google Maps URL)
- Timeout & delay constants
- Validation mode constants
- Email validation constants
- Regex patterns (email, phone, filename)
- CSV headers & field length limits
- Logging constants
- Error & success messages

**Best Practice:** Semua hardcoded values ada di sini untuk easy maintenance.

#### 4. `utils.py` - Utility Functions

**Decorator Functions:**
- `retry_on_failure()`: Retry mechanism dengan exponential backoff

**Selenium Helpers:**
- `safe_find_element()`: Safely find element dengan default value
- `close_extra_tabs()`: Cleanup browser tabs
- `scroll_element()`: Smart scrolling dengan end detection

**Data Validation:**
- `validate_email()`: Validasi email dengan regex & business rules
- `extract_email_from_text()`: Extract email dari text/HTML
- `validate_data()`: Validasi data berdasarkan mode

**Data Transformation:**
- `truncate_fields()`: Truncate field yang terlalu panjang
- `extract_city_from_address()`: Extract nama kota dari alamat
- `format_phone_number()`: Clean & format nomor telepon
- `sanitize_filename()`: Sanitize text untuk filename

**Progress Tracking Classes:**
- `ProgressTracker`: Track progress scraping dengan logging
- `DataStatistics`: Collect statistics & generate report

#### 5. `exceptions.py` - Custom Exceptions

Custom exception classes untuk better error handling:
- `ScraperBaseException`: Base exception untuk semua custom exceptions
- `WebDriverSetupError`: Error saat setup WebDriver
- `SearchError`: Error saat searching di Google Maps
- `NoResultsFoundError`: Tidak ada hasil ditemukan
- `ScrapeError`: Error saat scraping data
- `EmailExtractionError`: Error saat extract email
- `ValidationError`: Error validasi data
- `ConfigurationError`: Error konfigurasi
- `FileOperationError`: Error operasi file
- `TimeoutError`: Timeout operations
- `InvalidInputError`: Invalid user input

**Decorator:** `handle_scraper_exception()` untuk graceful error handling.

---

## 🔄 Cara Kerja

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    1. INITIALIZATION                            │
│  • Setup Chrome WebDriver dengan anti-detection                 │
│  • Load konfigurasi dari config.py                              │
│  • Setup logging system                                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    2. SEARCH & SCROLL                           │
│  • Buka Google Maps                                              │
│  • Input search query                                            │
│  • Scroll hasil untuk load lebih banyak bisnis                   │
│  • Detect "end of list" untuk stop scroll                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    3. COLLECT LINKS                             │
│  • Find semua link bisnis dari feed                              │
│  • Deduplicate links                                             │
│  • Log total unique links found                                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    4. SCRAPE DETAILS                            │
│  UNTUK SETIAP BISNIS:                                            │
│    a. Buka detail page                                           │
│    b. Extract: nama, alamat, telepon, kategori, website, logo    │
│    c. Extract kota dari alamat                                   │
│    d. Format & clean data                                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    5. EMAIL EXTRACTION                          │
│  JIKA WEBSITE DITEMUKAN:                                         │
│    → Buka website di new tab                                     │
│    → Metode 1: Cari mailto: links                                │
│    → Metode 2: Regex scan di page source                         │
│    → Metode 3: Scan visible elements (footer, contact)           │
│    → Validate email (blacklist, format, length)                  │
│    → Return first valid email                                    │
│    → Close tab & kembali ke Google Maps                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    6. DATA VALIDATION                           │
│  • Check required fields berdasarkan validation mode             │
│  • Truncate fields yang terlalu panjang                          │
│  • Track skip reasons jika data tidak valid                      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    7. SAVE TO CSV                               │
│  • Save valid data ke CSV (UTF-8-sig untuk Excel)                │
│  • Flush setiap N rows untuk prevent data loss                   │
│  • Track statistics (saved, skipped, reasons)                    │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    8. GENERATE REPORT                           │
│  • Print summary statistics                                      │
│  • Show success rate                                             │
│  • Breakdown skip reasons                                        │
│  • Log output file location                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Email Extraction Strategy

Tool ini menggunakan **3 metode bertingkat** untuk maximize success rate:

```python
# METODE 1: Mailto Links (Most Accurate - ~60% success)
<a href="mailto:info@company.com">Email Us</a>

# METODE 2: Regex Pattern Matching (~25% success)
# Scan entire page source untuk email pattern
Contact: sales@company.co.id

# METODE 3: Visible Elements Scanning (~15% success)
# Cari di footer, contact section, dll
<div class="footer">
    <p>Email: support@company.com</p>
</div>
```

**Validasi Email:**
- ✅ Min/max length check (5-256 chars)
- ✅ RFC 5322 regex validation
- ✅ Blacklist domain check (example.com, test.com, dll)
- ✅ Image extension filter (.jpg, .png di URL false positive)

---

## ✨ Fitur Unggulan

### Core Features

| Fitur | Deskripsi |
|-------|-----------|
| 🚀 **Automated Scraping** | Full automation dari search sampai export CSV |
| 📧 **Email Extraction** | 3 metode ekstrak email dari website bisnis |
| 🧠 **Smart Scrolling** | Auto-detect end of list untuk efisiensi |
| 🎯 **Multi-Selector Strategy** | Kombinasi XPath & CSS selector untuk maksimal data |
| 📱 **Phone & Website Parsing** | Format & clean nomor telepon, filter URL asli |
| 🔄 **Auto Retry** | Exponential backoff retry untuk handle error |

### Data Quality & Validation

| Mode | Required Fields | Data Tersimpan | Use Case |
|------|----------------|----------------|----------|
| **STRICT** | Semua 9 field wajib | ~10-20% | Premium leads dengan data lengkap |
| **MODERATE** ⭐ | Nama + Website + Email | ~20-30% | Email marketing campaigns |
| **LENIENT** | Nama + Telepon | ~80-90% | Cold calling, telemarketing |
| **NONE** | Tidak ada filter | ~100% | Raw data, research purposes |

### Technical Features

- **🪵 Comprehensive Logging**: Console + file logging (`scraper.log`)
- **⚙️ Configuration Management**: Centralized config di `config.py`
- **🛡️ Error Handling**: Custom exceptions & graceful shutdown (Ctrl+C)
- **📂 Smart Output**: Filename dinamis dengan timestamp
- **🔇 Headless Mode**: Run tanpa UI browser (background mode)
- **📊 Statistics Report**: Detailed report dengan skip reasons breakdown
- **🔧 Highly Configurable**: Semua settings bisa di-customize
- **🧪 Type Hints**: Full type hints untuk code quality
- **📝 Comprehensive Docs**: Docstrings lengkap di setiap function

---

## 📋 Prasyarat

### System Requirements

- **Python**: 3.7 atau lebih tinggi
- **Google Chrome**: Versi terbaru (auto-updated driver via webdriver-manager)
- **OS**: Windows, macOS, atau Linux
- **RAM**: Minimal 4GB (Recommended: 8GB+)
- **Internet**: Koneksi stabil untuk scraping

### Python Dependencies

```
selenium>=4.0.0
webdriver-manager>=3.8.0
```

---

## ⚙️ Instalasi

### Metode 1: Quick Start (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/rotiawan/gmaps-scraper.git

# 2. Masuk ke direktori project
cd gmaps-scraper

# 3. Install dependencies
pip install -r gmaps_scraper/requirements.txt

# 4. Test run
cd gmaps_scraper
python gmaps_scraper.py
```

### Metode 2: Virtual Environment (Best Practice)

```bash
# 1. Clone repository
git clone https://github.com/rotiawan/gmaps-scraper.git
cd gmaps-scraper

# 2. Buat virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r gmaps_scraper/requirements.txt

# 5. Test run
cd gmaps_scraper
python gmaps_scraper.py
```

### Metode 3: Install as Package

```bash
# Install sebagai Python package (editable mode)
pip install -e .

# Sekarang bisa import dari mana saja
python
>>> from gmaps_scraper import GoogleMapsScraper
>>> scraper = GoogleMapsScraper()
```

### Verify Installation

```bash
# Check Python version
python --version  # Should be 3.7+

# Check Chrome installation
# Windows:
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
# macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
# Linux:
google-chrome --version

# Test import
python -c "from gmaps_scraper import GoogleMapsScraper; print('✅ Installation OK')"
```

---

## 🚀 Cara Penggunaan

### 1. Mode Interaktif

Mode paling mudah untuk user non-technical:

```bash
cd gmaps_scraper
python gmaps_scraper.py
```

**Follow Interactive Prompts:**

```
🗺️  ===== GOOGLE MAPS LEAD SCRAPER v18 =====

📍 Masukkan kata kunci pencarian (contoh: 'travel agent di Jakarta'): 
> travel umrah di Bandung

📜 Maksimal scroll (default: 15, Enter = default): 
> 20

🔍 Pilih Data Validation Mode:
   1. STRICT   - Semua field wajib terisi (~10-20% data tersimpan)
   2. MODERATE - Minimal: nama, website, email (~20-30% data tersimpan) [RECOMMENDED]
   3. LENIENT  - Minimal: nama, telepon (~80-90% data tersimpan)
   4. NONE     - Simpan semua data tanpa filter (~100% data tersimpan)

Pilih mode (1-4, default: 2): 
> 2

🔇 Jalankan headless mode? (y/n, default: n): 
> n

⚙️  CONFIGURATION SUMMARY
======================================================================
Max Scrolls       : 20
Validation Mode   : MODERATE
Max Retries       : 3
Output Directory  : results
Log Level         : INFO
======================================================================

✅ WebDriver berhasil di-setup
🔍 Searching for: travel umrah di Bandung
📜 Memulai scrolling untuk mengumpulkan link...
...
```

### 2. Mode Programmatic (Python Code)

Untuk integrasi ke script Python Anda:

#### Basic Usage

```python
from gmaps_scraper import GoogleMapsScraper

# Initialize scraper
scraper = GoogleMapsScraper(headless=False)

# Run scraping
output_file, total_saved = scraper.run(
    query="travel agent di Jakarta",
    max_scrolls=20,
    validation_mode="MODERATE"
)

print(f"✅ Data tersimpan: {total_saved} bisnis")
print(f"📁 File output: {output_file}")
```

#### Advanced Usage dengan Custom Config

```python
from gmaps_scraper import GoogleMapsScraper, ScraperConfig

# Customize config
ScraperConfig.PAGE_LOAD_TIMEOUT = 60
ScraperConfig.MAX_RETRIES = 5
ScraperConfig.VALIDATION_MODE = "LENIENT"

# Initialize scraper dengan headless mode
scraper = GoogleMapsScraper(headless=True)

# Run multiple queries
queries = [
    "travel umrah di Jakarta",
    "travel umrah di Bandung",
    "travel umrah di Surabaya"
]

for query in queries:
    try:
        output_file, total_saved = scraper.run(query, max_scrolls=30)
        print(f"✅ {query}: {total_saved} leads → {output_file}")
    except Exception as e:
        print(f"❌ {query}: Error - {e}")
    finally:
        scraper.cleanup()
```

#### Email Extraction Standalone

```python
from gmaps_scraper import EmailFinder

# Initialize email finder
email_finder = EmailFinder(driver)  # driver = selenium webdriver

# Find email dari website
email = email_finder.find_email_from_website("https://company.com")

if email:
    print(f"✅ Email found: {email}")
else:
    print("❌ Email tidak ditemukan")
```

#### Utility Functions

```python
from gmaps_scraper import validate_email, extract_email_from_text

# Validate email
is_valid = validate_email("info@company.com")
print(f"Email valid: {is_valid}")

# Extract email from text
text = "Contact us at sales@company.co.id or call 021-1234567"
email = extract_email_from_text(text)
print(f"Email extracted: {email}")
```

### 3. Command Line (Jika Install as Package)

```bash
# Setelah install dengan: pip install -e .
gmaps-scraper
```

---

## 🔍 Validation Modes

Validation modes menentukan **filter kualitas data** yang akan disimpan ke CSV.

### Comparison Table

| Mode | Required Fields | Saved | Skipped | Success Rate | Best For |
|------|----------------|-------|---------|--------------|----------|
| **STRICT** | Nama, Alamat, Kota, Telepon, Deskripsi, Website, Logo, Email, Map URL | 10-15 | 85-90 | ~12% | Premium qualified leads |
| **MODERATE** ⭐ | Nama, Website, Email | 20-30 | 70-80 | ~25% | Email marketing campaigns |
| **LENIENT** | Nama, Telepon | 80-90 | 10-20 | ~85% | Cold calling, telemarketing |
| **NONE** | Tidak ada filter | 100 | 0 | 100% | Raw data collection, research |

### Kapan Menggunakan Mode Apa?

#### 🎯 STRICT Mode
**Use Case:**
- Butuh lead dengan data **super lengkap**
- Sales cycle panjang yang butuh research mendalam
- B2B enterprise sales

**Expected Result:**
```
Input:  100 bisnis di-scrape
Output: ~12 bisnis tersimpan
Data:   Semua field lengkap, siap untuk immediate action
```

#### ⭐ MODERATE Mode (RECOMMENDED)
**Use Case:**
- **Email marketing campaigns**
- Lead generation untuk outbound email
- Balance antara kualitas dan kuantitas

**Expected Result:**
```
Input:  100 bisnis di-scrape
Output: ~25 bisnis tersimpan
Data:   Nama + Website + Email (cukup untuk cold email)
```

#### 📞 LENIENT Mode
**Use Case:**
- **Cold calling campaigns**
- Telemarketing
- Butuh banyak kontak cepat

**Expected Result:**
```
Input:  100 bisnis di-scrape
Output: ~85 bisnis tersimpan
Data:   Nama + Telepon (cukup untuk phone outreach)
```

#### 📊 NONE Mode
**Use Case:**
- Market research & analysis
- Mapping industri
- Data collection untuk analisis statistik

**Expected Result:**
```
Input:  100 bisnis di-scrape
Output: 100 bisnis tersimpan
Data:   Semua data apa adanya (beberapa field bisa kosong)
```

### Customize Validation Rules

Edit di `config.py`:

```python
# Tambah custom mode
VALIDATION_RULES = {
    'CUSTOM': ['namaTravel', 'email'],  # Hanya nama & email
    'STRICT': [...],
    'MODERATE': [...],
    # ...
}
```

---

## 📁 Output Data

### File Format

Hasil scraping disimpan dalam **CSV** di folder `results/` dengan naming format:

```
results/travel_umrah_di_bandung_20251127_143052.csv
        └────────┬────────┘         └──────┬──────┘
           Query sanitized         Timestamp
```

### CSV Structure

| Kolom | Tipe | Max Length | Deskripsi | Contoh |
|-------|------|------------|-----------|--------|
| `namaTravel` | String | 256 | Nama bisnis | "PT Alam Indah Travel" |
| `alamat` | String | 512 | Alamat lengkap | "Jl. Sudirman No.123, Jakarta Pusat, DKI Jakarta 10110" |
| `kota` | String | 100 | Nama kota (auto-extracted) | "Jakarta Pusat" |
| `telepon` | String | 50 | Nomor telepon | "+62 21 1234567" |
| `deskripsi` | String | 512 | Kategori/jenis bisnis | "Travel agency, Tour operator" |
| `websiteUrl` | String | 256 | URL website | "https://alamindah.com" |
| `logoUrl` | String | 256 | URL logo/gambar bisnis | "https://lh3.googleusercontent.com/..." |
| `email` | String | 256 | Email address | "info@alamindah.com" |
| `mapUrl` | String | 512 | Google Maps link | "https://www.google.com/maps/place/..." |

### Sample Output

```csv
namaTravel,alamat,kota,telepon,deskripsi,websiteUrl,logoUrl,email,mapUrl
"PT Alam Indah Travel","Jl. Sudirman No.123, Jakarta Pusat, DKI Jakarta","Jakarta Pusat","+62 21 1234567","Travel agency","https://alamindah.com","https://lh3.googleusercontent.com/...","info@alamindah.com","https://maps.google.com/..."
"Mandiri Tour & Travel","Jl. Asia Afrika No.45, Bandung, Jawa Barat","Bandung","022-87654321","Tour operator","https://mandiritour.co.id","https://lh3.googleusercontent.com/...","sales@mandiritour.co.id","https://maps.google.com/..."
```

### Statistics Report

Setelah scraping selesai, akan ditampilkan summary:

```
╔══════════════════════════════════════════════════════════╗
║           📊 STATISTIK SCRAPING RESULTS                  ║
╠══════════════════════════════════════════════════════════╣
║  Total Diproses    :  100 bisnis                         ║
║  ✅ Tersimpan      :   28 bisnis ( 28.0%)                ║
║  ❌ Dilewati       :   72 bisnis ( 72.0%)                ║
╠══════════════════════════════════════════════════════════╣
║  📋 Alasan Dilewati:                                     ║
║     • Missing: email                         :  45       ║
║     • Missing: websiteUrl                    :  20       ║
║     • Missing: namaTravel                    :   7       ║
╚══════════════════════════════════════════════════════════╝

✅ Data berhasil disimpan ke: results/travel_umrah_di_bandung_20251127_143052.csv
```

### Open di Excel

File menggunakan **UTF-8-sig** encoding (UTF-8 with BOM) untuk Excel compatibility.

**Windows:**
- Double-click file CSV → otomatis buka di Excel dengan encoding benar

**Mac/Linux:**
1. Buka Excel
2. File → Import → CSV
3. Pilih delimiter: Comma
4. Encoding: UTF-8

---

## 🔧 Konfigurasi

### Edit Configuration

Semua settings ada di `gmaps_scraper/config.py`:

```python
class ScraperConfig:
    # ===== TIMEOUT SETTINGS =====
    PAGE_LOAD_TIMEOUT = 300        # Timeout page load (detik)
    IMPLICIT_WAIT = 10             # Implicit wait untuk find element
    EXPLICIT_WAIT = 20             # Explicit wait untuk WebDriverWait
    EMAIL_PAGE_LOAD_TIMEOUT = 10   # Timeout scan email di website
    
    # ===== SCRAPING BEHAVIOR =====
    DEFAULT_MAX_SCROLLS = 15       # Default jumlah scroll
    SCROLL_PAUSE_TIME = 3.0        # Delay antar scroll (detik)
    AFTER_SEARCH_DELAY = 5.0       # Delay setelah search (detik)
    DETAIL_PAGE_DELAY = 3.0        # Delay di detail page (detik)
    
    # ===== RETRY SETTINGS =====
    MAX_RETRIES = 3                # Max percobaan ulang
    RETRY_DELAY = 2                # Base delay untuk retry (detik)
    BACKOFF_FACTOR = 2             # Exponential backoff factor
    
    # ===== VALIDATION MODE =====
    VALIDATION_MODE = "MODERATE"   # Default validation mode
    
    # ===== EMAIL VALIDATION =====
    EMAIL_MIN_LENGTH = 5
    EMAIL_MAX_LENGTH = 256
    EMAIL_BLACKLIST = (
        'example.com',
        'domain.com',
        'test.com',
        # ... tambah domain blacklist
    )
```

### Customize Chrome Options

```python
@classmethod
def get_chrome_options(cls, headless: bool = False):
    options = Options()
    
    # Custom user agent
    options.add_argument(f"user-agent={cls.USER_AGENT}")
    
    # Window settings
    options.add_argument('--start-maximized')
    # options.add_argument('--window-size=1920,1080')  # Custom size
    
    # Performance optimization
    # options.add_argument('--disable-images')  # Nonaktifkan gambar
    # options.add_argument('--disable-javascript')  # Nonaktifkan JS (HATI-HATI!)
    
    # Headless mode
    if headless:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
    
    return options
```

### Environment Variables (Advanced)

Buat file `.env` untuk sensitive config:

```bash
# .env
GMAPS_MAX_SCROLLS=20
GMAPS_VALIDATION_MODE=MODERATE
GMAPS_HEADLESS=false
```

Load di code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

ScraperConfig.DEFAULT_MAX_SCROLLS = int(os.getenv('GMAPS_MAX_SCROLLS', 15))
ScraperConfig.VALIDATION_MODE = os.getenv('GMAPS_VALIDATION_MODE', 'MODERATE')
```

---

## 🐛 Troubleshooting

### 1. Browser Tidak Terbuka

**Gejala:**
```
❌ ERROR: Gagal setup WebDriver
```

**Solusi:**
```bash
# Update Chrome ke versi terbaru
# Windows: Settings → About Chrome → Update
# Mac: Chrome → About Google Chrome → Update

# Clear webdriver cache
rm -rf ~/.wdm/  # Mac/Linux
rmdir /s %USERPROFILE%\.wdm\  # Windows

# Reinstall webdriver-manager
pip install --upgrade webdriver-manager
```

### 2. Email Tidak Ditemukan

**Gejala:**
```
⚠️  Email tidak ditemukan di website
```

**Possible Reasons:**
- Website tidak mencantumkan email
- Email dalam format gambar (tidak bisa di-scrape)
- Website terlalu lambat (timeout)
- Website memerlukan JavaScript rendering kompleks

**Solusi:**
```python
# Increase timeout di config.py
ScraperConfig.EMAIL_PAGE_LOAD_TIMEOUT = 20

# Atau gunakan mode LENIENT untuk fokus ke telepon
validation_mode = "LENIENT"
```

### 3. Script Stuck/Hang

**Gejala:**
- Script tidak progress
- Progress bar berhenti

**Solusi:**
```bash
# Tekan Ctrl+C untuk graceful shutdown
# Data yang sudah di-scrape akan tetap tersimpan

# Check log file untuk detail
tail -f gmaps_scraper/scraper.log
```

### 4. Data Hasil Sedikit

**Gejala:**
```
100 bisnis diproses, hanya 5 tersimpan
```

**Solusi:**
- **Pilih validation mode lebih lenient**
  ```python
  validation_mode = "LENIENT"  # atau "NONE"
  ```

- **Increase max scrolls**
  ```python
  max_scrolls = 50  # Lebih banyak bisnis
  ```

- **Cek skip reasons di statistics report**
  ```
  Missing: email → 70 bisnis
  → Solusi: Gunakan mode LENIENT (tidak butuh email)
  ```

### 5. Encoding Issues di Excel

**Gejala:**
- Karakter Indonesia (ă, é, ü) jadi aneh
- Contoh: "CafĂŠ" instead of "Café"

**Solusi:**
```bash
# File sudah UTF-8-sig, tapi jika masih ada masalah:

# Method 1: Buka dengan Excel Import Wizard
# File → Import → Text File → Pilih "UTF-8"

# Method 2: Convert encoding
iconv -f UTF-8 -t UTF-8 input.csv > output.csv
```

### 6. TimeoutException

**Gejala:**
```
selenium.common.exceptions.TimeoutException
```

**Solusi:**
```python
# Increase timeout di config.py
ScraperConfig.PAGE_LOAD_TIMEOUT = 60
ScraperConfig.EXPLICIT_WAIT = 30

# Atau gunakan headless mode (lebih cepat)
scraper = GoogleMapsScraper(headless=True)
```

### 7. XPath/Selector Tidak Ditemukan

**Gejala:**
```
NoSuchElementException: Element not found
```

**Reason:**
- Google Maps update struktur HTML

**Solusi:**
```python
# Update selector di config.py → SELECTORS dict
# Inspect element di Google Maps untuk XPath baru
# Atau report issue di GitHub
```

---

## 💡 Best Practices

### 1. Keyword Optimization

**❌ BAD:**
```python
query = "travel"  # Terlalu general
```

**✅ GOOD:**
```python
query = "travel umrah di Jakarta Selatan"  # Spesifik dengan lokasi
query = "restaurant chinese food di Bandung"
query = "hotel bintang 3 di Bali"
```

### 2. Rate Limiting

**❌ BAD:**
```python
# Scrape 1000 bisnis sekaligus
max_scrolls = 200  # Aggressive!
```

**✅ GOOD:**
```python
# Batch processing dengan delay
queries = ["travel di Jakarta", "travel di Bandung", ...]

for query in queries:
    scraper.run(query, max_scrolls=20)
    time.sleep(60)  # Delay 1 menit antar query
```

### 3. Data Quality vs Quantity

**Tips:**
- Untuk **cold email**: Gunakan `MODERATE` mode
- Untuk **cold calling**: Gunakan `LENIENT` mode
- Untuk **research**: Gunakan `NONE` mode lalu filter manual di Excel

### 4. Error Handling

**❌ BAD:**
```python
scraper.run(query, max_scrolls=20)  # No error handling
```

**✅ GOOD:**
```python
try:
    output_file, total = scraper.run(query, max_scrolls=20)
    print(f"✅ Success: {total} leads")
except Exception as e:
    logger.error(f"❌ Failed: {e}")
finally:
    scraper.cleanup()  # Always cleanup
```

### 5. Logging & Monitoring

```python
# Monitor log file real-time
# Terminal 1: Run scraper
python gmaps_scraper.py

# Terminal 2: Monitor log
tail -f scraper.log | grep "ERROR\|WARNING"
```

### 6. Resource Management

```python
# Use context manager untuk auto cleanup
with GoogleMapsScraper(headless=True) as scraper:
    scraper.run(query, max_scrolls=20)
# Auto cleanup saat selesai
```

### 7. Performance Optimization

**Tips untuk scraping lebih cepat:**
- ✅ Gunakan **headless mode**
- ✅ **Kurangi scroll** jika butuh cepat
- ✅ **Increase timeout** jika koneksi lambat
- ✅ **Close aplikasi berat** lainnya
- ✅ Scrape di **malam hari** (koneksi lebih stabil)

---

## 🔬 Technical Details

### Technology Stack

- **Python 3.7+**: Core language
- **Selenium 4.x**: Browser automation
- **ChromeDriver**: WebDriver untuk Chrome
- **webdriver-manager**: Auto-download & manage ChromeDriver

### Design Patterns

1. **Singleton Pattern**: `ScraperConfig` class
2. **Factory Pattern**: `get_chrome_options()` method
3. **Decorator Pattern**: `@retry_on_failure` decorator
4. **Strategy Pattern**: Multiple email extraction methods
5. **Template Method Pattern**: `GoogleMapsScraper.run()` flow

### Code Quality

- ✅ **PEP 8 Compliant**: Follow Python style guide
- ✅ **Type Hints**: Full type annotations untuk IDE support
- ✅ **Docstrings**: Comprehensive documentation di setiap function
- ✅ **SOLID Principles**: Clean architecture
- ✅ **DRY**: No code duplication
- ✅ **Error Handling**: Custom exceptions & graceful degradation

### Performance Metrics

**Typical Performance** (tested on mid-range laptop):

| Metric | Value |
|--------|-------|
| Search & Scroll (20x) | ~30-40 detik |
| Scrape per bisnis (tanpa email) | ~2 detik |
| Scrape per bisnis (dengan email) | ~5-7 detik |
| Total untuk 100 bisnis | ~8-12 menit |

**Bottleneck:**
- Email extraction (mengunjungi website external)
- Website loading time (varies by target)

**Optimization:**
- Gunakan headless mode: **~20% faster**
- Skip email extraction: **~60% faster**

### Security & Privacy

- ✅ **No credentials stored**: Tidak simpan password/API key
- ✅ **User agent rotation**: Appear as normal browser
- ✅ **Rate limiting**: Respect Google's ToS
- ⚠️  **Responsible scraping**: Jangan abuse tool ini

---

## 🤝 Contributing

Kontribusi sangat welcome! Berikut cara contribute:

### Setup Development Environment

```bash
# Fork & clone repository
git clone https://github.com/YOUR_USERNAME/gmaps-scraper.git
cd gmaps-scraper

# Create feature branch
git checkout -b feature/amazing-feature

# Install development dependencies
pip install -r gmaps_scraper/requirements.txt
pip install pytest pytest-cov black flake8

# Make your changes...

# Run tests
pytest gmaps_scraper/test_utils.py

# Format code
black gmaps_scraper/

# Check linting
flake8 gmaps_scraper/

# Commit & push
git add .
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Create Pull Request di GitHub
```

### Areas for Contribution

- 🐛 **Bug fixes**: Report atau fix bugs
- ✨ **New features**: Email filter, proxy support, dll
- 📝 **Documentation**: Improve docs, add tutorials
- 🧪 **Tests**: Add unit tests & integration tests
- 🌍 **Localization**: Translate to other languages
- ⚡ **Performance**: Optimization & speed improvements

---

## 📄 License

Project ini dilisensikan under **MIT License**.

```
MIT License

Copyright (c) 2025 rotiawan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[... full MIT license text ...]
```

**Disclaimer:**
- Tool ini untuk **educational & research purposes**
- Pengguna **bertanggung jawab penuh** atas penggunaan
- **Patuhi Terms of Service** Google Maps
- **Jangan gunakan** untuk spam atau aktivitas ilegal

---

## ⚠️ Important Notes

### Legal & Ethical Use

- ✅ **DO**: Gunakan untuk legitimate business development
- ✅ **DO**: Respect rate limits dan robots.txt
- ✅ **DO**: Verify data sebelum digunakan
- ❌ **DON'T**: Spam atau harassment
- ❌ **DON'T**: Scrape excessively (DDoS-like behavior)
- ❌ **DON'T**: Sell data tanpa verifikasi

### Google Maps Terms of Service

Tool ini melakukan web scraping yang **may or may not** violate Google Maps ToS. Gunakan dengan **bijak dan bertanggung jawab**.

### Rate Limiting Recommendation

```python
# Recommended: Max 100 bisnis per query, max 5 queries per jam
queries = ["travel di Jakarta", "travel di Bandung"]

for query in queries:
    scraper.run(query, max_scrolls=20)  # ~100 bisnis
    time.sleep(3600)  # Wait 1 jam
```

---

## 📞 Support & Contact

### Butuh Bantuan?

1. **Dokumentasi**: Baca README ini dengan teliti
2. **Log File**: Check `scraper.log` untuk error details
3. **GitHub Issues**: [Report bugs atau request features](https://github.com/rotiawan/gmaps-scraper/issues)
4. **Email**: your.email@example.com (update dengan email asli)

### Changelog

**Version 18.0.0** (2025-11-22)
- ✅ Complete refactoring dengan modular architecture
- ✅ Added configuration management (`config.py`)
- ✅ Added centralized constants (`constants.py`)
- ✅ Added custom exceptions (`exceptions.py`)
- ✅ Added comprehensive utility functions (`utils.py`)
- ✅ Logging system dengan file output
- ✅ Retry mechanism dengan exponential backoff
- ✅ Progress tracking & statistics report
- ✅ Data validation dengan 4 modes
- ✅ Field length truncation
- ✅ Type hints & docstrings lengkap
- ✅ Graceful shutdown handler (Ctrl+C)

**Previous Versions:**
- v17: Email extraction feature
- v16: Basic scraping functionality

---

<div align="center">

### ⭐ Jika project ini membantu, berikan star di GitHub! ⭐

**Built with ❤️ for Business Development Teams**

[⬆ Back to Top](#-google-maps-lead-scraper)

</div>
