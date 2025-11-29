"""
Configuration management for the Email Spam Classifier application.

Centralized configuration using environment variables and default values.
"""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application configuration settings."""
    
    # Application metadata
    APP_NAME: str = "Email Spam Classifier"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    MODEL_PATH: str = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "spam_v2.pkl"))
    VECTORIZER_PATH: str = os.getenv("VECTORIZER_PATH", str(BASE_DIR / "models" / "vectorizer_v2.pkl"))
    LOG_DIR: str = os.getenv("LOG_DIR", str(BASE_DIR / "logs"))
    
    # Model configuration
    MODEL_VERSION: str = "2.0"
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    
    # UI configuration
    PAGE_TITLE: str = "Email Spam Classifier - AI Powered"
    PAGE_ICON: str = "✨"
    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "collapsed"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Security
    API_KEY: str = os.getenv("API_KEY", "default-dev-key")
    
    # Performance
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", "10000"))
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            True if valid, raises exception otherwise
        """
        # Check if critical files exist
        model_path = Path(cls.MODEL_PATH)
        vectorizer_path = Path(cls.VECTORIZER_PATH)
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {cls.MODEL_PATH}")
        
        if not vectorizer_path.exists():
            raise FileNotFoundError(f"Vectorizer file not found: {cls.VECTORIZER_PATH}")
        
        return True
    
    @classmethod
    def get_info(cls) -> dict:
        """Get configuration information."""
        return {
            "app_name": cls.APP_NAME,
            "version": cls.APP_VERSION,
            "environment": cls.ENVIRONMENT,
            "model_path": cls.MODEL_PATH,
            "vectorizer_path": cls.VECTORIZER_PATH,
            "log_level": cls.LOG_LEVEL
        }


# Create singleton instance
settings = Settings()
