"""
Response models for the Email Spam Classifier API.

Defines Pydantic models for API responses.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


class TextStats(BaseModel):
    """Text statistics for an email."""
    
    word_count: int = Field(..., description="Number of words")
    char_count: int = Field(..., description="Number of characters")
    avg_word_length: float = Field(..., description="Average word length")
    uppercase_ratio: float = Field(..., description="Percentage of uppercase characters")


class ClassificationResult(BaseModel):
    """Result of email classification."""
    
    is_spam: bool = Field(..., description="Whether the email is spam")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence (0-1)")
    spam_probability: float = Field(..., ge=0, le=1, description="Probability of being spam")
    ham_probability: float = Field(..., ge=0, le=1, description="Probability of being legitimate")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    model_version: str = Field(..., description="Version of the model used")
    text_stats: TextStats = Field(..., description="Statistics about the email text")
    
    model_config = {
        "protected_namespaces": (),  # Disable protected namespace warnings
        "json_schema_extra": {
            "example": {
                "is_spam": True,
                "confidence": 0.95,
                "spam_probability": 0.95,
                "ham_probability": 0.05,
                "processing_time_ms": 12.5,
                "model_version": "1.0",
                "text_stats": {
                    "word_count": 50,
                    "char_count": 250,
                    "avg_word_length": 5.0,
                    "uppercase_ratio": 15.2
                }
            }
        }
    }


class BatchClassificationItem(BaseModel):
    """Single item in batch classification response."""
    
    id: str = Field(..., description="Email identifier")
    result: ClassificationResult = Field(..., description="Classification result")


class BatchClassificationResponse(BaseModel):
    """Response for batch classification."""
    
    results: List[BatchClassificationItem] = Field(..., description="Classification results")
    total_processed: int = Field(..., description="Number of emails processed")
    processing_time_ms: float = Field(..., description="Total processing time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "id": "email_001",
                        "result": {
                            "is_spam": False,
                            "confidence": 0.92,
                            "spam_probability": 0.08,
                            "ham_probability": 0.92,
                            "processing_time_ms": 10.2,
                            "model_version": "1.0",
                            "text_stats": {
                                "word_count": 30,
                                "char_count": 150,
                                "avg_word_length": 5.0,
                                "uppercase_ratio": 2.0
                            }
                        }
                    }
                ],
                "total_processed": 1,
                "processing_time_ms": 15.5
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Current timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-11-28T20:52:00Z"
            }
        }


class InfoResponse(BaseModel):
    """API information response."""
    
    api_version: str = Field(..., description="API version")
    app_name: str = Field(..., description="Application name")
    model_version: str = Field(..., description="Model version")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    supported_features: List[str] = Field(..., description="Supported features")
    
    model_config = {
        "protected_namespaces": (),  # Disable protected namespace warnings
        "json_schema_extra": {
            "example": {
                "api_version": "1.0.0",
                "app_name": "Email Spam Classifier",
                "model_version": "1.0",
                "model_loaded": True,
                "supported_features": ["single", "batch"]
            }
        }
    }


class ErrorResponse(BaseModel):
    """Error response."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Dict[str, Any] = Field(default={}, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Email text cannot be empty",
                "details": {}
            }
        }
