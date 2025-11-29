"""
Model loading and management for the Email Spam Classifier.

Handles loading, caching, and validation of ML models.
"""

import pickle
import hashlib
from pathlib import Path
from typing import Tuple, Optional

from src.utils.logger import get_logger
from src.utils.exceptions import ModelLoadError
from src.config.settings import settings


logger = get_logger(__name__)


class ModelManager:
    """
    Singleton class for managing ML models.
    
    Handles model loading, caching, and validation.
    """
    
    _instance = None
    _model = None
    _vectorizer = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the model manager."""
        if not self._initialized:
            self._initialized = True
            logger.info("ModelManager initialized")
    
    def load_models(self) -> Tuple:
        """
        Load the spam classifier model and vectorizer.
        
        Returns:
            Tuple of (model, vectorizer)
        
        Raises:
            ModelLoadError: If models cannot be loaded
        """
        # Return cached models if already loaded
        if self._model is not None and self._vectorizer is not None:
            logger.debug("Returning cached models")
            return self._model, self._vectorizer
        
        try:
            logger.info("Loading models from disk")
            
            # Validate files exist
            if not Path(settings.MODEL_PATH).exists():
                raise ModelLoadError(f"Model file not found: {settings.MODEL_PATH}")
            
            if not Path(settings.VECTORIZER_PATH).exists():
                raise ModelLoadError(f"Vectorizer file not found: {settings.VECTORIZER_PATH}")
            
            # Load model
            logger.debug(f"Loading model from {settings.MODEL_PATH}")
            with open(settings.MODEL_PATH, 'rb') as f:
                self._model = pickle.load(f)
            
            # Load vectorizer
            logger.debug(f"Loading vectorizer from {settings.VECTORIZER_PATH}")
            with open(settings.VECTORIZER_PATH, 'rb') as f:
                self._vectorizer = pickle.load(f)
            
            # Verify models are loaded
            if self._model is None or self._vectorizer is None:
                raise ModelLoadError("Models loaded but are None")
            
            logger.info("Models loaded successfully")
            return self._model, self._vectorizer
            
        except pickle.UnpicklingError as e:
            logger.error(f"Failed to unpickle models: {str(e)}")
            raise ModelLoadError(f"Corrupted model files: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to load models: {str(e)}", exc_info=True)
            raise ModelLoadError(f"Model loading failed: {str(e)}")
    
    def get_model_info(self) -> dict:
        """
        Get information about loaded models.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_loaded": self._model is not None,
            "vectorizer_loaded": self._vectorizer is not None,
            "model_path": settings.MODEL_PATH,
            "vectorizer_path": settings.VECTORIZER_PATH,
            "model_version": settings.MODEL_VERSION
        }
    
    def reload_models(self):
        """Force reload of models from disk."""
        logger.info("Force reloading models")
        self._model = None
        self._vectorizer = None
        return self.load_models()


# Create singleton instance
model_manager = ModelManager()

def load_model_and_vectorizer():
    """Wrapper for model_manager.load_models() to maintain compatibility."""
    return model_manager.load_models()
