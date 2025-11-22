"""
Utility Functions Module
=========================

Helper functions untuk reduce code duplication.
Mengikuti DRY (Don't Repeat Yourself) dan KISS (Keep It Simple, Stupid) principles.

Author: rotiawan
Date: 2025-11-22
Version: 18.0.0
"""

import re
import logging
import time
from typing import Optional, Tuple, Dict
from functools import wraps

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)

# Import local modules
try:
    from . import constants as const
    from .config import ScraperConfig
except ImportError:
    import constants as const
    from config import ScraperConfig

# Setup logger
logger = logging.getLogger(__name__)


# ============================================================================
# DECORATOR FUNCTIONS
# ============================================================================

def retry_on_failure(
    max_retries: int = ScraperConfig.MAX_RETRIES,
    delay: int = ScraperConfig.RETRY_DELAY
):
    """
    Decorator untuk retry mechanism dengan exponential backoff.
    
    Implementasi exponential backoff: delay * (backoff_factor ^ attempt)
    Example: delay=2, backoff=2 → 2s, 4s, 8s, 16s, ...
    
    Args:
        max_retries: Maksimal percobaan ulang
        delay: Delay awal dalam detik
    
    Returns:
        Decorated function yang akan di-retry jika gagal
    
    Example:
        @retry_on_failure(max_retries=3, delay=2)
        def fetch_data():
            # ... code that might fail
            pass
    
    Note:
        Function akan raise exception terakhir jika semua retry gagal.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_retries - 1:
                        # Calculate exponential backoff delay
                        wait_time = delay * (ScraperConfig.BACKOFF_FACTOR ** attempt)
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for "
                            f"{func.__name__}: {e}. Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed for {func.__name__}"
                        )
            
            # Raise last exception jika semua attempts gagal
            raise last_exception
        
        return wrapper
    return decorator


# ============================================================================
# SELENIUM HELPER FUNCTIONS
# ============================================================================

def safe_find_element(
    driver: WebDriver,
    by: By,
    selector: str,
    attribute: Optional[str] = None,
    default: str = ""
) -> str:
    """
    Safely find element dan ambil text/attribute-nya.
    Return default value jika element tidak ditemukan.
    
    Args:
        driver: Selenium WebDriver instance
        by: By locator strategy (By.XPATH, By.CSS_SELECTOR, etc)
        selector: Selector string
        attribute: Attribute name to get (None = get text content)
        default: Default value if element not found
    
    Returns:
        String value dari element atau default value
    
    Example:
        # Get text content
        name = safe_find_element(driver, By.XPATH, "//h1")
        
        # Get attribute
        url = safe_find_element(driver, By.XPATH, "//a", attribute="href")
    """
    try:
        element = driver.find_element(by, selector)
        
        if attribute:
            value = element.get_attribute(attribute)
        else:
            value = element.text
        
        return value.strip() if value else default
        
    except NoSuchElementException:
        logger.debug(f"Element tidak ditemukan: {selector}")
        return default
        
    except Exception as e:
        logger.debug(f"Error saat find element {selector}: {e}")
        return default


def close_extra_tabs(driver: WebDriver, keep_first: bool = True) -> None:
    """
    Tutup semua tab extra, keep hanya tab pertama.
    Berguna untuk cleanup setelah membuka banyak tabs.
    
    Args:
        driver: Selenium WebDriver instance
        keep_first: Jika True, keep tab pertama (default behavior)
    
    Note:
        Function ini akan gracefully handle jika tab sudah tertutup.
    """
    try:
        if len(driver.window_handles) <= 1:
            return  # No extra tabs to close
        
        current_handle = driver.window_handles[0] if keep_first else None
        
        for handle in driver.window_handles:
            if keep_first and handle == current_handle:
                continue
            
            driver.switch_to.window(handle)
            driver.close()
        
        # Switch back to main window
        if keep_first and current_handle:
            driver.switch_to.window(current_handle)
            
    except Exception as e:
        logger.warning(f"Error closing tabs: {e}")


def scroll_element(
    driver: WebDriver,
    element: WebElement,
    max_scrolls: int,
    pause_time: float = ScraperConfig.SCROLL_PAUSE_TIME
) -> bool:
    """
    Scroll element secara bertahap dengan detection end of list.
    
    Args:
        driver: Selenium WebDriver instance
        element: WebElement yang akan di-scroll
        max_scrolls: Jumlah maksimal scroll
        pause_time: Jeda antar scroll (detik)
    
    Returns:
        True jika mencapai end of list, False jika mencapai max_scrolls
    
    Note:
        Function akan stop early jika menemukan "end of list" marker.
    """
    for i in range(max_scrolls):
        # Scroll to bottom
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight",
            element
        )
        time.sleep(pause_time)
        
        # Check end of list marker
        try:
            end_markers = driver.find_elements(
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_END_OF_LIST]
            )
            if end_markers:
                logger.info(f"✅ {const.INFO_REACH_END} setelah {i+1} scroll")
                return True
        except Exception:
            pass  # Continue scrolling
        
        # Log progress periodically
        if (i + 1) % ScraperConfig.SCROLL_PROGRESS_INTERVAL == 0:
            logger.info(f"Progress scroll: {i+1}/{max_scrolls}")
    
    return False


# ============================================================================
# DATA VALIDATION FUNCTIONS
# ============================================================================

def validate_email(email: str) -> bool:
    """
    Validasi email address dengan regex dan business rules.
    
    Validation rules:
    1. Minimum length check
    2. Regex pattern matching (RFC 5322 simplified)
    3. Blacklist check (dummy domains)
    4. Image extension check (false positives)
    
    Args:
        email: Email string untuk divalidasi
    
    Returns:
        True jika email valid, False jika tidak
    
    Example:
        >>> validate_email("user@example.com")
        False  # example.com is blacklisted
        >>> validate_email("user@company.co.id")
        True
    """
    if not email or len(email) < ScraperConfig.EMAIL_MIN_LENGTH:
        return False
    
    if len(email) > ScraperConfig.EMAIL_MAX_LENGTH:
        return False
    
    # Regex validation
    if not re.match(const.EMAIL_PATTERN, email):
        return False
    
    # Blacklist check
    email_lower = email.lower()
    for blacklisted in ScraperConfig.EMAIL_BLACKLIST:
        if blacklisted in email_lower:
            return False
    
    # Image extension check
    for ext in ScraperConfig.EMAIL_IMAGE_EXTENSIONS:
        if ext in email_lower:
            return False
    
    return True


def extract_email_from_text(text: str) -> Optional[str]:
    """
    Extract email dari text menggunakan regex.
    Return first valid email found.
    
    Args:
        text: Text source (HTML, plain text, etc)
    
    Returns:
        Email address jika ditemukan dan valid, None jika tidak
    
    Example:
        >>> extract_email_from_text("Contact us at info@company.com")
        "info@company.com"
    """
    if not text:
        return None
    
    matches = re.findall(const.EMAIL_EXTRACT_PATTERN, text.lower())
    
    for match in matches:
        if validate_email(match):
            return match
    
    return None


def validate_data(
    data: Dict[str, str],
    mode: str = ScraperConfig.VALIDATION_MODE
) -> Tuple[bool, str]:
    """
    Validasi data berdasarkan validation mode.
    
    Args:
        data: Dictionary data yang akan divalidasi
        mode: Validation mode ('STRICT', 'MODERATE', 'LENIENT', 'NONE')
    
    Returns:
        Tuple (is_valid: bool, reason: str)
        - is_valid: True jika data memenuhi requirement
        - reason: Reason jika tidak valid, atau "Valid" jika valid
    
    Example:
        >>> data = {"namaTravel": "PT ABC", "telepon": "021123"}
        >>> is_valid, reason = validate_data(data, "LENIENT")
        >>> print(is_valid)  # True
    """
    # Validate mode
    if mode not in const.VALIDATION_MODES:
        logger.warning(f"Invalid validation mode: {mode}. Using MODERATE.")
        mode = const.VALIDATION_MODE_MODERATE
    
    required_fields = ScraperConfig.VALIDATION_RULES[mode]
    
    # Mode NONE: semua data valid
    if not required_fields:
        return True, "No validation required"
    
    # Check required fields
    missing_fields = []
    for field in required_fields:
        value = data.get(field, "").strip()
        if not value:
            missing_fields.append(field)
    
    if missing_fields:
        reason = f"Missing: {', '.join(missing_fields)}"
        return False, reason
    
    return True, "Valid"


# ============================================================================
# DATA TRANSFORMATION FUNCTIONS
# ============================================================================

def truncate_fields(data: Dict[str, str]) -> Dict[str, str]:
    """
    Truncate fields yang terlalu panjang sesuai MAX_FIELD_LENGTH.
    Menghindari error saat save ke database/CSV.
    
    Args:
        data: Dictionary data
    
    Returns:
        New dictionary dengan fields yang sudah di-truncate
    
    Note:
        Truncated fields akan diberi suffix "..." untuk indikasi.
    """
    truncated = {}
    
    for key, value in data.items():
        if key in ScraperConfig.MAX_FIELD_LENGTH:
            max_len = ScraperConfig.MAX_FIELD_LENGTH[key]
            
            if value and len(value) > max_len:
                # Truncate dan tambah ellipsis
                truncated[key] = value[:max_len - 3] + "..."
                logger.debug(f"Truncated {key}: {len(value)} → {max_len} chars")
            else:
                truncated[key] = value
        else:
            truncated[key] = value
    
    return truncated


def extract_city_from_address(address: str) -> str:
    """
    Extract nama kota dari string alamat (best effort).
    
    Heuristic:
    - Split by comma
    - Ambil bagian kedua dari belakang
    - Skip jika hanya angka (kemungkinan kode pos)
    
    Args:
        address: String alamat lengkap
    
    Returns:
        Nama kota (best guess) atau empty string
    
    Example:
        >>> extract_city_from_address("Jl. Sudirman No.1, Jakarta Pusat, DKI Jakarta")
        "Jakarta Pusat"
    """
    if not address:
        return ""
    
    try:
        parts = [p.strip() for p in address.split(',')]
        
        if len(parts) > 1:
            # Ambil bagian kedua dari belakang
            city_candidate = parts[-2]
            
            # Cek apakah bagian terakhir adalah kode pos (pure digits)
            last_part = parts[-1].split()[-1]
            if re.match(r'^\d+$', last_part) and len(parts) > 2:
                city_candidate = parts[-3]
            
            return city_candidate
            
    except Exception as e:
        logger.debug(f"Error extracting city from '{address}': {e}")
    
    return ""


def format_phone_number(phone: str) -> str:
    """
    Format nomor telepon dengan standard format.
    Remove unwanted characters, keep only digits, +, spaces, (), -.
    
    Args:
        phone: Raw phone number string
    
    Returns:
        Cleaned phone number
    
    Example:
        >>> format_phone_number("Phone: +62-21-1234567 ext.100")
        "+62-21-1234567"
    """
    if not phone:
        return ""
    
    # Remove common prefixes
    phone = phone.strip()
    
    # Clean: keep only digits, +, spaces, (), -
    phone = re.sub(const.PHONE_CLEANUP_PATTERN, '', phone)
    
    return phone.strip()


def sanitize_filename(text: str, max_length: int = const.MAX_LENGTH_FILENAME) -> str:
    """
    Sanitize text untuk dijadikan filename yang aman.
    
    Rules:
    - Keep only alphanumeric, spaces, hyphens, underscores
    - Replace spaces/multiple underscores with single underscore
    - Lowercase
    - Limit length
    
    Args:
        text: Text input
        max_length: Maksimal panjang filename
    
    Returns:
        Sanitized filename string
    
    Example:
        >>> sanitize_filename("Travel Umrah di Jakarta!!", 30)
        "travel_umrah_di_jakarta"
    """
    # Replace special chars with underscore
    sanitized = "".join(
        c if c.isalnum() or c in (' ', '-', '_') else '_'
        for c in text
    )
    
    # Replace multiple spaces/underscores with single underscore
    sanitized = re.sub(const.FILENAME_ALLOWED_CHARS_PATTERN, '_', sanitized)
    
    # Trim, lowercase
    sanitized = sanitized.strip('_').lower()
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_')
    
    return sanitized


# ============================================================================
# PROGRESS TRACKING CLASSES
# ============================================================================

class ProgressTracker:
    """
    Helper class untuk tracking progress dengan style yang konsisten.
    
    Attributes:
        total: Total items yang akan diproses
        current: Current progress counter
        desc: Description/label untuk progress
    
    Example:
        tracker = ProgressTracker(100, "Processing")
        for item in items:
            # ... process item ...
            tracker.update(1, f"Processed {item.name}")
        tracker.complete()
    """
    
    def __init__(self, total: int, desc: str = "Progress"):
        """
        Initialize progress tracker.
        
        Args:
            total: Total items yang akan diproses
            desc: Description label
        """
        self.total = total
        self.current = 0
        self.desc = desc
    
    def update(self, increment: int = 1, message: str = "") -> None:
        """
        Update progress counter dan log.
        
        Args:
            increment: Jumlah increment (default: 1)
            message: Optional message untuk di-log
        """
        self.current += increment
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        status = f"[{self.current}/{self.total}] ({percentage:.1f}%)"
        
        if message:
            logger.info(f"{self.desc} {status} - {message}")
        else:
            logger.info(f"{self.desc} {status}")
    
    def complete(self, message: str = "Selesai") -> None:
        """
        Mark progress as complete.
        
        Args:
            message: Completion message
        """
        logger.info(f"✅ {self.desc} {message} - Total: {self.current}/{self.total}")


class DataStatistics:
    """
    Helper class untuk tracking statistics scraping.
    Mengumpulkan data tentang berapa banyak yang berhasil/gagal dan alasannya.
    
    Attributes:
        total_processed: Total data yang diproses
        total_saved: Total data yang berhasil disimpan
        total_skipped: Total data yang di-skip
        skip_reasons: Dictionary of skip reasons dan count-nya
    
    Example:
        stats = DataStatistics()
        for data in scraped_data:
            if is_valid(data):
                stats.add_saved()
            else:
                stats.add_skipped("Missing email")
        print(stats.get_summary())
    """
    
    def __init__(self):
        """Initialize statistics counters"""
        self.total_processed = 0
        self.total_saved = 0
        self.total_skipped = 0
        self.skip_reasons: Dict[str, int] = {}
    
    def add_saved(self) -> None:
        """Increment saved counter"""
        self.total_processed += 1
        self.total_saved += 1
    
    def add_skipped(self, reason: str) -> None:
        """
        Increment skipped counter dengan reason tracking.
        
        Args:
            reason: Alasan kenapa di-skip
        """
        self.total_processed += 1
        self.total_skipped += 1
        
        # Track skip reasons
        self.skip_reasons[reason] = self.skip_reasons.get(reason, 0) + 1
    
    def get_success_rate(self) -> float:
        """
        Calculate success rate.
        
        Returns:
            Success rate in percentage (0-100)
        """
        if self.total_processed == 0:
            return 0.0
        return (self.total_saved / self.total_processed) * 100
    
    def get_summary(self) -> str:
        """
        Generate formatted summary statistics.
        
        Returns:
            Formatted string dengan box drawing characters
        """
        success_rate = self.get_success_rate()
        fail_rate = 100 - success_rate
        
        # Build summary with box drawing
        lines = [
            "",
            "╔══════════════════════════════════════════════════════════╗",
            "║           📊 STATISTIK SCRAPING RESULTS                  ║",
            "╠══════════════════════════════════════════════════════════╣",
            f"║  Total Diproses    : {self.total_processed:>4} bisnis                      ║",
            f"║  ✅ Tersimpan      : {self.total_saved:>4} bisnis ({success_rate:>5.1f}%)             ║",
            f"║  ❌ Dilewati       : {self.total_skipped:>4} bisnis ({fail_rate:>5.1f}%)             ║",
            "╠══════════════════════════════════════════════════════════╣",
        ]
        
        # Add skip reasons if any
        if self.skip_reasons:
            lines.append("║  📋 Alasan Dilewati:                                     ║")
            
            # Sort by count (descending)
            sorted_reasons = sorted(
                self.skip_reasons.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            for reason, count in sorted_reasons:
                # Truncate reason if too long
                reason_short = reason[:40] if len(reason) > 40 else reason
                lines.append(f"║     • {reason_short:<40} : {count:>3}  ║")
        
        lines.append("╚══════════════════════════════════════════════════════════╝")
        
        return "\n".join(lines)
