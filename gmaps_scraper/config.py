"""
Configuration Management Module
================================

Centralized configuration untuk Google Maps Scraper.
Menggunakan constants module untuk menghindari magic numbers/strings.
Mengikuti SOLID principles dan best practices.

Author: rotiawan
Date: 2025-11-22
Version: 18.0.0
"""

import os
from typing import Dict, List, Tuple, Final
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Import constants
try:
    from . import constants as const
except ImportError:
    import constants as const


class ScraperConfig:
    """
    Configuration class untuk scraper.
    Semua settings terpusat di sini untuk easy customization.
    
    Design Pattern: Singleton-like behavior dengan class methods
    """
    
    # ========================================================================
    # SELENIUM SETTINGS
    # ========================================================================
    
    USER_AGENT: Final[str] = const.USER_AGENT_CHROME
    PAGE_LOAD_TIMEOUT: Final[int] = const.TIMEOUT_PAGE_LOAD
    IMPLICIT_WAIT: Final[int] = const.TIMEOUT_IMPLICIT_WAIT
    EXPLICIT_WAIT: Final[int] = const.TIMEOUT_EXPLICIT_WAIT
    
    # ========================================================================
    # SCRAPING SETTINGS
    # ========================================================================
    
    DEFAULT_MAX_SCROLLS: Final[int] = const.DEFAULT_MAX_SCROLLS
    SCROLL_PAUSE_TIME: Final[float] = const.DELAY_SCROLL_PAUSE
    AFTER_SEARCH_DELAY: Final[float] = const.DELAY_AFTER_SEARCH
    DETAIL_PAGE_DELAY: Final[float] = const.DELAY_DETAIL_PAGE
    SCROLL_PROGRESS_INTERVAL: Final[int] = const.SCROLL_PROGRESS_INTERVAL
    
    # ========================================================================
    # EMAIL FINDER SETTINGS
    # ========================================================================
    
    EMAIL_PAGE_LOAD_TIMEOUT: Final[int] = const.TIMEOUT_EMAIL_PAGE_LOAD
    EMAIL_BODY_WAIT: Final[int] = const.TIMEOUT_EMAIL_BODY_WAIT
    EMAIL_BLACKLIST: Final[Tuple[str, ...]] = const.EMAIL_BLACKLIST
    EMAIL_IMAGE_EXTENSIONS: Final[Tuple[str, ...]] = const.EMAIL_IMAGE_EXTENSIONS
    EMAIL_MIN_LENGTH: Final[int] = const.EMAIL_MIN_LENGTH
    EMAIL_MAX_LENGTH: Final[int] = const.EMAIL_MAX_LENGTH
    
    # ========================================================================
    # RETRY SETTINGS
    # ========================================================================
    
    MAX_RETRIES: Final[int] = const.MAX_RETRIES
    RETRY_DELAY: Final[int] = const.DELAY_RETRY_BASE
    BACKOFF_FACTOR: Final[int] = const.BACKOFF_FACTOR
    
    # ========================================================================
    # CSV SETTINGS
    # ========================================================================
    
    CSV_HEADERS: Final[List[str]] = list(const.CSV_HEADERS)
    CSV_ENCODING: Final[str] = const.CSV_ENCODING
    FLUSH_INTERVAL: Final[int] = const.FLUSH_INTERVAL
    
    # ========================================================================
    # DATA VALIDATION SETTINGS
    # ========================================================================
    
    # Default validation mode
    VALIDATION_MODE: str = const.VALIDATION_MODE_MODERATE
    
    # Field requirements untuk setiap mode
    VALIDATION_RULES: Final[Dict[str, List[str]]] = {
        const.VALIDATION_MODE_STRICT: [
            const.CSV_HEADER_NAMA,
            const.CSV_HEADER_ALAMAT,
            const.CSV_HEADER_KOTA,
            const.CSV_HEADER_TELEPON,
            const.CSV_HEADER_DESKRIPSI,
            const.CSV_HEADER_WEBSITE,
            const.CSV_HEADER_LOGO,
            const.CSV_HEADER_EMAIL,
            const.CSV_HEADER_MAP_URL
        ],
        const.VALIDATION_MODE_MODERATE: [
            const.CSV_HEADER_NAMA,
            const.CSV_HEADER_WEBSITE,
            const.CSV_HEADER_EMAIL
        ],
        const.VALIDATION_MODE_LENIENT: [
            const.CSV_HEADER_NAMA,
            const.CSV_HEADER_TELEPON
        ],
        const.VALIDATION_MODE_NONE: []
    }
    
    # Maximum field lengths
    MAX_FIELD_LENGTH: Final[Dict[str, int]] = {
        const.CSV_HEADER_NAMA: const.MAX_LENGTH_NAMA,
        const.CSV_HEADER_ALAMAT: const.MAX_LENGTH_ALAMAT,
        const.CSV_HEADER_KOTA: const.MAX_LENGTH_KOTA,
        const.CSV_HEADER_TELEPON: const.MAX_LENGTH_TELEPON,
        const.CSV_HEADER_DESKRIPSI: const.MAX_LENGTH_DESKRIPSI,
        const.CSV_HEADER_WEBSITE: const.MAX_LENGTH_WEBSITE,
        const.CSV_HEADER_LOGO: const.MAX_LENGTH_LOGO,
        const.CSV_HEADER_EMAIL: const.MAX_LENGTH_EMAIL,
        const.CSV_HEADER_MAP_URL: const.MAX_LENGTH_MAP_URL
    }
    
    # ========================================================================
    # XPATH/CSS SELECTORS
    # ========================================================================
    
    SELECTORS: Final[Dict[str, Tuple[By, str] | str]] = {
        const.SELECTOR_ID_SEARCH_BOX: (By.ID, "searchboxinput"),
        const.SELECTOR_ID_FEED: "//div[@role='feed']",
        const.SELECTOR_ID_RESULT_LINKS: "div[role='feed'] a.hfpxzc",
        const.SELECTOR_ID_END_OF_LIST: (
            "//span[contains(text(), 'You have reached the end of the list') or "
            "contains(text(), 'Anda telah mencapai akhir daftar')]"
        ),
        const.SELECTOR_ID_NAME: "//h1",
        const.SELECTOR_ID_ADDRESS: (
            "//button[contains(@aria-label, 'Address') or "
            "contains(@aria-label, 'Alamat')]"
        ),
        const.SELECTOR_ID_PHONE: (
            "//button[contains(@aria-label, 'Phone') or "
            "contains(@aria-label, 'Telepon')]"
        ),
        const.SELECTOR_ID_CATEGORY: "//button[contains(@jsaction, 'pane.rating.category')]",
        const.SELECTOR_ID_WEBSITE: (
            "//a[contains(@aria-label, 'Website') or "
            "contains(@data-item-id, 'authority')]"
        ),
        const.SELECTOR_ID_LOGO: "//button[contains(@jsaction, 'hero')]/img",
        const.SELECTOR_ID_MAILTO: "//a[starts-with(@href, 'mailto:')]"
    }
    
    # ========================================================================
    # LOGGING SETTINGS
    # ========================================================================
    
    LOG_FORMAT: Final[str] = const.LOG_FORMAT
    LOG_DATE_FORMAT: Final[str] = const.LOG_DATE_FORMAT
    LOG_LEVEL: Final[str] = const.LOG_LEVEL_DEFAULT
    LOG_FILE_NAME: Final[str] = const.LOG_FILE_NAME
    
    # ========================================================================
    # OUTPUT SETTINGS
    # ========================================================================
    
    OUTPUT_DIR: Final[str] = const.OUTPUT_DIR_NAME
    DATE_FORMAT: Final[str] = const.DATE_FORMAT
    
    # ========================================================================
    # CLASS METHODS
    # ========================================================================
    
    @classmethod
    def get_chrome_options(cls, headless: bool = False) -> Options:
        """
        Generate Chrome options dengan best practices untuk anti-detection.
        
        Args:
            headless: Jika True, run browser tanpa UI
        
        Returns:
            Configured Chrome Options instance
        
        Note:
            Options ini dirancang untuk menghindari deteksi sebagai bot.
        """
        options = Options()
        
        # User agent untuk appear as normal browser
        options.add_argument(f"user-agent={cls.USER_AGENT}")
        
        # Window settings
        options.add_argument('--start-maximized')
        
        # Anti-detection measures
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Page load strategy: 'eager' = don't wait for images/css
        options.page_load_strategy = 'eager'
        
        # Headless mode if requested
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        
        return options
    
    @classmethod
    def create_output_dir(cls) -> Path:
        """
        Buat folder output jika belum ada.
        
        Returns:
            Path object ke output directory
        
        Raises:
            OSError: Jika gagal create directory
        """
        output_path = Path(cls.OUTPUT_DIR)
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validasi konfigurasi untuk memastikan semua settings valid.
        
        Returns:
            True jika config valid, False jika ada issue
        
        Note:
            Method ini bisa dipanggil saat startup untuk early detection of issues.
        """
        try:
            # Check validation mode
            if cls.VALIDATION_MODE not in const.VALIDATION_MODES:
                print(f"⚠️  Warning: Invalid VALIDATION_MODE '{cls.VALIDATION_MODE}'. "
                      f"Using default: {const.VALIDATION_MODE_MODERATE}")
                cls.VALIDATION_MODE = const.VALIDATION_MODE_MODERATE
            
            # Check numeric values
            if cls.DEFAULT_MAX_SCROLLS < 1:
                print(f"⚠️  Warning: DEFAULT_MAX_SCROLLS must be >= 1. Using 15.")
                cls.DEFAULT_MAX_SCROLLS = 15
            
            if cls.MAX_RETRIES < 1:
                print(f"⚠️  Warning: MAX_RETRIES must be >= 1. Using 3.")
                cls.MAX_RETRIES = 3
            
            return True
            
        except Exception as e:
            print(f"❌ Config validation error: {e}")
            return False
    
    @classmethod
    def get_validation_modes_info(cls) -> Dict[str, str]:
        """
        Get informasi lengkap tentang validation modes.
        
        Returns:
            Dictionary dengan mode sebagai key dan deskripsi sebagai value
        """
        return {
            const.VALIDATION_MODE_STRICT: 
                "Semua field wajib terisi (~10-20% data tersimpan)",
            const.VALIDATION_MODE_MODERATE: 
                "Minimal: nama, website, email (~20-30% data tersimpan) [RECOMMENDED]",
            const.VALIDATION_MODE_LENIENT: 
                "Minimal: nama, telepon (~80-90% data tersimpan)",
            const.VALIDATION_MODE_NONE: 
                "Simpan semua data tanpa filter (~100% data tersimpan)"
        }
    
    @classmethod
    def print_config_summary(cls) -> None:
        """Print summary dari current configuration"""
        print("\n" + "="*70)
        print("⚙️  CONFIGURATION SUMMARY")
        print("="*70)
        print(f"Max Scrolls       : {cls.DEFAULT_MAX_SCROLLS}")
        print(f"Validation Mode   : {cls.VALIDATION_MODE}")
        print(f"Max Retries       : {cls.MAX_RETRIES}")
        print(f"Output Directory  : {cls.OUTPUT_DIR}")
        print(f"Log Level         : {cls.LOG_LEVEL}")
        print("="*70 + "\n")


# Initialize and validate config on module load
ScraperConfig.validate_config()
