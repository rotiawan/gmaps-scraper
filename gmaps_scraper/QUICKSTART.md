# 🚀 Quick Start Guide - Google Maps Lead Scraper

## 📦 Installation

### Option 1: Install Dependencies Only (Recommended untuk pemula)

```bash
# 1. Clone repository
git clone https://github.com/rotiawan/gmaps-scraper.git
cd gmaps-scraper

# 2. Masuk ke folder gmaps_scraper
cd gmaps_scraper

# 3. Install dependencies
pip install -r requirements.txt
```

### Option 2: Install sebagai Package (Advanced)

```bash
# Clone dan install package
git clone https://github.com/rotiawan/gmaps-scraper.git
cd gmaps-scraper
pip install -e .
```

---

## 🏃 Running the Scraper

### Method 1: Direct Script Execution (Simple)

```bash
# Dari folder gmaps_scraper/
cd gmaps_scraper
python gmaps_scraper.py
```

### Method 2: As Python Module (Recommended)

```bash
# Dari root folder (Gmaps-Lead-Scraper/)
cd D:\magang\Gmaps-Lead-Scraper
python -m gmaps_scraper.gmaps_scraper
```

### Method 3: As Installed Package (Jika sudah install dengan pip)

```bash
# Dari mana saja
gmaps-scraper
```

---

## 📝 Penggunaan

### Interactive CLI

Setelah menjalankan script, ikuti prompt interaktif:

```
🗺️  GOOGLE MAPS LEAD SCRAPER - VERSION 18.0.0
======================================================================

📍 Masukkan kata kunci pencarian (contoh: 'travel agent di Jakarta'):
> travel umroh di Jakarta

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

🚀 Memulai scraping...
```

---

## 🐍 Programmatic Usage

Untuk menggunakan dalam Python script Anda sendiri:

```python
from gmaps_scraper import GoogleMapsScraper, ScraperConfig

# Configure validation mode
ScraperConfig.VALIDATION_MODE = 'MODERATE'

# Initialize scraper
scraper = GoogleMapsScraper(headless=True)

# Run scraping
output_file, count, stats = scraper.run(
    query="travel agent Jakarta",
    max_scrolls=20
)

# Print statistics
print(stats.get_summary())
print(f"Saved to: {output_file}")
```

---

## 🧪 Running Tests

```bash
# Install pytest (jika belum)
pip install pytest pytest-cov

# Run tests
cd gmaps_scraper
pytest test_utils.py -v

# Dengan coverage report
pytest test_utils.py --cov=. --cov-report=html
```

---

## 📁 Output Files

Results akan tersimpan di folder `results/`:

```
gmaps_scraper/results/
└── travel_agent_jakarta_20251122_143025.csv
```

Format CSV:
```csv
namaTravel,alamat,kota,telepon,deskripsi,websiteUrl,logoUrl,email,mapUrl
"PT Travel Mandiri","Jl. Thamrin No.1, Jakarta","Jakarta","+62211234567","Travel agency","https://example.com","https://...","info@example.com","https://maps.google.com/..."
```

---

## ⚙️ Configuration

### Custom Configuration

Edit `config.py` untuk customize settings:

```python
# Timeout settings
PAGE_LOAD_TIMEOUT = 300  # detik
EMAIL_PAGE_LOAD_TIMEOUT = 10  # detik

# Scroll behavior
SCROLL_PAUSE_TIME = 3  # detik
DEFAULT_MAX_SCROLLS = 15

# Validation mode (bisa diubah via CLI juga)
VALIDATION_MODE = 'MODERATE'
```

### Environment Variables (Optional)

Buat file `.env` untuk custom settings:

```bash
LOG_LEVEL=DEBUG
HEADLESS=true
MAX_SCROLLS=30
```

---

## 🔧 Troubleshooting

### Problem: ImportError: attempted relative import

**Solution:** Gunakan salah satu method di atas untuk running script.

```bash
# ✅ BENAR:
cd gmaps_scraper
python gmaps_scraper.py

# ✅ BENAR:
python -m gmaps_scraper.gmaps_scraper

# ❌ SALAH:
python D:\magang\Gmaps-Lead-Scraper\gmaps_scraper\gmaps_scraper.py
```

### Problem: Chrome driver not found

**Solution:** WebDriver Manager akan auto-download. Pastikan internet stabil.

```bash
# Manual install jika perlu
pip install --upgrade webdriver-manager
```

### Problem: Script hang/stuck

**Solution:** 
- Tekan `Ctrl+C` untuk graceful shutdown
- Data yang sudah di-scrape akan tetap tersimpan
- Check `scraper.log` untuk detail error

### Problem: No data saved

**Solution:**
- Pilih validation mode yang lebih lenient (LENIENT atau NONE)
- Tingkatkan `max_scrolls`
- Check koneksi internet
- Pastikan keyword tidak terlalu spesifik

---

## 📊 Tips untuk Hasil Maksimal

### 1. Keyword Strategy

```bash
# ✅ BAIK - Spesifik dengan lokasi
"travel umroh di Jakarta Selatan"
"hotel di Bali dekat pantai"
"restoran jepang di Surabaya"

# ❌ KURANG BAIK - Terlalu umum
"travel"
"hotel"
"restoran"
```

### 2. Validation Mode Selection

| Mode | Use Case | Expected Results |
|------|----------|------------------|
| **STRICT** | Need high-quality leads with complete info | 10-20% data |
| **MODERATE** | Need leads with email (RECOMMENDED) | 20-30% data |
| **LENIENT** | Need many leads with phone numbers | 80-90% data |
| **NONE** | Research/analysis, need all data | 100% data |

### 3. Max Scrolls Recommendation

| Purpose | Max Scrolls | Expected Results |
|---------|-------------|------------------|
| Quick test | 5-10 | 20-50 businesses |
| Normal usage | 20-30 | 100-150 businesses |
| Comprehensive | 50+ | 300+ businesses |

---

## 🎯 Example Workflows

### Example 1: Quick Test

```bash
cd gmaps_scraper
python gmaps_scraper.py

# Input:
# Query: travel agent Jakarta
# Scrolls: 5
# Mode: NONE (untuk test semua data)
# Headless: n
```

### Example 2: Production Scraping

```bash
python -m gmaps_scraper.gmaps_scraper

# Input:
# Query: hotel bintang 4 di Bali
# Scrolls: 30
# Mode: MODERATE (quality leads dengan email)
# Headless: y (faster)
```

### Example 3: Bulk Scraping (Python Script)

```python
from gmaps_scraper import GoogleMapsScraper, ScraperConfig

queries = [
    "travel umroh di Jakarta",
    "travel haji di Surabaya",
    "tour organizer di Bandung"
]

for query in queries:
    scraper = GoogleMapsScraper(headless=True)
    output, count, stats = scraper.run(query, max_scrolls=20)
    print(f"✅ {query}: {count} leads saved")
```

---

## 🆘 Need Help?

- **Documentation**: Read `REFACTORING_NOTES.md` untuk detail teknis
- **Issues**: Report bugs di [GitHub Issues](https://github.com/rotiawan/gmaps-scraper/issues)
- **Logs**: Check `scraper.log` untuk detailed error messages

---

**Happy Scraping! 🚀**
