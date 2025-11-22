"""
Unit Tests untuk Utility Functions
===================================

Test suite untuk memastikan utility functions bekerja dengan benar.
Menggunakan pytest framework untuk testing.

Run tests:
    pytest test_utils.py -v

Install pytest:
    pip install pytest

Author: rotiawan
Date: 2025-11-22
"""

import pytest
from typing import Dict

# Import functions to test
try:
    from .utils import (
        validate_email,
        extract_email_from_text,
        extract_city_from_address,
        sanitize_filename,
        format_phone_number,
        validate_data,
        truncate_fields,
        DataStatistics
    )
    from . import constants as const
    from .config import ScraperConfig
except ImportError:
    from utils import (
        validate_email,
        extract_email_from_text,
        extract_city_from_address,
        sanitize_filename,
        format_phone_number,
        validate_data,
        truncate_fields,
        DataStatistics
    )
    import constants as const
    from config import ScraperConfig


class TestEmailValidation:
    """Test cases untuk email validation"""
    
    def test_valid_emails(self):
        """Test dengan email yang valid"""
        valid_emails = [
            "user@domain.com",
            "info@company.co.id",
            "contact@travel-agency.com",
            "support+inquiry@business.net",
            "john.doe@email.org"
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True, f"Email should be valid: {email}"
    
    def test_invalid_emails(self):
        """Test dengan email yang tidak valid"""
        invalid_emails = [
            "",  # Empty
            "not-an-email",  # No @
            "@domain.com",  # Missing local part
            "user@",  # Missing domain
            "user@domain",  # Missing TLD
            "user@example.com",  # Blacklisted domain
            "contact@sample.com",  # Blacklisted domain
            "image@photo.jpg",  # Image extension
            "a@b.c",  # Too short
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False, f"Email should be invalid: {email}"
    
    def test_email_extraction_from_text(self):
        """Test extraction email dari text"""
        # Test dengan valid email
        text1 = "Contact us at info@company.com for more information"
        assert extract_email_from_text(text1) == "info@company.com"
        
        # Test dengan multiple emails (ambil yang pertama valid)
        text2 = "Email: contact@test.com or admin@business.co.id"
        result = extract_email_from_text(text2)
        assert result in ["admin@business.co.id"]  # test.com is blacklisted
        
        # Test tanpa email
        text3 = "No email address here"
        assert extract_email_from_text(text3) is None


class TestAddressHandling:
    """Test cases untuk address handling"""
    
    def test_extract_city_from_valid_address(self):
        """Test extract city dari alamat yang valid"""
        test_cases = [
            ("Jl. Sudirman No.1, Jakarta Pusat, DKI Jakarta", "Jakarta Pusat"),
            ("Ruko Graha No.5, Bandung, Jawa Barat 40123", "Bandung"),
            ("Main Street 123, Surabaya, East Java", "Surabaya"),
        ]
        
        for address, expected_city in test_cases:
            result = extract_city_from_address(address)
            assert expected_city in result, f"Expected '{expected_city}' in '{result}'"
    
    def test_extract_city_from_invalid_address(self):
        """Test extract city dari alamat yang tidak valid"""
        # Empty address
        assert extract_city_from_address("") == ""
        
        # Address without comma
        assert extract_city_from_address("Main Street 123") == ""


class TestPhoneFormatting:
    """Test cases untuk phone number formatting"""
    
    def test_format_phone_numbers(self):
        """Test formatting nomor telepon"""
        test_cases = [
            ("+62-21-1234567", "+62-21-1234567"),
            ("Phone: (021) 1234567", "(021) 1234567"),
            "+62 812-3456-7890",  # Should keep this format
            "021 1234567",  # Indonesian format
        ]
        
        for phone in test_cases:
            result = format_phone_number(phone)
            assert result, f"Phone should not be empty: {phone}"
            # Should remove unwanted chars
            assert not any(c in result for c in [':', ';', ',', '*', '#'])
    
    def test_empty_phone(self):
        """Test dengan empty phone"""
        assert format_phone_number("") == ""
        assert format_phone_number(None) == ""


class TestFilenameHandling:
    """Test cases untuk filename sanitization"""
    
    def test_sanitize_valid_filenames(self):
        """Test sanitize filename"""
        test_cases = [
            ("Travel Agent Jakarta", "travel_agent_jakarta"),
            ("Hotel di Bali!!", "hotel_di_bali"),
            ("Restaurant#123@City", "restaurant_123_city"),
            ("Café & Bar", "caf_bar"),
        ]
        
        for input_text, expected in test_cases:
            result = sanitize_filename(input_text)
            assert result == expected, f"Expected '{expected}', got '{result}'"
    
    def test_sanitize_long_filename(self):
        """Test sanitize filename yang terlalu panjang"""
        long_text = "This is a very long filename that exceeds the maximum length limit"
        result = sanitize_filename(long_text, max_length=30)
        assert len(result) <= 30
        assert not result.endswith('_')


class TestDataValidation:
    """Test cases untuk data validation"""
    
    def setup_method(self):
        """Setup test data"""
        self.valid_data_strict = {
            const.CSV_HEADER_NAMA: "PT Test",
            const.CSV_HEADER_ALAMAT: "Jl. Test No.1",
            const.CSV_HEADER_KOTA: "Jakarta",
            const.CSV_HEADER_TELEPON: "021-1234567",
            const.CSV_HEADER_DESKRIPSI: "Test company",
            const.CSV_HEADER_WEBSITE: "https://test.com",
            const.CSV_HEADER_LOGO: "https://logo.com/test.png",
            const.CSV_HEADER_EMAIL: "info@test-company.com",
            const.CSV_HEADER_MAP_URL: "https://maps.google.com/test"
        }
        
        self.valid_data_moderate = {
            const.CSV_HEADER_NAMA: "PT Test",
            const.CSV_HEADER_WEBSITE: "https://test.com",
            const.CSV_HEADER_EMAIL: "info@test-company.com",
        }
        
        self.valid_data_lenient = {
            const.CSV_HEADER_NAMA: "PT Test",
            const.CSV_HEADER_TELEPON: "021-1234567",
        }
    
    def test_validation_strict_mode(self):
        """Test validation dengan STRICT mode"""
        is_valid, reason = validate_data(
            self.valid_data_strict,
            const.VALIDATION_MODE_STRICT
        )
        assert is_valid is True, f"Should be valid: {reason}"
        
        # Test dengan data incomplete
        incomplete_data = {const.CSV_HEADER_NAMA: "PT Test"}
        is_valid, reason = validate_data(
            incomplete_data,
            const.VALIDATION_MODE_STRICT
        )
        assert is_valid is False
        assert "Missing" in reason
    
    def test_validation_moderate_mode(self):
        """Test validation dengan MODERATE mode"""
        is_valid, reason = validate_data(
            self.valid_data_moderate,
            const.VALIDATION_MODE_MODERATE
        )
        assert is_valid is True, f"Should be valid: {reason}"
        
        # Test dengan missing email
        incomplete_data = {
            const.CSV_HEADER_NAMA: "PT Test",
            const.CSV_HEADER_WEBSITE: "https://test.com"
        }
        is_valid, reason = validate_data(
            incomplete_data,
            const.VALIDATION_MODE_MODERATE
        )
        assert is_valid is False
    
    def test_validation_lenient_mode(self):
        """Test validation dengan LENIENT mode"""
        is_valid, reason = validate_data(
            self.valid_data_lenient,
            const.VALIDATION_MODE_LENIENT
        )
        assert is_valid is True, f"Should be valid: {reason}"
    
    def test_validation_none_mode(self):
        """Test validation dengan NONE mode"""
        empty_data = {}
        is_valid, reason = validate_data(
            empty_data,
            const.VALIDATION_MODE_NONE
        )
        # NONE mode should always pass
        assert is_valid is True


class TestTruncateFields:
    """Test cases untuk field truncation"""
    
    def test_truncate_long_fields(self):
        """Test truncate fields yang terlalu panjang"""
        long_text = "A" * 300  # Exceeds MAX_LENGTH_NAMA (256)
        
        data = {
            const.CSV_HEADER_NAMA: long_text,
            const.CSV_HEADER_ALAMAT: "Normal address"
        }
        
        truncated = truncate_fields(data)
        
        # Nama should be truncated
        assert len(truncated[const.CSV_HEADER_NAMA]) <= ScraperConfig.MAX_FIELD_LENGTH[const.CSV_HEADER_NAMA]
        assert truncated[const.CSV_HEADER_NAMA].endswith("...")
        
        # Alamat should remain same
        assert truncated[const.CSV_HEADER_ALAMAT] == "Normal address"
    
    def test_truncate_normal_fields(self):
        """Test dengan fields yang normal (tidak perlu truncate)"""
        data = {
            const.CSV_HEADER_NAMA: "PT Test Company",
            const.CSV_HEADER_TELEPON: "021-1234567"
        }
        
        truncated = truncate_fields(data)
        
        # Should remain same
        assert truncated[const.CSV_HEADER_NAMA] == data[const.CSV_HEADER_NAMA]
        assert truncated[const.CSV_HEADER_TELEPON] == data[const.CSV_HEADER_TELEPON]


class TestDataStatistics:
    """Test cases untuk DataStatistics class"""
    
    def test_statistics_tracking(self):
        """Test statistics tracking"""
        stats = DataStatistics()
        
        # Initial state
        assert stats.total_processed == 0
        assert stats.total_saved == 0
        assert stats.total_skipped == 0
        
        # Add saved
        stats.add_saved()
        assert stats.total_processed == 1
        assert stats.total_saved == 1
        assert stats.total_skipped == 0
        
        # Add skipped
        stats.add_skipped("Missing email")
        assert stats.total_processed == 2
        assert stats.total_saved == 1
        assert stats.total_skipped == 1
        assert stats.skip_reasons["Missing email"] == 1
    
    def test_success_rate_calculation(self):
        """Test success rate calculation"""
        stats = DataStatistics()
        
        # Add some data
        stats.add_saved()
        stats.add_saved()
        stats.add_saved()
        stats.add_skipped("Missing email")
        
        # Should be 75% (3 out of 4)
        success_rate = stats.get_success_rate()
        assert success_rate == 75.0
    
    def test_summary_generation(self):
        """Test summary generation"""
        stats = DataStatistics()
        stats.add_saved()
        stats.add_skipped("Missing email")
        
        summary = stats.get_summary()
        
        # Should contain key information
        assert "STATISTIK" in summary
        assert "Tersimpan" in summary
        assert "Dilewati" in summary
        assert "Missing email" in summary


# ============================================================================
# Integration Tests (dapat dijalankan jika diperlukan)
# ============================================================================

class TestIntegration:
    """Integration tests - memerlukan setup yang lebih kompleks"""
    
    @pytest.mark.skip(reason="Requires WebDriver setup")
    def test_full_scraping_workflow(self):
        """
        Test full scraping workflow.
        Di-skip by default karena memerlukan WebDriver.
        """
        pass


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    # Run tests dengan pytest
    pytest.main([__file__, "-v", "--tb=short"])

