"""
Utility Functions untuk Google Maps Scraper
Berisi helper functions untuk reduce code duplication
"""

import re
import logging
import time
from typing import Optional, Tuple, Dict
from functools import wraps
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from config import ScraperConfig

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = ScraperConfig.MAX_RETRIES, 
                    delay: int = ScraperConfig.RETRY_DELAY):
    """
    Decorator untuk retry mechanism dengan exponential backoff
    
    Args:
        max_retries: Maksimal percobaan ulang
        delay: Delay awal dalam detik
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
                        wait_time = delay * (ScraperConfig.BACKOFF_FACTOR ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator


def safe_find_element(driver: WebDriver, 
                      by: By, 
                      selector: str, 
                      attribute: Optional[str] = None,
                      default: str = "") -> str:
    """
    Safely find element dan ambil text/attribute-nya.
    Return default value jika element tidak ditemukan.
    
    Args:
        driver: Selenium WebDriver instance
        by: By locator strategy (By.XPATH, By.CSS_SELECTOR, etc)
        selector: Selector string
        attribute: Attribute name to get (None = get text)
        default: Default value if element not found
    
    Returns:
        String value dari element atau default value
    """
    try:
        element = driver.find_element(by, selector)
        if attribute:
            value = element.get_attribute(attribute)
        else:
            value = element.text
        return value if value else default
    except NoSuchElementException:
        logger.debug(f"Element tidak ditemukan: {selector}")
        return default
    except Exception as e:
        logger.debug(f"Error saat find element {selector}: {e}")
        return default


def validate_email(email: str) -> bool:
    """
    Validasi email address dengan regex yang lebih strict
    
    Args:
        email: Email string untuk divalidasi
    
    Returns:
        True jika email valid, False jika tidak
    """
    if not email or len(email) < 5:
        return False
    
    # Regex yang lebih strict untuk email validation
    email_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63}@[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False
    
    # Check blacklist
    email_lower = email.lower()
    for blacklisted in ScraperConfig.EMAIL_BLACKLIST:
        if blacklisted in email_lower:
            return False
    
    # Check image extensions
    for ext in ScraperConfig.EMAIL_IMAGE_EXTENSIONS:
        if ext in email_lower:
            return False
    
    return True


def extract_email_from_text(text: str) -> Optional[str]:
    """
    Extract email dari text menggunakan regex
    
    Args:
        text: Text source (HTML, plain text, etc)
    
    Returns:
        Email address jika ditemukan dan valid, None jika tidak
    """
    email_pattern = r'[a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63}@[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text.lower())
    
    for match in matches:
        if validate_email(match):
            return match
    
    return None


def extract_city_from_address(address: str) -> str:
    """
    Extract nama kota dari string alamat (best effort)
    
    Args:
        address: String alamat lengkap
    
    Returns:
        Nama kota (best guess) atau empty string
    """
    if not address:
        return ""
    
    try:
        parts = address.split(',')
        if len(parts) > 1:
            # Ambil bagian kedua dari belakang
            city_candidate = parts[-2].strip()
            
            # Jika bagian terakhir adalah kode pos, ambil yang ketiga dari belakang
            if re.match(r'^\d+$', city_candidate.split()[-1]):
                if len(parts) > 2:
                    city_candidate = parts[-3].strip()
            
            return city_candidate
    except Exception as e:
        logger.debug(f"Error extracting city: {e}")
    
    return ""


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    Sanitize text untuk dijadikan filename yang aman
    
    Args:
        text: Text input
        max_length: Maksimal panjang filename
    
    Returns:
        Sanitized filename string
    """
    # Ganti karakter special dengan underscore
    sanitized = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in text)
    # Replace multiple spaces/underscores dengan single underscore
    sanitized = re.sub(r'[_\s]+', '_', sanitized)
    # Trim dan lowercase
    sanitized = sanitized.strip('_').lower()
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_')
    
    return sanitized


def close_extra_tabs(driver: WebDriver, keep_first: bool = True) -> None:
    """
    Tutup semua tab extra, keep hanya tab pertama
    
    Args:
        driver: Selenium WebDriver instance
        keep_first: Jika True, keep tab pertama
    """
    try:
        if len(driver.window_handles) > 1:
            current_handle = driver.window_handles[0] if keep_first else None
            for handle in driver.window_handles:
                if keep_first and handle == current_handle:
                    continue
                driver.switch_to.window(handle)
                driver.close()
            
            if keep_first and current_handle:
                driver.switch_to.window(current_handle)
    except Exception as e:
        logger.warning(f"Error closing tabs: {e}")


