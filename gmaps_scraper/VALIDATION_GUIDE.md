# 🔍 Data Validation Guide

## Overview

Versi v18 mendukung **data filtering dengan 4 mode validation** untuk memastikan kualitas data yang di-scrape.

---

## 🎯 Validation Modes

### 1. **STRICT Mode** (Semua field wajib)

**Required Fields:**
- ✅ namaTravel
- ✅ alamat
- ✅ kota
- ✅ telepon
- ✅ deskripsi
- ✅ websiteUrl
- ✅ logoUrl
- ✅ email
- ✅ mapUrl

**Expected Results:**
- ~10-20% data tersimpan
- Kualitas data: ⭐⭐⭐⭐⭐ (Excellent)
- Use case: Data marketing premium, direct contact

**Pros:**
- Data sangat lengkap dan berkualitas tinggi
- Cocok untuk campaign marketing langsung
- Semua informasi kontak tersedia

**Cons:**
- Sangat sedikit data yang lolos filter
- Banyak bisnis tidak punya semua field
- Time consuming untuk hasil minimal

---

### 2. **MODERATE Mode** (Recommended) ⭐

**Required Fields:**
- ✅ namaTravel
- ✅ websiteUrl
- ✅ email

**Expected Results:**
- ~20-30% data tersimpan
- Kualitas data: ⭐⭐⭐⭐ (Very Good)
- Use case: Email marketing, B2B outreach

**Pros:**
- Balance antara quantity dan quality
- Fokus ke data penting untuk marketing
- Dapat email untuk cold outreach

**Cons:**
- Beberapa data mungkin tidak punya telepon
- Alamat mungkin kosong

**💡 Recommended untuk:**
- Email marketing campaigns
- B2B lead generation
- Website outreach
- Cold email lists

---

### 3. **LENIENT Mode** (Basic minimum)

**Required Fields:**
- ✅ namaTravel
- ✅ telepon

**Expected Results:**
- ~80-90% data tersimpan
- Kualitas data: ⭐⭐⭐ (Good)
- Use case: Cold calling, phone marketing

**Pros:**
- Banyak data tersimpan
- Minimal requirement tapi cukup untuk contact
- Cocok untuk telemarketing

**Cons:**
- Mungkin tidak ada email/website
- Harder untuk email outreach
- Kurang info detail

**💡 Recommended untuk:**
- Cold calling campaigns
- SMS marketing
- Basic lead list
- Local business outreach

---

### 4. **NONE Mode** (No filter)

**Required Fields:**
- (tidak ada - semua data disimpan)

**Expected Results:**
- ~100% data tersimpan
- Kualitas data: ⭐⭐ (Varies)
- Use case: Raw data collection, manual filtering

**Pros:**
- Semua data tersimpan
- Tidak ada data loss
- Bisa manual filter nanti

**Cons:**
- Banyak data incomplete
- Perlu manual cleaning
- Lower data quality

**💡 Recommended untuk:**
- Research dan analysis
- Manual data cleaning nanti
- Backup full data
- Testing scraper

---

## 📊 Perbandingan Mode

| Mode | Required Fields | Data Saved | Quality | Best For |
|------|----------------|------------|---------|----------|
| STRICT | 9 fields | ~10-20% | ⭐⭐⭐⭐⭐ | Premium marketing |
| MODERATE | 3 fields | ~20-30% | ⭐⭐⭐⭐ | Email marketing ⭐ |
| LENIENT | 2 fields | ~80-90% | ⭐⭐⭐ | Cold calling |
| NONE | 0 fields | ~100% | ⭐⭐ | Raw data collection |

---

## 🎮 Cara Menggunakan

### Method 1: Interactive (Saat Run)

```bash
python gmaps_scraper.py
```

Program akan tanya:
```
🔍 Pilih Data Validation Mode:
   1. STRICT   - Semua field wajib terisi (~10-20% data tersimpan)
   2. MODERATE - Minimal: nama, website, email (~20-30% data tersimpan) [RECOMMENDED]
   3. LENIENT  - Minimal: nama, telepon (~80-90% data tersimpan)
   4. NONE     - Simpan semua data tanpa filter (~100% data tersimpan)

Pilih mode (1-4, default: 2): 
```

### Method 2: Edit Config (Permanent)

Edit `config.py`:

```python
# Untuk email marketing (RECOMMENDED)
VALIDATION_MODE = 'MODERATE'

# Untuk cold calling
VALIDATION_MODE = 'LENIENT'

# Untuk premium data
VALIDATION_MODE = 'STRICT'

# Untuk raw data
VALIDATION_MODE = 'NONE'
```

