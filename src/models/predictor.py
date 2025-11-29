"""
Spam prediction logic for email classification.

Handles the prediction pipeline using the loaded models.
"""

import time
import numpy as np
from typing import Dict

from src.utils.logger import get_logger
from src.utils.exceptions import PredictionError, ValidationError
from src.preprocessing.text_processor import text_processor
from src.config.settings import settings


logger = get_logger(__name__)


class SpamPredictor:
    """Spam email predictor using ML models."""
    
    def __init__(self, model, vectorizer):
        """
        Initialize the predictor.
        
        Args:
            model: Trained classification model
            vectorizer: Text vectorizer
        """
        self.model = model
        self.vectorizer = vectorizer
        logger.info("SpamPredictor initialized")
    
    def predict(self, text: str) -> Dict:
        """
        Predict if an email is spam or not.
        
        Args:
            text: Email text to classify
        
        Returns:
            Dictionary with prediction results
        
        Raises:
            ValidationError: If input is invalid
            PredictionError: If prediction fails
        """
        start_time = time.time()
        
        try:
            # Validate input
            text_processor.validate_input(text, settings.MAX_CONTENT_LENGTH)
            
            # Preprocess text
            processed_text = text_processor.clean_text(text)
            logger.debug(f"Preprocessed text: {processed_text[:100]}...")
            
            # Vectorize
            vectorized = self.vectorizer.transform([processed_text]).toarray()
            logger.debug(f"Vectorized shape: {vectorized.shape}")
            
            # Predict
            prediction = self.model.predict(vectorized)[0]
            probabilities = self.model.predict_proba(vectorized)[0]
            
            # Calculate metrics
            is_spam = bool(prediction)
            confidence = float(np.max(probabilities))
            
            if len(probabilities) >= 2:
                spam_prob = float(probabilities[1])
                ham_prob = float(probabilities[0])
            else:
                # Handle edge case where model returns single probability
                logger.warning(f"Model returned single probability: {probabilities}")
                if is_spam:
                    spam_prob = confidence
                    ham_prob = 1.0 - confidence
                else:
                    ham_prob = confidence
                    spam_prob = 1.0 - confidence
            
            processing_time = (time.time() - start_time) * 1000
            
            result = {
                "is_spam": is_spam,
                "confidence": confidence,
                "spam_probability": spam_prob,
                "ham_probability": ham_prob,
                "processing_time_ms": processing_time,
                "model_version": settings.MODEL_VERSION,
                "text_stats": text_processor.get_text_stats(text)
            }
            
            logger.info(f"Prediction: {'SPAM' if is_spam else 'HAM'} (confidence: {confidence:.2%}, time: {processing_time:.1f}ms)")
            return result
            
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            raise ValidationError(str(e))
        
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}", exc_info=True)
            raise PredictionError(f"Failed to classify email: {str(e)}")
    
    def predict_batch(self, texts: list) -> list:
        """
        Predict multiple emails at once.
        
        Args:
            texts: List of email texts
        
        Returns:
            List of prediction results
        """
        logger.info(f"Batch prediction for {len(texts)} emails")
        return [self.predict(text) for text in texts]
