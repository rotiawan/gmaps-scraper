"""
Google Maps Lead Scraper - Refactored Version v18
==================================================

Professional scraper untuk mengambil data lead bisnis dari Google Maps
dengan fitur email extraction dari website.

Features:
- ✅ Modular architecture dengan separation of concerns
- ✅ Comprehensive logging system
- ✅ Configuration management dengan constants
- ✅ Custom exceptions untuk better error handling
- ✅ Retry mechanism dengan exponential backoff
- ✅ Progress tracking yang informatif
- ✅ Email extraction dengan 3 metode
- ✅ Data validation dengan multiple modes
- ✅ Type hints dan docstrings lengkap
- ✅ Graceful shutdown handler
- ✅ Mengikuti PEP 8 dan SOLID principles

Author: rotiawan
Date: 2025-11-22
Version: 18.0.0
"""

import csv
import time
import signal
import sys
import logging
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Import local modules
# Support both direct script execution and package import
try:
    # Try relative imports (when used as package)
    from . import constants as const
    from .config import ScraperConfig
    from .exceptions import (
        WebDriverSetupError,
        SearchError,
        NoResultsFoundError,
        ScrapeError,
        EmailExtractionError
    )
    from .utils import (
        retry_on_failure,
        safe_find_element,
        validate_email,
        extract_email_from_text,
        extract_city_from_address,
        sanitize_filename,
        close_extra_tabs,
        scroll_element,
        format_phone_number,
        validate_data,
        truncate_fields,
        ProgressTracker,
        DataStatistics
    )
except ImportError:
    # Fall back to absolute imports (when run as script)
    import constants as const
    from config import ScraperConfig
    from exceptions import (
        WebDriverSetupError,
        SearchError,
        NoResultsFoundError,
        ScrapeError,
        EmailExtractionError
    )
    from utils import (
        retry_on_failure,
        safe_find_element,
        validate_email,
        extract_email_from_text,
        extract_city_from_address,
        sanitize_filename,
        close_extra_tabs,
        scroll_element,
        format_phone_number,
        validate_data,
        truncate_fields,
        ProgressTracker,
        DataStatistics
    )

# Setup logging
logging.basicConfig(
    level=getattr(logging, ScraperConfig.LOG_LEVEL),
    format=ScraperConfig.LOG_FORMAT,
    datefmt=ScraperConfig.LOG_DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            ScraperConfig.LOG_FILE_NAME,
            encoding='utf-8',
            mode='a'
        )
    ]
)
logger = logging.getLogger(__name__)

# Global flag untuk graceful shutdown
shutdown_requested = False


def signal_handler(signum: int, frame) -> None:
    """
    Handler untuk graceful shutdown saat Ctrl+C.
    
    Args:
        signum: Signal number
        frame: Current stack frame
    """
    global shutdown_requested
    logger.warning("\n⚠️  Shutdown request diterima. Menyelesaikan proses...")
    shutdown_requested = True


# Register signal handler untuk SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)


