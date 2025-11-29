import time
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TransformerService:
    """Service for handling HuggingFace Transformer models."""
    
    def __init__(self, model_name="mrm8488/bert-tiny-finetuned-sms-spam-detection"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self._initialized = False
        
    def load_model(self):
        """Lazy load the model and tokenizer."""
        if self._initialized:
            return

        try:
            logger.info(f"Loading Transformer model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self._initialized = True
            logger.info("Transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Transformer model: {e}")
            raise e

    def predict(self, text: str):
        """
        Predict spam probability using the Transformer model.
        """
        if not self._initialized:
            self.load_model()
            
        start_time = time.time()
        
        try:
            # Tokenize
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1).numpy()[0]
            
            # Map output (assuming model output 0=HAM, 1=SPAM or similar, need to verify for specific model)
            # For mrm8488/bert-tiny-finetuned-sms-spam-detection: Label 0 is HAM, Label 1 is SPAM
            
            ham_prob = float(probabilities[0])
            spam_prob = float(probabilities[1])
            
            is_spam = spam_prob > ham_prob
            confidence = max(spam_prob, ham_prob)
            
            processing_time = (time.time() - start_time) * 1000
            
            return {
                "is_spam": is_spam,
                "confidence": confidence,
                "spam_probability": spam_prob,
                "ham_probability": ham_prob,
                "processing_time_ms": processing_time,
                "model_version": self.model_name
            }
            
        except Exception as e:
            logger.error(f"Transformer prediction failed: {e}")
            raise e
