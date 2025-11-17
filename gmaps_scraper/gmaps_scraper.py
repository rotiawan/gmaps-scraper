"""
Google Maps Lead Scraper - Improved Version v18
================================================
Scraper untuk mengambil data travel agent dari Google Maps
dengan fitur email extraction dari website.

Features:
- ✅ Logging system yang proper
- ✅ Configuration management
- ✅ Retry mechanism dengan exponential backoff
- ✅ Progress tracking yang informatif
- ✅ Helper functions untuk reduce duplication
- ✅ Better error handling
- ✅ Email validation yang robust
- ✅ Type hints untuk code quality
- ✅ Graceful shutdown handler

Author: Improved Version
Date: 2025-11-17
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

# Import custom modules
from config import ScraperConfig
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
        logging.FileHandler('scraper.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Global variable untuk graceful shutdown
shutdown_requested = False


def signal_handler(signum, frame):
    """Handler untuk graceful shutdown saat Ctrl+C"""
    global shutdown_requested
    logger.warning("\n⚠️  Shutdown request diterima. Menyelesaikan proses...")
    shutdown_requested = True


# Register signal handler
signal.signal(signal.SIGINT, signal_handler)


class EmailFinder:
    """Class untuk mencari email di website dengan berbagai metode"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.original_timeout = driver.timeouts.page_load
    
    def find_email_on_website(self, website_url: str) -> str:
        """
        Mencari email di website menggunakan multiple methods
        
        Args:
            website_url: URL website yang akan di-scan
        
        Returns:
            Email address jika ditemukan, empty string jika tidak
        """
        email = ""
        original_window = self.driver.current_window_handle
        
        try:
            # Set timeout pendek untuk anti-stuck
            self.driver.set_page_load_timeout(ScraperConfig.EMAIL_PAGE_LOAD_TIMEOUT)
            
            # Buka di tab baru
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            logger.debug(f"   → Scanning website: {website_url}")
            self.driver.get(website_url)
            
            # Wait for body
            WebDriverWait(self.driver, ScraperConfig.EMAIL_BODY_WAIT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Method 1: Cari mailto: links (paling akurat)
            email = self._find_by_mailto()
            
            # Method 2: Cari dengan regex di page source
            if not email:
                email = self._find_by_regex()
            
            # Method 3: Cari di visible text elements
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
        """Cari email melalui mailto: links"""
        try:
            mailto_links = self.driver.find_elements(
                By.XPATH, 
                ScraperConfig.SELECTORS['mailto_links']
            )
            if mailto_links:
                href = mailto_links[0].get_attribute('href')
                email = href.replace('mailto:', '').split('?')[0].strip()
                if validate_email(email):
                    logger.debug(f"   ✅ Email found via mailto: {email}")
                    return email
        except Exception as e:
            logger.debug(f"   Mailto method error: {e}")
        return ""
    
    def _find_by_regex(self) -> str:
        """Cari email dengan regex di page source"""
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
        """Cari email di visible text elements (footer, contact section, etc)"""
        try:
            # Cari di common elements yang biasa contain email
            selectors = [
                "//footer",
                "//*[contains(@class, 'contact')]",
                "//*[contains(@class, 'footer')]",
                "//*[contains(@id, 'contact')]",
                "//*[contains(@id, 'footer')]"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements[:3]:  # Limit to first 3 matches
                    text = element.text.lower()
                    email = extract_email_from_text(text)
                    if email:
                        logger.debug(f"   ✅ Email found in visible element: {email}")
                        return email
        except Exception as e:
            logger.debug(f"   Visible elements method error: {e}")
        return ""


class GoogleMapsScraper:
    """Main scraper class untuk Google Maps"""
    
    def __init__(self, headless: bool = False):
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.email_finder: Optional[EmailFinder] = None
        self.headless = headless
        
    def setup_driver(self) -> None:
        """Setup Selenium WebDriver dengan configuration"""
        logger.info("🔧 Setup Selenium WebDriver...")
        
        try:
            service = Service(ChromeDriverManager().install())
            options = ScraperConfig.get_chrome_options()
            
            if self.headless:
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(ScraperConfig.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(ScraperConfig.IMPLICIT_WAIT)
            
            self.wait = WebDriverWait(self.driver, ScraperConfig.EXPLICIT_WAIT)
            self.email_finder = EmailFinder(self.driver)
            
            logger.info("✅ WebDriver berhasil di-setup")
        except Exception as e:
            logger.error(f"❌ Gagal setup WebDriver: {e}")
            raise
    
    @retry_on_failure(max_retries=2, delay=3)
    def search_google_maps(self, query: str) -> None:
        """Buka Google Maps dan lakukan pencarian"""
        logger.info(f"🔎 Mencari: '{query}'")
        
        self.driver.get("https://www.google.com/maps")
        
        search_box = self.wait.until(
            EC.element_to_be_clickable(ScraperConfig.SELECTORS['search_box'])
        )
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
        
        time.sleep(ScraperConfig.AFTER_SEARCH_DELAY)
        logger.info("✅ Pencarian berhasil")
    
    def collect_links(self, max_scrolls: int) -> List[str]:
        """
        Scroll hasil dan kumpulkan semua link unik
        
        Args:
            max_scrolls: Maksimal jumlah scroll
        
        Returns:
            List of unique URLs
        """
        logger.info("📜 Memulai scrolling untuk mengumpulkan link...")
        
        scrollable_div = self.wait.until(
            EC.presence_of_element_located((By.XPATH, ScraperConfig.SELECTORS['feed']))
        )
        
        # Scroll dengan helper function
        reached_end = scroll_element(
            self.driver, 
            scrollable_div, 
            max_scrolls,
            ScraperConfig.SCROLL_PAUSE_TIME
        )
        
        if not reached_end:
            logger.info(f"⚠️  Scroll selesai tanpa mencapai akhir daftar (max: {max_scrolls})")
        
        # Kumpulkan links
        logger.info("🔗 Mengumpulkan link hasil...")
        result_links = self.driver.find_elements(
            By.CSS_SELECTOR, 
            ScraperConfig.SELECTORS['result_links']
        )
        
        links = [
            link.get_attribute('href') 
            for link in result_links 
            if link.get_attribute('href')
        ]
        
        # Deduplicate sambil preserve order
        unique_links = list(dict.fromkeys(links))
        logger.info(f"✅ Total {len(unique_links)} link unik ditemukan")
        
        return unique_links
    
    def scrape_detail_page(self, url: str) -> Dict[str, str]:
        """
        Scrape detail dari satu halaman bisnis
        
        Args:
            url: URL halaman detail
        
        Returns:
            Dictionary berisi data yang di-scrape
        """
        data = {
            'namaTravel': '',
            'alamat': '',
            'kota': '',
            'telepon': '',
            'deskripsi': '',
            'websiteUrl': '',
            'logoUrl': '',
            'email': '',
            'mapUrl': url
        }
        
        try:
            self.driver.get(url)
            time.sleep(ScraperConfig.DETAIL_PAGE_DELAY)
            
            # Scrape dengan helper function
            data['namaTravel'] = safe_find_element(
                self.driver, By.XPATH, ScraperConfig.SELECTORS['name']
            )
            
            # Alamat
            address_raw = safe_find_element(
                self.driver, By.XPATH, ScraperConfig.SELECTORS['address'],
                attribute='aria-label'
            )
            if address_raw and ':' in address_raw:
                data['alamat'] = address_raw.split(':', 1)[1].strip()
            
            # Kota (extract dari alamat)
            if data['alamat']:
                data['kota'] = extract_city_from_address(data['alamat'])
            
            # Telepon
            phone_raw = safe_find_element(
                self.driver, By.XPATH, ScraperConfig.SELECTORS['phone'],
                attribute='aria-label'
            )
            if phone_raw and ':' in phone_raw:
                data['telepon'] = format_phone_number(phone_raw.split(':', 1)[1])
            
            # Kategori/Deskripsi - coba multiple selectors
            data['deskripsi'] = safe_find_element(
                self.driver, By.XPATH, ScraperConfig.SELECTORS['category']
            )
            
            # Website URL
            data['websiteUrl'] = safe_find_element(
                self.driver, By.XPATH, ScraperConfig.SELECTORS['website'],
                attribute='href'
            )
            
            # Logo/Image
            data['logoUrl'] = safe_find_element(
                self.driver, By.XPATH, ScraperConfig.SELECTORS['logo'],
                attribute='src'
            )
            
            # Email (hanya jika ada website)
            if data['websiteUrl'] and self.email_finder:
                data['email'] = self.email_finder.find_email_on_website(data['websiteUrl'])
            
        except Exception as e:
            logger.warning(f"⚠️  Error scraping {url}: {str(e)[:100]}")
        
        return data
    
    def scrape_all(self, links: List[str], output_file: str) -> Tuple[int, DataStatistics]:
        """
        Scrape semua links dan simpan ke CSV (dengan validation)
        
        Args:
            links: List of URLs untuk di-scrape
            output_file: Path file output CSV
        
        Returns:
            Tuple (success_count, statistics)
        """
        logger.info(f"💾 Membuka file output: {output_file}")
        logger.info(f"🔍 Validation Mode: {ScraperConfig.VALIDATION_MODE}")
        
        # Show required fields
        required = ScraperConfig.VALIDATION_RULES[ScraperConfig.VALIDATION_MODE]
        if required:
            logger.info(f"📋 Required Fields: {', '.join(required)}")
        else:
            logger.info(f"📋 No validation - semua data akan disimpan")
        
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
                    email_status = f"✉️ {data['email'][:30]}" if data['email'] else "❌"
                    name_display = data['namaTravel'][:35] if data['namaTravel'] else "No name"
                    tracker.update(1, f"✅ {name_display} | {email_status}")
                    
                    # Flush every 10 rows
                    if stats.total_saved % 10 == 0:
                        f.flush()
                else:
                    # Skip data
                    stats.add_skipped(reason)
                    
                    # Log skip
                    name_display = data['namaTravel'][:35] if data['namaTravel'] else "No name"
                    logger.warning(f"   ⏭️  SKIP: {name_display} - {reason}")
        
        tracker.complete(f"Processing selesai")
        return stats.total_saved, stats
    
    def run(self, query: str, max_scrolls: int) -> Tuple[str, int, DataStatistics]:
        """
        Main method untuk menjalankan scraper
        
        Args:
            query: Search query
            max_scrolls: Maksimal scroll
        
        Returns:
            Tuple (output_filename, success_count, statistics)
        """
        stats = DataStatistics()
        
        try:
            self.setup_driver()
            self.search_google_maps(query)
            links = self.collect_links(max_scrolls)
            
            if not links:
                logger.error("❌ Tidak ada link ditemukan. Proses berhenti.")
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
        """Cleanup resources"""
        if self.driver:
            try:
                close_extra_tabs(self.driver)
                self.driver.quit()
                logger.info("✨ Browser ditutup, cleanup selesai")
            except Exception as e:
                logger.warning(f"Warning saat cleanup: {e}")


def main():
    """Main entry point"""
    print("=" * 70)
    print("🗺️  GOOGLE MAPS LEAD SCRAPER - IMPROVED VERSION v18")
    print("=" * 70)
    print()
    
    # User input
    search_query = input("📍 Masukkan kata kunci pencarian (contoh: 'travel agent di Jakarta'): ").strip()
    
    if not search_query:
        print("❌ Query pencarian tidak boleh kosong!")
        return
    
    # Max scrolls input
    while True:
        try:
            max_scrolls_str = input(f"📜 Maksimal scroll (default: {ScraperConfig.DEFAULT_MAX_SCROLLS}, Enter = default): ").strip()
            if not max_scrolls_str:
                max_scrolls = ScraperConfig.DEFAULT_MAX_SCROLLS
                break
            max_scrolls = int(max_scrolls_str)
            if max_scrolls < 1:
                print("⚠️  Minimal scroll adalah 1")
                continue
            break
        except ValueError:
            print("❌ Input tidak valid, masukkan angka!")
    
    # Validation mode selection
    print()
    print("🔍 Pilih Data Validation Mode:")
    print("   1. STRICT   - Semua field wajib terisi (~10-20% data tersimpan)")
    print("   2. MODERATE - Minimal: nama, website, email (~20-30% data tersimpan) [RECOMMENDED]")
    print("   3. LENIENT  - Minimal: nama, telepon (~80-90% data tersimpan)")
    print("   4. NONE     - Simpan semua data tanpa filter (~100% data tersimpan)")
    
    while True:
        mode_input = input(f"Pilih mode (1-4, default: 2): ").strip()
        if not mode_input:
            ScraperConfig.VALIDATION_MODE = 'MODERATE'
            break
        if mode_input == '1':
            ScraperConfig.VALIDATION_MODE = 'STRICT'
            break
        elif mode_input == '2':
            ScraperConfig.VALIDATION_MODE = 'MODERATE'
            break
        elif mode_input == '3':
            ScraperConfig.VALIDATION_MODE = 'LENIENT'
            break
        elif mode_input == '4':
            ScraperConfig.VALIDATION_MODE = 'NONE'
            break
        else:
            print("❌ Pilihan tidak valid!")
    
    print(f"✅ Mode dipilih: {ScraperConfig.VALIDATION_MODE}")
    
    # Headless option
    headless_input = input("🔇 Jalankan headless mode? (y/n, default: n): ").strip().lower()
    headless = headless_input == 'y'
    
    print()
    print("🚀 Memulai scraping...")
    print("=" * 70)
    print()
    
    # Run scraper
    scraper = GoogleMapsScraper(headless=headless)
    output_file, success_count, stats = scraper.run(search_query, max_scrolls)
    
    # Final report
    print()
    print("=" * 70)
    if output_file and success_count > 0:
        print(f"🎉 SELESAI! Data berhasil disimpan:")
        print(f"   📁 File: {output_file}")
        print()
        # Show detailed statistics
        print(stats.get_summary())
    else:
        print("❌ Scraping gagal atau tidak ada data.")
        if stats.total_processed > 0:
            print()
            print(stats.get_summary())
    print("=" * 70)


if __name__ == "__main__":
    main()
