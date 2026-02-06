"""
Custom Exceptions Module
=========================

Custom exception classes untuk better error handling dan debugging.
Mengikuti best practices dengan specific exception types.

Author: rotiawan
Date: 2025-11-22
"""


class ScraperBaseException(Exception):
    """
    Base exception untuk semua scraper exceptions.
    Semua custom exceptions harus inherit dari class ini.
    """
    
    def __init__(self, message: str, details: str = None):
        """
        Initialize base exception.
        
        Args:
            message: Error message utama
            details: Detail tambahan (optional)
        """
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """String representation dari exception"""
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class WebDriverSetupError(ScraperBaseException):
    """Exception untuk error saat setup WebDriver"""
    
    def __init__(self, message: str = "Failed to setup WebDriver", details: str = None):
        super().__init__(message, details)


class SearchError(ScraperBaseException):
    """Exception untuk error saat melakukan search di Google Maps"""
    
    def __init__(self, query: str, details: str = None):
        message = f"Failed to search for query: '{query}'"
        super().__init__(message, details)


class NoResultsFoundError(ScraperBaseException):
    """Exception ketika tidak ada hasil ditemukan"""
    
    def __init__(self, query: str = None):
        if query:
            message = f"No results found for query: '{query}'"
        else:
            message = "No results found"
        super().__init__(message)


class ScrapeError(ScraperBaseException):
    """Exception untuk error saat scraping data"""
    
    def __init__(self, url: str, details: str = None):
        message = f"Failed to scrape data from: {url}"
        super().__init__(message, details)


class EmailExtractionError(ScraperBaseException):
    """Exception untuk error saat extract email dari website"""
    
    def __init__(self, url: str, details: str = None):
        message = f"Failed to extract email from: {url}"
        super().__init__(message, details)


class ValidationError(ScraperBaseException):
    """Exception untuk error validasi data"""
    
    def __init__(self, field: str, reason: str = None):
        message = f"Validation failed for field: '{field}'"
        super().__init__(message, reason)


class ConfigurationError(ScraperBaseException):
    """Exception untuk error konfigurasi"""
    
    def __init__(self, message: str, details: str = None):
        super().__init__(f"Configuration error: {message}", details)


class FileOperationError(ScraperBaseException):
    """Exception untuk error operasi file (read/write)"""
    
    def __init__(self, filepath: str, operation: str, details: str = None):
        message = f"Failed to {operation} file: {filepath}"
        super().__init__(message, details)


class TimeoutError(ScraperBaseException):
    """Exception untuk timeout operations"""
    
    def __init__(self, operation: str, timeout: int, details: str = None):
        message = f"Operation '{operation}' timed out after {timeout} seconds"
        super().__init__(message, details)


class InvalidInputError(ScraperBaseException):
    """Exception untuk invalid user input"""
    
    def __init__(self, input_name: str, value: str, reason: str = None):
        message = f"Invalid input for '{input_name}': {value}"
        super().__init__(message, reason)


# ============================================================================
# Exception Handler Decorator
# ============================================================================

def handle_scraper_exception(default_return=None, log_error=True):
    """
    Decorator untuk handle scraper exceptions secara graceful.
    
    Args:
        default_return: Value yang akan di-return jika exception terjadi
        log_error: Apakah error perlu di-log
    
    Example:
        @handle_scraper_exception(default_return="")
        def get_data():
            # ... code that might raise exception
            pass
    """
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ScraperBaseException as e:
                if log_error:
                    import logging
                    logger = logging.getLogger(func.__module__)
                    logger.error(f"ScraperException in {func.__name__}: {e}")
                return default_return
            except Exception as e:
                if log_error:
                    import logging
                    logger = logging.getLogger(func.__module__)
                    logger.error(
                        f"Unexpected error in {func.__name__}: {e}",
                        exc_info=True
                    )
                return default_return
        return wrapper
    return decorator


