# ⚡ Quick Start Guide

## 🎯 Install & Run dalam 3 Menit

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run Scraper
```bash
python gmaps_scraper.py
```

### 3️⃣ Input Data
```
📍 Masukkan kata kunci: travel agent di Jakarta
📜 Maksimal scroll: 15 (atau Enter untuk default)
🔇 Headless mode: n (atau Enter untuk default)
```

### 4️⃣ Lihat Hasil
```
📁 File tersimpan di: results/travel_agent_di_jakarta_20251117_143022.csv
```

---

## 🎮 Contoh Penggunaan

### Contoh 1: Basic Search
```
Input: hotel di Bali
Max scroll: 10
Output: ~100-150 data hotel
```

### Contoh 2: Specific Location
```
Input: restoran di Bandung
Max scroll: 20
Output: ~200-300 data restoran
```

### Contoh 3: Niche Business
```
Input: coworking space Jakarta Selatan
Max scroll: 5
Output: ~50-75 data coworking
```

---

## 📊 Expected Results

| Scroll | Estimated Data | Time Required |
|--------|---------------|---------------|
| 5      | ~50 items     | ~5 menit      |
| 10     | ~100 items    | ~10 menit     |
| 15     | ~150 items    | ~15 menit     |
| 20     | ~200 items    | ~20 menit     |

*Waktu bervariasi tergantung koneksi internet dan website speed*

---

## 🔧 Troubleshooting Cepat

### ❌ Error: ChromeDriver not found
```bash
# Install ulang webdriver-manager
pip install --upgrade webdriver-manager
```

### ❌ Error: Module not found
```bash
# Install dependencies
pip install -r requirements.txt
```

### ❌ Browser tidak buka
```bash
# Update Chrome ke versi terbaru
# Download di: https://www.google.com/chrome/
```

### ❌ No data found
- Coba kata kunci yang lebih spesifik
- Check koneksi internet
- Coba scroll lebih banyak

---

## 💡 Tips untuk Hasil Maksimal

### ✅ Best Practices:
1. **Gunakan kata kunci spesifik** 
   - ✅ "travel agent di Jakarta Pusat"
   - ❌ "travel"

2. **Tentukan scroll sesuai kebutuhan**
   - Small dataset: 5-10 scroll
   - Large dataset: 15-20 scroll

3. **Run di waktu non-peak**
   - Malam hari = koneksi lebih stabil
   - Siang hari = lebih ramai

4. **Check log file untuk debugging**
   ```bash
   tail -f scraper.log
   ```

---

## 📱 Output Format

CSV file dengan kolom:
```
namaTravel, alamat, kota, telepon, deskripsi, websiteUrl, logoUrl, email, mapUrl
```

### Contoh Data:
```csv
ABC Travel,Jl. Sudirman No.123,Jakarta,021-12345678,Travel Agency,https://abc.com,https://...,info@abc.com,https://maps.google.com/...
```

---

## 🎨 Customization

### Change Default Settings:
Edit `config.py`:

```python
# Lebih cepat (reduce timeout)
ScraperConfig.DETAIL_PAGE_DELAY = 1  # dari 3

# Lebih teliti (increase timeout)
ScraperConfig.EMAIL_BODY_WAIT = 10  # dari 7

# More retries
ScraperConfig.MAX_RETRIES = 5  # dari 3
```

---

## 🚀 Advanced Usage

### Programmatic Usage:
```python
from gmaps_scraper import GoogleMapsScraper

# Create scraper instance
scraper = GoogleMapsScraper(headless=True)

# Run scraping
output_file, count = scraper.run(
    query="restaurant in Jakarta",
    max_scrolls=20
)

print(f"Saved to: {output_file}")
print(f"Total: {count} records")
```

### Batch Processing:
```python
queries = [
    "hotel di Bali",
    "restaurant di Bandung", 
    "cafe di Yogyakarta"
]

scraper = GoogleMapsScraper(headless=True)

for query in queries:
    print(f"Processing: {query}")
    scraper.run(query, max_scrolls=10)
```

---

## 📞 Need Help?

1. **Check README.md** - Comprehensive documentation
2. **Check IMPROVEMENTS.md** - What's new in v18
3. **Check scraper.log** - Detailed error logs
4. **Check results/** folder - Your CSV outputs

---

**Happy Scraping! 🎉**

*Jika ada pertanyaan, refer to README.md atau check log file*

