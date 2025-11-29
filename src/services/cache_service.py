import streamlit as st
import hashlib

class CacheService:
    """Service for caching prediction results."""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def get_cached_prediction(text_hash, _model_service, text, model_type):
        """
        Cache wrapper for prediction.
        Note: We hash the text to use as a key, but pass the full text for prediction.
        We pass _model_service with underscore to prevent hashing the object itself.
        """
        return _model_service.predict(text, model_type)

    @staticmethod
    def get_prediction(model_service, text, model_type):
        """Public method to get prediction (cached or fresh)."""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return CacheService.get_cached_prediction(text_hash, model_service, text, model_type)
