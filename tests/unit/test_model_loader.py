"""
Unit tests for ModelManager.
"""

import pytest
from src.models.model_loader import ModelManager, model_manager


class TestModelManager:
    """Tests for ModelManager class."""
    
    def test_singleton_pattern(self):
        """Test that ModelManager implements singleton pattern."""
        manager1 = ModelManager()
        manager2 = ModelManager()
        assert manager1 is manager2
    
    def test_load_models_success(self):
        """Test successful model loading."""
        model, vectorizer = model_manager.load_models()
        assert model is not None
        assert vectorizer is not None
    
    def test_load_models_cached(self):
        """Test that models are cached after first load."""
        # Load first time
        model1, vectorizer1 = model_manager.load_models()
        
        # Load second time (should return cached)
        model2, vectorizer2 = model_manager.load_models()
        
        assert model1 is model2
        assert vectorizer1 is vectorizer2
    
    def test_get_model_info(self):
        """Test getting model information."""
        info = model_manager.get_model_info()
        
        assert "model_loaded" in info
        assert "vectorizer_loaded" in info
        assert "model_path" in info
        assert "vectorizer_path" in info
        assert "model_version" in info
    
    def test_model_info_after_loading(self):
        """Test model info shows loaded status after loading."""
        model_manager.load_models()
        info = model_manager.get_model_info()
        
        assert info["model_loaded"] is True
        assert info["vectorizer_loaded"] is True
