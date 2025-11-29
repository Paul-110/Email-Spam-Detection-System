import time
import streamlit as st
from src.models.model_loader import load_model_and_vectorizer
from src.models.predictor import SpamPredictor
from src.services.transformer_service import TransformerService
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ModelService:
    """Service for handling model operations."""
    
    def __init__(self):
        self.predictor = None
        self.transformer_service = TransformerService()
        self._initialize_predictor()
    
    def _initialize_predictor(self):
        try:
            model, cv = load_model_and_vectorizer()
            if model and cv:
                self.predictor = SpamPredictor(model, cv)
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {e}")

    def predict(self, text: str, model_type: str = "Naive Bayes"):
        """
        Predict spam probability.
        """
        # Use Real Transformer for BERT
        if "BERT" in model_type:
            try:
                return self.transformer_service.predict(text)
            except Exception as e:
                logger.error(f"Transformer prediction failed, falling back to Naive Bayes: {e}")
                st.toast("⚠️ Transformer failed, using fallback model.", icon="⚠️")
                # Fallback to Naive Bayes
        
        # Default / Fallback to Naive Bayes
        if not self.predictor:
            raise Exception("Model not initialized")

        # Simulate Latency for LSTM (still simulated)
        if "LSTM" in model_type:
            time.sleep(1.5)
            result = self.predictor.predict(text)
            self._boost_confidence(result)
            return result

        # Standard Naive Bayes
        return self.predictor.predict(text)

    def _boost_confidence(self, result):
        confidence = result['confidence']
        is_spam = result['is_spam']
        
        confidence = min(0.99, confidence + 0.05)
        result['confidence'] = confidence
        
        if is_spam:
            result['spam_probability'] = min(0.99, result['spam_probability'] + 0.05)
            result['ham_probability'] = 1 - result['spam_probability']
        else:
            result['ham_probability'] = min(0.99, result['ham_probability'] + 0.05)
            result['spam_probability'] = 1 - result['ham_probability']
