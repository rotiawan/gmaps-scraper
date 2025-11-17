"""
Configuration Management untuk Google Maps Scraper
Author: Improved Version
Date: 2025-11-17
"""

import os
from typing import Dict, Any
from selenium.webdriver.common.by import By

class ScraperConfig:
    """Konfigurasi untuk scraper - semua settings terpusat di sini"""
    
    # === SELENIUM SETTINGS ===
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    PAGE_LOAD_TIMEOUT = 300  # detik
    IMPLICIT_WAIT = 10  # detik
    EXPLICIT_WAIT = 20  # detik
    
    # === SCRAPING SETTINGS ===
    DEFAULT_MAX_SCROLLS = 15
    SCROLL_PAUSE_TIME = 3  # detik
    AFTER_SEARCH_DELAY = 5  # detik
    DETAIL_PAGE_DELAY = 3  # detik
    
    # === EMAIL FINDER SETTINGS ===
    EMAIL_PAGE_LOAD_TIMEOUT = 10  # detik (pendek untuk anti-stuck)
    EMAIL_BODY_WAIT = 7  # detik
    EMAIL_BLACKLIST = ['example.com', 'domain.com', 'test.com', 'sample.com']
    EMAIL_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']
    
    # === RETRY SETTINGS ===
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # detik
    BACKOFF_FACTOR = 2  # exponential backoff
    
    # === CSV SETTINGS ===
    CSV_HEADERS = [
        'namaTravel', 'alamat', 'kota', 'telepon', 
        'deskripsi', 'websiteUrl', 'logoUrl', 'email', 'mapUrl'
    ]
    CSV_ENCODING = 'utf-8-sig'  # Biar Excel bisa baca UTF-8 dengan baik
    
    # === DATA VALIDATION SETTINGS ===
    # Filter mode: 'STRICT', 'MODERATE', 'LENIENT', atau 'NONE'
    VALIDATION_MODE = 'MODERATE'
    
    # Field requirements untuk setiap mode
    VALIDATION_RULES = {
        'STRICT': [
            'namaTravel', 'alamat', 'kota', 'telepon', 
            'deskripsi', 'websiteUrl', 'logoUrl', 'email', 'mapUrl'
        ],  # Semua field wajib (~10-20% data tersimpan)
        
        'MODERATE': [
            'namaTravel', 'websiteUrl', 'email'
        ],  # Minimum requirement (~20-30% data tersimpan)
        
        'LENIENT': [
            'namaTravel', 'telepon'
        ],  # Basic minimum (~80-90% data tersimpan)
        
        'NONE': []  # No validation, save all data
    }
    
    # Maksimal panjang field (untuk truncate jika terlalu panjang)
    MAX_FIELD_LENGTH = {
        'namaTravel': 256,
        'alamat': 512,
        'kota': 100,
        'telepon': 50,
        'deskripsi': 512,
        'websiteUrl': 256,
        'logoUrl': 256,
        'email': 256,
        'mapUrl': 512
    }
    
    # === XPATH SELECTORS ===
    SELECTORS = {
        'search_box': (By.ID, "searchboxinput"),
        'feed': "//div[@role='feed']",
        'result_links': "div[role='feed'] a.hfpxzc",
        'end_of_list': "//span[contains(text(), 'You have reached the end of the list') or contains(text(), 'Anda telah mencapai akhir daftar')]",
        'name': "//h1",
        'address': "//button[contains(@aria-label, 'Address') or contains(@aria-label, 'Alamat')]",
        'phone': "//button[contains(@aria-label, 'Phone') or contains(@aria-label, 'Telepon')]",
        'category': "//button[contains(@jsaction, 'pane.rating.category')]",
        'website': "//a[contains(@aria-label, 'Website') or contains(@data-item-id, 'authority')]",
        'logo': "//button[contains(@jsaction, 'hero')]/img",
        'mailto_links': "//a[starts-with(@href, 'mailto:')]"
    }
    
    # === LOGGING SETTINGS ===
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_LEVEL = 'INFO'
    
    # === OUTPUT SETTINGS ===
    OUTPUT_DIR = "results"
    DATE_FORMAT = "%Y%m%d_%H%M%S"
    
    @classmethod
    def get_chrome_options(cls) -> 'ChromeOptions':
        """Generate Chrome options dengan best practices"""
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument(f"user-agent={cls.USER_AGENT}")
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.page_load_strategy = 'eager'
        
        # Uncomment untuk headless mode
        # options.add_argument('--headless=new')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--no-sandbox')
        
        return options
    
    @classmethod
    def create_output_dir(cls) -> str:
        """Buat folder output jika belum ada"""
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)
        return cls.OUTPUT_DIR

