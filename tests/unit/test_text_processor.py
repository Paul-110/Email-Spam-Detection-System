"""
Unit tests for TextProcessor.
"""

import pytest
from src.preprocessing.text_processor import TextProcessor, text_processor


class TestTextProcessor:
    """Tests for TextProcessor class."""
    
    def test_clean_text_lowercase(self):
        """Test that text is converted to lowercase."""
        result = text_processor.clean_text("HELLO WORLD")
        assert result == "hello world"
    
    def test_clean_text_url_replacement(self):
        """Test that URLs are replaced with placeholder."""
        text = "Check this out http://example.com/spam"
        result = text_processor.clean_text(text)
        assert "http://example.com" not in result
        assert "URL" in result
    
    def test_clean_text_email_replacement(self):
        """Test that email addresses are replaced."""
        text = "Contact me at spam@example.com"
        result = text_processor.clean_text(text)
        assert "spam@example.com" not in result
        assert "EMAIL" in result
    
    def test_clean_text_phone_replacement(self):
        """Test that phone numbers are replaced."""
        text = "Call me at 555-123-4567"
        result = text_processor.clean_text(text)
        assert "555-123-4567" not in result
        assert "PHONE" in result
    
    def test_clean_text_whitespace_normalization(self):
        """Test that extra whitespace is removed."""
        text = "Hello    world   test"
        result = text_processor.clean_text(text)
        assert result == "hello world test"
    
    def test_clean_text_empty(self):
        """Test cleaning empty text."""
        result = text_processor.clean_text("")
        assert result == ""
    
    def test_validate_input_success(self):
        """Test successful input validation."""
        assert text_processor.validate_input("Valid email text") is True
    
    def test_validate_input_empty(self):
        """Test validation fails for empty text."""
        with pytest.raises(ValueError, match="cannot be empty"):
            text_processor.validate_input("")
    
    def test_validate_input_whitespace(self):
        """Test validation fails for whitespace-only text."""
        with pytest.raises(ValueError, match="cannot be empty"):
            text_processor.validate_input("   ")
    
    def test_validate_input_too_long(self):
        """Test validation fails for text exceeding max length."""
        long_text = "a" * 20000
        with pytest.raises(ValueError, match="too long"):
            text_processor.validate_input(long_text, max_length=10000)
    
    def test_validate_input_null_bytes(self):
        """Test validation fails for text with null bytes."""
        with pytest.raises(ValueError, match="invalid characters"):
            text_processor.validate_input("Hello\x00World")
    
    def test_get_text_stats(self):
        """Test getting text statistics."""
        text = "Hello World Test"
        stats = text_processor.get_text_stats(text)
        
        assert stats["word_count"] == 3
        assert stats["char_count"] == 16
        assert stats["avg_word_length"] > 0
        assert "uppercase_ratio" in stats
    
    def test_get_text_stats_empty(self):
        """Test getting stats for empty text."""
        stats = text_processor.get_text_stats("")
        
        assert stats["word_count"] == 0
        assert stats["char_count"] == 0
        assert stats["avg_word_length"] == 0
