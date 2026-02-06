# 🗺️ Google Maps Lead Scraper

Tool untuk mengambil data bisnis dari Google Maps secara otomatis.

**Apa yang bisa diambil:**

- Nama bisnis
- Alamat & kota
- Nomor telepon
- Website
- Email (dari website bisnis)

---

## 📋 Persyaratan

1. **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
2. **Google Chrome** - [Download Chrome](https://www.google.com/chrome/)

---

## 🚀 Cara Menggunakan

### Langkah 1: Download Project

```bash
git clone https://github.com/rotiawan/gmaps-scraper.git
cd gmaps-scraper
```

### Langkah 2: Install Dependencies

```bash
pip install -r gmaps_scraper/requirements.txt
```

### Langkah 3: Jalankan

```bash
cd gmaps_scraper
python gmaps_scraper.py
```

### Langkah 4: Ikuti Petunjuk

Program akan menanyakan:

1. **Kata kunci** - Contoh: `restoran di Jakarta`
2. **Jumlah scroll** - Tekan Enter untuk default (15)
3. **Mode validasi** - Pilih 1-4:
   - `1` = Data harus lengkap semua
   - `2` = Harus ada nama, website, email ⭐ (Disarankan)
   - `3` = Harus ada nama dan telepon
   - `4` = Simpan semua data
4. **Headless mode** - Ketik `y` jika tidak ingin melihat browser

### Langkah 5: Hasil

File CSV akan tersimpan di folder `results/` dengan format:

```
results/restoran_di_jakarta_20260206_143052.csv
```

---

## 📁 Struktur Hasil CSV

| Kolom      | Isi              |
| ---------- | ---------------- |
| namaTravel | Nama bisnis      |
| alamat     | Alamat lengkap   |
| kota       | Nama kota        |
| telepon    | Nomor telepon    |
| deskripsi  | Kategori bisnis  |
| websiteUrl | Link website     |
| email      | Alamat email     |
| mapUrl     | Link Google Maps |

---

## ❓ Troubleshooting

**"cannot find Chrome binary"**
→ Install Google Chrome terlebih dahulu

**Program tidak merespon**
→ Tunggu beberapa saat, atau tekan Ctrl+C untuk berhenti

**Tidak ada data tersimpan**
→ Coba mode validasi `4` (simpan semua)

---

## 📝 Lisensi

MIT License - Bebas digunakan untuk keperluan pribadi dan komersial.
