"""
Google Maps Lead Scraper Package
==================================

A professional web scraping tool for extracting business leads from Google Maps.

Main Features:
- Automated Google Maps search and data extraction
- Email extraction from business websites
- Multiple validation modes for data quality
- Comprehensive logging and error handling
- Progress tracking and statistics

Author: rotiawan
Version: 18.0.0
License: MIT
"""

__version__ = "18.0.0"
__author__ = "rotiawan"
__email__ = "your.email@example.com"
__license__ = "MIT"

# Import main classes untuk easy access
from .gmaps_scraper import GoogleMapsScraper, EmailFinder
from .config import ScraperConfig
from .utils import (
    retry_on_failure,
    validate_email,
    extract_email_from_text,
    ProgressTracker,
    DataStatistics
)

__all__ = [
    "GoogleMapsScraper",
    "EmailFinder",
    "ScraperConfig",
    "retry_on_failure",
    "validate_email",
    "extract_email_from_text",
    "ProgressTracker",
    "DataStatistics",
    "__version__"
]

