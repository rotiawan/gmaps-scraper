"""
Constants Module
================

Centralized constants untuk menghindari magic numbers/strings di codebase.
Mengikuti prinsip SOLID (Single Responsibility) dan DRY.

Author: rotiawan
Date: 2025-11-22
"""

from typing import Final

# ============================================================================
# APPLICATION CONSTANTS
# ============================================================================

APP_NAME: Final[str] = "Google Maps Lead Scraper"
APP_VERSION: Final[str] = "18.0.0"
APP_DESCRIPTION: Final[str] = "Professional lead generation tool from Google Maps"

# ============================================================================
# URL CONSTANTS
# ============================================================================

GOOGLE_MAPS_URL: Final[str] = "https://www.google.com/maps"

# ============================================================================
# TIMEOUT CONSTANTS (in seconds)
# ============================================================================

TIMEOUT_PAGE_LOAD: Final[int] = 300
TIMEOUT_IMPLICIT_WAIT: Final[int] = 10
TIMEOUT_EXPLICIT_WAIT: Final[int] = 20
TIMEOUT_EMAIL_PAGE_LOAD: Final[int] = 10
TIMEOUT_EMAIL_BODY_WAIT: Final[int] = 7

# ============================================================================
# DELAY CONSTANTS (in seconds)
# ============================================================================

DELAY_SCROLL_PAUSE: Final[float] = 3.0
DELAY_AFTER_SEARCH: Final[float] = 5.0
DELAY_DETAIL_PAGE: Final[float] = 3.0
DELAY_RETRY_BASE: Final[int] = 2

# ============================================================================
# RETRY CONSTANTS
# ============================================================================

MAX_RETRIES: Final[int] = 3
BACKOFF_FACTOR: Final[int] = 2

# ============================================================================
# SCRAPING CONSTANTS
# ============================================================================

DEFAULT_MAX_SCROLLS: Final[int] = 15
SCROLL_PROGRESS_INTERVAL: Final[int] = 5  # Log setiap N scrolls
FLUSH_INTERVAL: Final[int] = 10  # Flush CSV setiap N rows

# ============================================================================
# DATA VALIDATION CONSTANTS
# ============================================================================

# Validation modes
VALIDATION_MODE_STRICT: Final[str] = "STRICT"
VALIDATION_MODE_MODERATE: Final[str] = "MODERATE"
VALIDATION_MODE_LENIENT: Final[str] = "LENIENT"
VALIDATION_MODE_NONE: Final[str] = "NONE"

# Available validation modes list
VALIDATION_MODES: Final[tuple] = (
    VALIDATION_MODE_STRICT,
    VALIDATION_MODE_MODERATE,
    VALIDATION_MODE_LENIENT,
    VALIDATION_MODE_NONE
)

# ============================================================================
# EMAIL VALIDATION CONSTANTS
# ============================================================================

EMAIL_MIN_LENGTH: Final[int] = 5
EMAIL_MAX_LENGTH: Final[int] = 256

# Email blacklist - domain dummy yang sering ditemukan di template
EMAIL_BLACKLIST: Final[tuple] = (
    'example.com',
    'domain.com',
    'test.com',
    'sample.com',
    'your-domain.com',
    'yourdomain.com',
    'website.com'
)

# Image extensions yang sering muncul di email pattern (false positive)
EMAIL_IMAGE_EXTENSIONS: Final[tuple] = (
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    '.svg',
    '.webp',
    '.bmp',
    '.ico'
)

# ============================================================================
# REGEX PATTERNS
# ============================================================================