def scroll_element(driver: WebDriver, 
                  element: WebElement, 
                  scrolls: int,
                  pause_time: float = ScraperConfig.SCROLL_PAUSE_TIME) -> bool:
    """
    Scroll element secara bertahap dengan detection end of list
    
    Args:
        driver: Selenium WebDriver instance
        element: Element yang akan di-scroll
        scrolls: Jumlah maksimal scroll
        pause_time: Jeda antar scroll
    
    Returns:
        True jika mencapai end of list, False jika tidak
    """
    for i in range(scrolls):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
        time.sleep(pause_time)
        
        # Check end of list
        try:
            end_markers = driver.find_elements(By.XPATH, ScraperConfig.SELECTORS['end_of_list'])
            if end_markers:
                logger.info(f"✅ Mencapai akhir daftar setelah {i+1} scroll")
                return True
        except Exception:
            pass
        
        if (i + 1) % 5 == 0:
            logger.info(f"Progress scroll: {i+1}/{scrolls}")
    
    return False


def format_phone_number(phone: str) -> str:
    """
    Format nomor telepon dengan standard format
    
    Args:
        phone: Raw phone number string
    
    Returns:
        Formatted phone number
    """
    if not phone:
        return ""
    
    # Remove common prefixes and clean
    phone = phone.strip()
    
    # Basic cleaning - hanya ambil digits, +, dan spaces
    phone = re.sub(r'[^\d+\s()-]', '', phone)
    
    return phone.strip()


def validate_data(data: Dict[str, str], mode: str = 'MODERATE') -> Tuple[bool, str]:
    """
    Validasi data berdasarkan validation mode
    
    Args:
        data: Dictionary data yang akan divalidasi
        mode: Validation mode ('STRICT', 'MODERATE', 'LENIENT', 'NONE')
    
    Returns:
        Tuple (is_valid, reason)
    """
    if mode not in ScraperConfig.VALIDATION_RULES:
        mode = 'MODERATE'
    
    required_fields = ScraperConfig.VALIDATION_RULES[mode]
    
    # Jika mode NONE, semua data valid
    if not required_fields:
        return True, "No validation required"
    
    # Check required fields
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field] or data[field].strip() == "":
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing: {', '.join(missing_fields)}"
    
    return True, "Valid"


def truncate_fields(data: Dict[str, str]) -> Dict[str, str]:
    """
    Truncate fields yang terlalu panjang sesuai MAX_FIELD_LENGTH
    
    Args:
        data: Dictionary data
    
    Returns:
        Data dengan fields yang sudah di-truncate
    """
    truncated = {}
    for key, value in data.items():
        if key in ScraperConfig.MAX_FIELD_LENGTH:
            max_len = ScraperConfig.MAX_FIELD_LENGTH[key]
            if value and len(value) > max_len:
                truncated[key] = value[:max_len-3] + "..."
                logger.debug(f"Truncated {key}: {len(value)} → {max_len} chars")
            else:
                truncated[key] = value
        else:
            truncated[key] = value
    
    return truncated


class ProgressTracker:
    """Helper class untuk tracking progress dengan style yang konsisten"""
    
    def __init__(self, total: int, desc: str = "Progress"):
        self.total = total
        self.current = 0
        self.desc = desc
    
    def update(self, increment: int = 1, message: str = ""):
        """Update progress"""
        self.current += increment
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        status = f"[{self.current}/{self.total}] ({percentage:.1f}%)"
        
        if message:
            logger.info(f"{self.desc} {status} - {message}")
        else:
            logger.info(f"{self.desc} {status}")
    
    def complete(self, message: str = "Selesai"):
        """Mark as complete"""
        logger.info(f"✅ {self.desc} {message} - Total: {self.current}/{self.total}")


class DataStatistics:
    """Helper class untuk tracking statistics scraping"""
    
    def __init__(self):
        self.total_processed = 0
        self.total_saved = 0
        self.total_skipped = 0
        self.skip_reasons = {}
    
    def add_saved(self):
        """Increment saved counter"""
        self.total_processed += 1
        self.total_saved += 1
    
    def add_skipped(self, reason: str):
        """Increment skipped counter dengan reason"""
        self.total_processed += 1
        self.total_skipped += 1
        
        # Track skip reasons
        if reason not in self.skip_reasons:
            self.skip_reasons[reason] = 0
        self.skip_reasons[reason] += 1
    
    def get_summary(self) -> str:
        """Get summary statistics"""
        success_rate = (self.total_saved / self.total_processed * 100) if self.total_processed > 0 else 0
        
        summary = f"""
╔══════════════════════════════════════════════════════════╗
║           📊 STATISTIK SCRAPING RESULTS                  ║
╠══════════════════════════════════════════════════════════╣
║  Total Diproses    : {self.total_processed:>4} bisnis                      ║
║  ✅ Tersimpan      : {self.total_saved:>4} bisnis ({success_rate:>5.1f}%)             ║
║  ❌ Dilewati       : {self.total_skipped:>4} bisnis ({100-success_rate:>5.1f}%)             ║
╠══════════════════════════════════════════════════════════╣"""
        
        if self.skip_reasons:
            summary += "\n║  📋 Alasan Dilewati:                                     ║"
            for reason, count in sorted(self.skip_reasons.items(), key=lambda x: x[1], reverse=True):
                reason_short = reason[:40] if len(reason) > 40 else reason
                summary += f"\n║     • {reason_short:<40} : {count:>3}  ║"
        
        summary += "\n╚══════════════════════════════════════════════════════════╝"
        
        return summary