class EmailFinder:
    """
    Class untuk mencari dan mengekstrak email dari website bisnis.
    
    Menggunakan 3 metode extraction:
    1. Mencari mailto: links (paling akurat)
    2. Regex pattern matching di page source
    3. Scanning visible elements (footer, contact section)
    
    Attributes:
        driver: Selenium WebDriver instance
        original_timeout: Original page load timeout untuk restore nanti
    """
    
    def __init__(self, driver: webdriver.Chrome):
        """
        Initialize EmailFinder.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.original_timeout = driver.timeouts.page_load
    
    def find_email_on_website(self, website_url: str) -> str:
        """
        Mencari email di website menggunakan multiple methods.
        
        Process:
        1. Buka website di tab baru (untuk isolation)
        2. Set timeout pendek (anti-stuck)
        3. Try 3 extraction methods secara berurutan
        4. Cleanup dan close tab
        
        Args:
            website_url: URL website yang akan di-scan
        
        Returns:
            Email address jika ditemukan, empty string jika tidak
        
        Note:
            Method ini akan gracefully handle timeout dan errors.
        """
        email = ""
        original_window = self.driver.current_window_handle
        
        try:
            # Set timeout pendek untuk anti-stuck
            self.driver.set_page_load_timeout(ScraperConfig.EMAIL_PAGE_LOAD_TIMEOUT)
            
            # Buka di tab baru untuk isolation
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            logger.debug(f"   → Scanning website: {website_url}")
            self.driver.get(website_url)
            
            # Wait for body element
            WebDriverWait(self.driver, ScraperConfig.EMAIL_BODY_WAIT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Method 1: Mailto links (paling akurat)
            email = self._find_by_mailto()
            
            # Method 2: Regex di page source
            if not email:
                email = self._find_by_regex()
            
            # Method 3: Visible text elements
            if not email:
                email = self._find_in_visible_elements()
            
        except TimeoutException:
            logger.debug(f"   ⏱️  Timeout saat load website: {website_url}")
            
        except WebDriverException as e:
            logger.debug(f"   ⚠️  WebDriver error: {str(e)[:100]}")
            
        except Exception as e:
            logger.debug(f"   ❌ Error scanning website: {str(e)[:100]}")
            
        finally:
            # Cleanup: restore timeout & close tab
            self.driver.set_page_load_timeout(self.original_timeout)
            try:
                self.driver.close()
                self.driver.switch_to.window(original_window)
            except Exception:
                # Fallback jika tab sudah tertutup
                if len(self.driver.window_handles) > 0:
                    self.driver.switch_to.window(self.driver.window_handles[0])
        
        return email
    
    def _find_by_mailto(self) -> str:
        """
        Method 1: Cari email via mailto: links.
        Paling akurat karena explicit email link.
        
        Returns:
            Email address atau empty string
        """
        try:
            mailto_links = self.driver.find_elements(
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_MAILTO]
            )
            
            if mailto_links:
                href = mailto_links[0].get_attribute('href')
                # Parse mailto:email@domain.com?subject=...
                email = href.replace('mailto:', '').split('?')[0].strip()
                
                if validate_email(email):
                    logger.debug(f"   ✅ Email found via mailto: {email}")
                    return email
                    
        except Exception as e:
            logger.debug(f"   Mailto method error: {e}")
        
        return ""
    
    def _find_by_regex(self) -> str:
        """
        Method 2: Cari email dengan regex pattern di page source.
        
        Returns:
            Email address atau empty string
        """
        try:
            page_source = self.driver.page_source.lower()
            email = extract_email_from_text(page_source)
            
            if email:
                logger.debug(f"   ✅ Email found via regex: {email}")
                return email
                
        except Exception as e:
            logger.debug(f"   Regex method error: {e}")
        
        return ""
    
    def _find_in_visible_elements(self) -> str:
        """
        Method 3: Cari email di visible text elements.
        Fokus ke footer, contact section, dll.
        
        Returns:
            Email address atau empty string
        """
        try:
            # Common selectors untuk email
            selectors = [
                "//footer",
                "//*[contains(@class, 'contact')]",
                "//*[contains(@class, 'footer')]",
                "//*[contains(@id, 'contact')]",
                "//*[contains(@id, 'footer')]"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                
                # Limit to first 3 matches untuk efficiency
                for element in elements[:3]:
                    text = element.text.lower()
                    email = extract_email_from_text(text)
                    
                    if email:
                        logger.debug(f"   ✅ Email found in visible element: {email}")
                        return email
                        
        except Exception as e:
            logger.debug(f"   Visible elements method error: {e}")
        
        return ""


class GoogleMapsScraper:
    """
    Main scraper class untuk Google Maps lead generation.
    
    Responsibilities:
    - Setup WebDriver
    - Search di Google Maps
    - Collect links dari hasil search
    - Scrape detail dari setiap bisnis
    - Extract email dari website (via EmailFinder)
    - Validate dan save data ke CSV
    
    Attributes:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        email_finder: EmailFinder instance
        headless: Flag untuk headless mode
    """
    
    def __init__(self, headless: bool = False):
        """
        Initialize scraper.
        
        Args:
            headless: Jika True, run browser dalam headless mode
        """
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.email_finder: Optional[EmailFinder] = None
        self.headless = headless
    
    def setup_driver(self) -> None:
        """
        Setup Selenium WebDriver dengan configuration optimal.
        
        Raises:
            WebDriverSetupError: Jika gagal setup WebDriver
        """
        logger.info("🔧 Setup Selenium WebDriver...")
        
        try:
            service = Service(ChromeDriverManager().install())
            options = ScraperConfig.get_chrome_options(headless=self.headless)
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(ScraperConfig.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(ScraperConfig.IMPLICIT_WAIT)
            
            self.wait = WebDriverWait(self.driver, ScraperConfig.EXPLICIT_WAIT)
            self.email_finder = EmailFinder(self.driver)
            
            logger.info(f"✅ {const.SUCCESS_WEBDRIVER}")
            
        except Exception as e:
            error_msg = f"{const.ERROR_WEBDRIVER_SETUP}: {e}"
            logger.error(error_msg)
            raise WebDriverSetupError(details=str(e))
    
    @retry_on_failure(max_retries=2, delay=3)
    def search_google_maps(self, query: str) -> None:
        """
        Buka Google Maps dan lakukan pencarian.
        
        Args:
            query: Search query string
        
        Raises:
            SearchError: Jika search gagal
        """
        logger.info(f"🔎 Mencari: '{query}'")
        
        try:
            self.driver.get(const.GOOGLE_MAPS_URL)
            
            # Find search box dan input query
            search_box = self.wait.until(
                EC.element_to_be_clickable(
                    ScraperConfig.SELECTORS[const.SELECTOR_ID_SEARCH_BOX]
                )
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)
            
            # Wait for results to load
            time.sleep(ScraperConfig.AFTER_SEARCH_DELAY)
            
            logger.info(f"✅ {const.SUCCESS_SEARCH}")
            
        except Exception as e:
            error_msg = f"Search failed for query '{query}': {e}"
            logger.error(error_msg)
            raise SearchError(query=query, details=str(e))
    
    def collect_links(self, max_scrolls: int) -> List[str]:
        """
        Scroll hasil pencarian dan kumpulkan semua link unik.
        
        Process:
        1. Find scrollable feed element
        2. Scroll bertahap dengan pause
        3. Detect end of list
        4. Collect unique links
        
        Args:
            max_scrolls: Maksimal jumlah scroll
        
        Returns:
            List of unique business URLs
        
        Raises:
            NoResultsFoundError: Jika tidak ada link ditemukan
        """
        logger.info(f"📜 {const.INFO_SCROLLING_START}")
        
        try:
            # Find scrollable div
            scrollable_div = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, ScraperConfig.SELECTORS[const.SELECTOR_ID_FEED])
                )
            )
            
            # Scroll dengan helper function
            reached_end = scroll_element(
                self.driver,
                scrollable_div,
                max_scrolls,
                ScraperConfig.SCROLL_PAUSE_TIME
            )
            
            if not reached_end:
                logger.info(
                    f"⚠️  Scroll selesai tanpa mencapai akhir daftar "
                    f"(max: {max_scrolls})"
                )
            
            # Collect links
            logger.info(f"🔗 {const.INFO_COLLECTING_LINKS}")
            result_links = self.driver.find_elements(
                By.CSS_SELECTOR,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_RESULT_LINKS]
            )
            
            # Extract URLs
            links = [
                link.get_attribute('href')
                for link in result_links
                if link.get_attribute('href')
            ]
            
            # Deduplicate sambil preserve order
            unique_links = list(dict.fromkeys(links))
            
            if not unique_links:
                raise NoResultsFoundError()
            
            logger.info(f"✅ Total {len(unique_links)} link unik ditemukan")
            return unique_links
            
        except NoResultsFoundError:
            raise
        except Exception as e:
            logger.error(f"Error collecting links: {e}")
            raise
    
    def scrape_detail_page(self, url: str) -> Dict[str, str]:
        """
        Scrape detail dari satu halaman bisnis.
        
        Data yang di-extract:
        - Nama bisnis
        - Alamat lengkap
        - Kota (extracted dari alamat)
        - Nomor telepon
        - Deskripsi/kategori
        - Website URL
        - Logo/image URL
        - Email (dari website jika ada)
        - Google Maps URL
        
        Args:
            url: URL halaman detail bisnis
        
        Returns:
            Dictionary berisi data yang di-scrape
        """
        data = {
            const.CSV_HEADER_NAMA: '',
            const.CSV_HEADER_ALAMAT: '',
            const.CSV_HEADER_KOTA: '',
            const.CSV_HEADER_TELEPON: '',
            const.CSV_HEADER_DESKRIPSI: '',
            const.CSV_HEADER_WEBSITE: '',
            const.CSV_HEADER_LOGO: '',
            const.CSV_HEADER_EMAIL: '',
            const.CSV_HEADER_MAP_URL: url
        }
        
        try:
            self.driver.get(url)
            time.sleep(ScraperConfig.DETAIL_PAGE_DELAY)
            
            # Nama bisnis
            data[const.CSV_HEADER_NAMA] = safe_find_element(
                self.driver,
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_NAME]
            )
            
            # Alamat
            address_raw = safe_find_element(
                self.driver,
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_ADDRESS],
                attribute='aria-label'
            )
            if address_raw and ':' in address_raw:
                data[const.CSV_HEADER_ALAMAT] = address_raw.split(':', 1)[1].strip()
            
            # Kota (extract dari alamat)
            if data[const.CSV_HEADER_ALAMAT]:
                data[const.CSV_HEADER_KOTA] = extract_city_from_address(
                    data[const.CSV_HEADER_ALAMAT]
                )
            
            # Telepon
            phone_raw = safe_find_element(
                self.driver,
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_PHONE],
                attribute='aria-label'
            )
            if phone_raw and ':' in phone_raw:
                data[const.CSV_HEADER_TELEPON] = format_phone_number(
                    phone_raw.split(':', 1)[1]
                )
            
            # Deskripsi/Kategori
            data[const.CSV_HEADER_DESKRIPSI] = safe_find_element(
                self.driver,
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_CATEGORY]
            )
            
            # Website URL
            data[const.CSV_HEADER_WEBSITE] = safe_find_element(
                self.driver,
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_WEBSITE],
                attribute='href'
            )
            
            # Logo/Image
            data[const.CSV_HEADER_LOGO] = safe_find_element(
                self.driver,
                By.XPATH,
                ScraperConfig.SELECTORS[const.SELECTOR_ID_LOGO],
                attribute='src'
            )
            
            # Email (hanya jika ada website)
            if data[const.CSV_HEADER_WEBSITE] and self.email_finder:
                try:
                    data[const.CSV_HEADER_EMAIL] = self.email_finder.find_email_on_website(
                        data[const.CSV_HEADER_WEBSITE]
                    )
                except Exception as e:
                    logger.debug(f"   Email extraction error: {e}")
            
        except Exception as e:
            logger.warning(f"⚠️  Error scraping {url}: {str(e)[:100]}")
        
        return data
    
    def scrape_all(
        self,
        links: List[str],
        output_file: str
    ) -> Tuple[int, DataStatistics]:
        """
        Scrape semua links dan simpan ke CSV dengan validation.
        
        Process:
        1. Open CSV file untuk writing
        2. Iterate semua links
        3. Scrape detail dari setiap link
        4. Truncate long fields
        5. Validate data berdasarkan mode
        6. Save jika valid, skip jika tidak
        7. Track statistics
        
        Args:
            links: List of URLs untuk di-scrape
            output_file: Path file output CSV
        
        Returns:
            Tuple (success_count: int, statistics: DataStatistics)
        """
        logger.info(f"💾 Membuka file output: {output_file}")
        logger.info(f"🔍 Validation Mode: {ScraperConfig.VALIDATION_MODE}")
        
        # Show required fields
        required = ScraperConfig.VALIDATION_RULES[ScraperConfig.VALIDATION_MODE]
        if required:
            logger.info(f"📋 Required Fields: {', '.join(required)}")
        else:
            logger.info("📋 No validation - semua data akan disimpan")
        
        stats = DataStatistics()
        tracker = ProgressTracker(len(links), "Scraping Progress")
        
        with open(output_file, 'w', newline='', encoding=ScraperConfig.CSV_ENCODING) as f:
            writer = csv.DictWriter(f, fieldnames=ScraperConfig.CSV_HEADERS)
            writer.writeheader()
            
            for i, link in enumerate(links, 1):
                # Check shutdown request
                if shutdown_requested:
                    logger.warning("⚠️  Shutdown detected. Menyimpan progress...")
                    break
                
                # Scrape data
                data = self.scrape_detail_page(link)
                
                # Truncate long fields
                data = truncate_fields(data)
                
                # Validate data
                is_valid, reason = validate_data(data, ScraperConfig.VALIDATION_MODE)
                
                if is_valid:
                    # Save to CSV
                    writer.writerow(data)
                    stats.add_saved()
                    
                    # Log progress
                    email_status = (
                        f"✉️ {data[const.CSV_HEADER_EMAIL][:30]}"
                        if data[const.CSV_HEADER_EMAIL]
                        else "❌"
                    )
                    name_display = (
                        data[const.CSV_HEADER_NAMA][:35]
                        if data[const.CSV_HEADER_NAMA]
                        else "No name"
                    )
                    tracker.update(1, f"✅ {name_display} | {email_status}")
                    
                    # Flush periodically untuk prevent data loss
                    if stats.total_saved % ScraperConfig.FLUSH_INTERVAL == 0:
                        f.flush()
                else:
                    # Skip data
                    stats.add_skipped(reason)
                    
                    # Log skip
                    name_display = (
                        data[const.CSV_HEADER_NAMA][:35]
                        if data[const.CSV_HEADER_NAMA]
                        else "No name"
                    )
                    logger.warning(f"   ⏭️  SKIP: {name_display} - {reason}")
        
        tracker.complete("Processing selesai")
        return stats.total_saved, stats
    
    def run(self, query: str, max_scrolls: int) -> Tuple[str, int, DataStatistics]:
        """
        Main method untuk menjalankan scraper end-to-end.
        
        Workflow:
        1. Setup WebDriver
        2. Search di Google Maps
        3. Collect links dari hasil
        4. Scrape detail + email
        5. Save ke CSV
        6. Return statistics
        
        Args:
            query: Search query
            max_scrolls: Maksimal scroll
        
        Returns:
            Tuple (output_filename: str, success_count: int, statistics: DataStatistics)
        """
        stats = DataStatistics()
        
        try:
            self.setup_driver()
            self.search_google_maps(query)
            links = self.collect_links(max_scrolls)
            
            if not links:
                logger.error(const.ERROR_NO_LINKS_FOUND)
                return "", 0, stats
            
            # Generate output filename
            ScraperConfig.create_output_dir()
            safe_query = sanitize_filename(query)
            timestamp = datetime.now().strftime(ScraperConfig.DATE_FORMAT)
            output_file = f"{ScraperConfig.OUTPUT_DIR}/{safe_query}_{timestamp}.csv"
            
            # Scrape all
            success_count, stats = self.scrape_all(links, output_file)
            
            return output_file, success_count, stats
            
        except Exception as e:
            logger.error(f"❌ Error fatal: {e}", exc_info=True)
            return "", 0, stats
            
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """
        Cleanup resources: close browser, tabs, etc.
        Akan dipanggil di finally block untuk ensure cleanup.
        """
        if self.driver:
            try:
                close_extra_tabs(self.driver)
                self.driver.quit()
                logger.info(f"✨ {const.SUCCESS_CLEANUP}")
            except Exception as e:
                logger.warning(f"Warning saat cleanup: {e}")


# ===========================================================================
# CLI Input Handlers
# ===========================================================================


def get_search_query_input() -> str:
    """
    Prompt user untuk memasukkan search query.

    Returns:
        Search query string, atau empty string jika tidak valid
    """
    query = input(
        "📍 Masukkan kata kunci pencarian "
        "(contoh: 'travel agent di Jakarta'): "
    ).strip()

    if not query:
        print(f"❌ {const.ERROR_EMPTY_QUERY}")
        return ""

    return query


def get_max_scrolls_input() -> int:
    """
    Prompt user untuk memasukkan jumlah maksimal scroll.

    Returns:
        Jumlah scroll (integer)
    """
    while True:
        try:
            user_input = input(
                f"📜 Maksimal scroll "
                f"(default: {ScraperConfig.DEFAULT_MAX_SCROLLS}, Enter = default): "
            ).strip()

            if not user_input:
                return ScraperConfig.DEFAULT_MAX_SCROLLS

            max_scrolls = int(user_input)
            if max_scrolls < 1:
                print(f"⚠️  {const.ERROR_INVALID_SCROLL}")
                continue

            return max_scrolls

        except ValueError:
            print(f"❌ {const.ERROR_INVALID_INPUT}")


def get_validation_mode_input() -> str:
    """
    Prompt user untuk memilih validation mode.

    Returns:
        Validation mode string (STRICT, MODERATE, LENIENT, atau NONE)
    """
    print()
    print("🔍 Pilih Data Validation Mode:")

    mode_info = ScraperConfig.get_validation_modes_info()
    for i, (mode, desc) in enumerate(mode_info.items(), 1):
        suffix = " [RECOMMENDED]" if mode == const.VALIDATION_MODE_MODERATE else ""
        print(f"   {i}. {mode:<10} - {desc}{suffix}")

    mode_mapping = {
        '1': const.VALIDATION_MODE_STRICT,
        '2': const.VALIDATION_MODE_MODERATE,
        '3': const.VALIDATION_MODE_LENIENT,
        '4': const.VALIDATION_MODE_NONE,
    }

    while True:
        user_input = input("Pilih mode (1-4, default: 2): ").strip()

        if not user_input:
            return const.VALIDATION_MODE_MODERATE

        if user_input in mode_mapping:
            return mode_mapping[user_input]

        print("❌ Pilihan tidak valid!")


def get_headless_mode_input() -> bool:
    """
    Prompt user untuk memilih headless mode.

    Returns:
        True jika headless mode dipilih, False jika tidak
    """
    user_input = input(
        "🔇 Jalankan headless mode? (y/n, default: n): "
    ).strip().lower()
    return user_input == 'y'


def print_final_report(
    output_file: str,
    success_count: int,
    stats: DataStatistics
) -> None:
    """
    Print laporan akhir hasil scraping.

    Args:
        output_file: Path ke file output CSV
        success_count: Jumlah data yang berhasil disimpan
        stats: Object DataStatistics dengan statistik lengkap
    """
    print()
    print("=" * 70)

    if output_file and success_count > 0:
        print("🎉 SELESAI! Data berhasil disimpan:")
        print(f"   📁 File: {output_file}")
        print()
        print(stats.get_summary())
    else:
        print("❌ Scraping gagal atau tidak ada data.")
        if stats.total_processed > 0:
            print()
            print(stats.get_summary())

    print("=" * 70)


# ===========================================================================
# Main Entry Point
# ===========================================================================


def main():
    """
    Main entry point untuk CLI application.
    Orchestrates user input collection dan scraping process.
    """
    print("=" * 70)
    print(f"🗺️  {const.APP_NAME.upper()} - VERSION {const.APP_VERSION}")
    print("=" * 70)
    print()

    # Collect user inputs
    search_query = get_search_query_input()
    if not search_query:
        return

    max_scrolls = get_max_scrolls_input()

    validation_mode = get_validation_mode_input()
    ScraperConfig.VALIDATION_MODE = validation_mode
    print(f"✅ Mode dipilih: {validation_mode}")

    headless = get_headless_mode_input()

    # Run scraper
    print()
    print("🚀 Memulai scraping...")
    print("=" * 70)
    print()

    scraper = GoogleMapsScraper(headless=headless)
    output_file, success_count, stats = scraper.run(search_query, max_scrolls)

    # Print final report
    print_final_report(output_file, success_count, stats)


if __name__ == "__main__":
    main()