### Method 3: Programmatic

```python
from config import ScraperConfig
from gmaps_scraper import GoogleMapsScraper

# Set validation mode
ScraperConfig.VALIDATION_MODE = 'MODERATE'

scraper = GoogleMapsScraper()
output_file, count, stats = scraper.run("travel agent Jakarta", 15)

print(stats.get_summary())
```

---

## 📈 Output Statistics

Setelah scraping selesai, kamu akan dapat statistik detail:

```
╔══════════════════════════════════════════════════════════╗
║           📊 STATISTIK SCRAPING RESULTS                  ║
╠══════════════════════════════════════════════════════════╣
║  Total Diproses    :  150 bisnis                         ║
║  ✅ Tersimpan      :   42 bisnis ( 28.0%)                ║
║  ❌ Dilewati       :  108 bisnis ( 72.0%)                ║
╠══════════════════════════════════════════════════════════╣
║  📋 Alasan Dilewati:                                     ║
║     • Missing: websiteUrl, email                  :  65  ║
║     • Missing: email                              :  28  ║
║     • Missing: websiteUrl                         :  15  ║
╚══════════════════════════════════════════════════════════╝
```

---

## 💡 Rekomendasi Berdasarkan Use Case

### 🎯 Email Marketing Campaign
**Mode: MODERATE** ⭐
- Dapat email untuk outreach
- Dapat website untuk research
- Cukup data untuk personalisasi

### 📞 Cold Calling Campaign
**Mode: LENIENT**
- Dapat telepon untuk call
- Cukup nama bisnis
- High volume leads

### 🏆 Premium Lead List
**Mode: STRICT**
- Data super lengkap
- High value prospects
- Ready untuk sales team

### 📊 Data Analysis
**Mode: NONE**
- Raw data lengkap
- Manual filtering nanti
- Research purpose

---

## 🔧 Custom Validation Rules

Kamu bisa custom required fields di `config.py`:

```python
VALIDATION_RULES = {
    'STRICT': [
        'namaTravel', 'alamat', 'kota', 'telepon', 
        'deskripsi', 'websiteUrl', 'logoUrl', 'email', 'mapUrl'
    ],
    
    'MODERATE': [
        'namaTravel', 'websiteUrl', 'email'
    ],
    
    'LENIENT': [
        'namaTravel', 'telepon'
    ],
    
    # Custom mode contoh:
    'CUSTOM': [
        'namaTravel', 'alamat', 'email'  # Custom requirements
    ],
    
    'NONE': []
}
```

Kemudian set:
```python
ScraperConfig.VALIDATION_MODE = 'CUSTOM'
```

---

## 📝 Field Length Limits

Semua field di-truncate otomatis jika terlalu panjang:

```python
MAX_FIELD_LENGTH = {
    'namaTravel': 256,    # chars
    'alamat': 512,
    'kota': 100,
    'telepon': 50,
    'deskripsi': 512,
    'websiteUrl': 256,
    'logoUrl': 256,
    'email': 256,
    'mapUrl': 512
}
```

---

## ❓ FAQ

### Q: Kenapa data saya sedikit?
**A:** Coba mode yang lebih lenient (LENIENT atau NONE) untuk hasil lebih banyak.

### Q: Kok banyak skip "Missing: email"?
**A:** Tidak semua bisnis punya email visible di website. Ini normal ~50-70% bisnis.

### Q: Mode mana yang paling bagus?
**A:** Tergantung use case:
- Email marketing → **MODERATE**
- Cold calling → **LENIENT**
- Premium list → **STRICT**
- Research → **NONE**

### Q: Bisa ubah validation setelah scraping?
**A:** Tidak. Tapi kamu bisa scrape ulang dengan mode NONE, simpan semua, lalu filter manual.

### Q: Gimana cara tambah custom field requirement?
**A:** Edit `config.py` → tambah custom mode di `VALIDATION_RULES` → set `VALIDATION_MODE`.

---

## 🎓 Best Practices

1. **Start with MODERATE** - Balance terbaik
2. **Check statistics** - Monitor success rate
3. **Adjust based on results** - Jika terlalu sedikit, lower mode
4. **Know your use case** - Different goals need different modes
5. **Test dulu** - Run dengan scroll kecil untuk test mode

---

## 🚀 Next Steps

1. Pilih validation mode sesuai kebutuhan
2. Run scraper
3. Check statistics report
4. Adjust mode jika perlu
5. Use data untuk campaign! 🎉

---

**Happy Scraping with Quality Data! 📊**

