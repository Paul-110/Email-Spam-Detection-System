"""
Text preprocessing for email spam classification.

Handles cleaning and normalization of email text.
"""

import re
from typing import Optional

from src.utils.logger import get_logger


logger = get_logger(__name__)


class TextProcessor:
    """Text preprocessing utilities for email classification."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize email text.
        
        Args:
            text: Raw email text
        
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Replace URLs with placeholder
            text = re.sub(r'http[s]?://\S+|www\.\S+', 'URL', text)
            
            # Replace email addresses with placeholder
            text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'EMAIL', text)
            
            # Replace phone numbers with placeholder
            text = re.sub(r'\d{10}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', 'PHONE', text)
            
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            logger.debug(f"Text cleaned: {len(text)} characters")
            return text
            
        except Exception as e:
            logger.error(f"Error cleaning text: {str(e)}")
            return text
    
    @staticmethod
    def validate_input(text: str, max_length: int = 10000) -> bool:
        """
        Validate email input text.
        
        Args:
            text: Email text to validate
            max_length: Maximum allowed length
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If validation fails
        """
        if not text or not text.strip():
            raise ValueError("Email text cannot be empty")
        
        if len(text) > max_length:
            raise ValueError(f"Email text too long (max {max_length} characters)")
        
        # Remove null bytes
        if '\x00' in text:
            raise ValueError("Email text contains invalid characters")
        
        return True
    
    @staticmethod
    def get_text_stats(text: str) -> dict:
        """
        Get statistics about the email text.
        
        Args:
            text: Email text
        
        Returns:
            Dictionary with text statistics
        """
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        
        return {
            "word_count": word_count,
            "char_count": char_count,
            "avg_word_length": char_count / word_count if word_count > 0 else 0,
            "uppercase_ratio": sum(1 for c in text if c.isupper()) / len(text) * 100 if text else 0
        }


# Create singleton instance
text_processor = TextProcessor()
