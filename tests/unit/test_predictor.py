"""
Unit tests for SpamPredictor.
"""

import pytest
from src.models.model_loader import model_manager
from src.models.predictor import SpamPredictor
from src.utils.exceptions import ValidationError


class TestSpamPredictor:
    """Tests for SpamPredictor class."""
    
    @pytest.fixture(scope="class")
    def predictor(self):
        """Create a predictor instance for testing."""
        model, vectorizer = model_manager.load_models()
        return SpamPredictor(model, vectorizer)
    
    def test_predict_spam(self, predictor, sample_spam_email):
        """Test prediction on spam email."""
        result = predictor.predict(sample_spam_email)
        
        assert "is_spam" in result
        assert "confidence" in result
        assert "spam_probability" in result
        assert "ham_probability" in result
        assert "processing_time_ms" in result
        assert "model_version" in result
        assert "text_stats" in result
        
        # Should detect as spam
        assert result["is_spam"] is True
        assert result["confidence"] > 0.5
    
    def test_predict_ham(self, predictor, sample_ham_email):
        """Test prediction on legitimate email."""
        result = predictor.predict(sample_ham_email)
        
        assert result["is_spam"] is False
        assert result["confidence"] > 0.5
    
    def test_predict_empty_text(self, predictor):
        """Test prediction with empty text raises ValidationError."""
        with pytest.raises(ValidationError):
            predictor.predict("")
    
    def test_predict_whitespace_only(self, predictor):
        """Test prediction with whitespace-only text raises ValidationError."""
        with pytest.raises(ValidationError):
            predictor.predict("   ")
    
    def test_predict_too_long_text(self, predictor):
        """Test prediction with text exceeding max length."""
        long_text = "spam " * 3000  # Exceeds MAX_CONTENT_LENGTH
        with pytest.raises(ValidationError):
            predictor.predict(long_text)
    
    def test_text_stats(self, predictor):
        """Test that text stats are included in result."""
        result = predictor.predict("Test email content")
        
        stats = result["text_stats"]
        assert "word_count" in stats
        assert "char_count" in stats
        assert "avg_word_length" in stats
        assert "uppercase_ratio" in stats
        
        assert stats["word_count"] == 3
        assert stats["char_count"] > 0
    
    def test_probabilities_sum_to_one(self, predictor, sample_spam_email):
        """Test that spam and ham probabilities sum to approximately 1."""
        result = predictor.predict(sample_spam_email)
        
        prob_sum = result["spam_probability"] + result["ham_probability"]
        assert abs(prob_sum - 1.0) < 0.01  # Allow small floating point error