# Email regex pattern (RFC 5322 simplified)
EMAIL_PATTERN: Final[str] = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63}@[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
EMAIL_EXTRACT_PATTERN: Final[str] = r'[a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63}@[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Phone number cleanup pattern
PHONE_CLEANUP_PATTERN: Final[str] = r'[^\d+\s()-]'

# Filename sanitization pattern
FILENAME_ALLOWED_CHARS_PATTERN: Final[str] = r'[_\s]+'

# ============================================================================
# CSV/FILE CONSTANTS
# ============================================================================

CSV_ENCODING: Final[str] = 'utf-8-sig'  # UTF-8 with BOM for Excel compatibility
OUTPUT_DIR_NAME: Final[str] = "results"
DATE_FORMAT: Final[str] = "%Y%m%d_%H%M%S"
LOG_FILE_NAME: Final[str] = "scraper.log"

# CSV Headers/Columns
CSV_HEADER_NAMA: Final[str] = 'namaTravel'
CSV_HEADER_ALAMAT: Final[str] = 'alamat'
CSV_HEADER_KOTA: Final[str] = 'kota'
CSV_HEADER_TELEPON: Final[str] = 'telepon'
CSV_HEADER_DESKRIPSI: Final[str] = 'deskripsi'
CSV_HEADER_WEBSITE: Final[str] = 'websiteUrl'
CSV_HEADER_LOGO: Final[str] = 'logoUrl'
CSV_HEADER_EMAIL: Final[str] = 'email'
CSV_HEADER_MAP_URL: Final[str] = 'mapUrl'

CSV_HEADERS: Final[tuple] = (
    CSV_HEADER_NAMA,
    CSV_HEADER_ALAMAT,
    CSV_HEADER_KOTA,
    CSV_HEADER_TELEPON,
    CSV_HEADER_DESKRIPSI,
    CSV_HEADER_WEBSITE,
    CSV_HEADER_LOGO,
    CSV_HEADER_EMAIL,
    CSV_HEADER_MAP_URL
)

# ============================================================================
# FIELD LENGTH LIMITS
# ============================================================================

MAX_LENGTH_NAMA: Final[int] = 256
MAX_LENGTH_ALAMAT: Final[int] = 512
MAX_LENGTH_KOTA: Final[int] = 100
MAX_LENGTH_TELEPON: Final[int] = 50
MAX_LENGTH_DESKRIPSI: Final[int] = 512
MAX_LENGTH_WEBSITE: Final[int] = 256
MAX_LENGTH_LOGO: Final[int] = 256
MAX_LENGTH_EMAIL: Final[int] = 256
MAX_LENGTH_MAP_URL: Final[int] = 512
MAX_LENGTH_FILENAME: Final[int] = 50

# ============================================================================
# LOGGING CONSTANTS
# ============================================================================

LOG_FORMAT: Final[str] = '%(asctime)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT: Final[str] = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL_DEFAULT: Final[str] = 'INFO'

# ============================================================================
# USER AGENT CONSTANTS
# ============================================================================

USER_AGENT_CHROME: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ============================================================================
# XPATH/CSS SELECTORS IDs
# ============================================================================

SELECTOR_ID_SEARCH_BOX: Final[str] = "search_box"
SELECTOR_ID_FEED: Final[str] = "feed"
SELECTOR_ID_RESULT_LINKS: Final[str] = "result_links"
SELECTOR_ID_END_OF_LIST: Final[str] = "end_of_list"
SELECTOR_ID_NAME: Final[str] = "name"
SELECTOR_ID_ADDRESS: Final[str] = "address"
SELECTOR_ID_PHONE: Final[str] = "phone"
SELECTOR_ID_CATEGORY: Final[str] = "category"
SELECTOR_ID_WEBSITE: Final[str] = "website"
SELECTOR_ID_LOGO: Final[str] = "logo"
SELECTOR_ID_MAILTO: Final[str] = "mailto_links"

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_NO_LINKS_FOUND: Final[str] = "Tidak ada link ditemukan. Proses berhenti."
ERROR_EMPTY_QUERY: Final[str] = "Query pencarian tidak boleh kosong!"
ERROR_INVALID_SCROLL: Final[str] = "Minimal scroll adalah 1"
ERROR_INVALID_INPUT: Final[str] = "Input tidak valid, masukkan angka!"
ERROR_WEBDRIVER_SETUP: Final[str] = "Gagal setup WebDriver"

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_SEARCH: Final[str] = "Pencarian berhasil"
SUCCESS_WEBDRIVER: Final[str] = "WebDriver berhasil di-setup"
SUCCESS_CLEANUP: Final[str] = "Browser ditutup, cleanup selesai"

# ============================================================================
# INFO MESSAGES
# ============================================================================

INFO_SCROLLING_START: Final[str] = "Memulai scrolling untuk mengumpulkan link..."
INFO_COLLECTING_LINKS: Final[str] = "Mengumpulkan link hasil..."
INFO_REACH_END: Final[str] = "Mencapai akhir daftar"

