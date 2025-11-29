"""
Classification endpoints for the Email Spam Classifier API.

Handles single and batch email classification requests.
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from typing import List
import time
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.models.requests import ClassifyRequest, BatchClassifyRequest
from api.models.responses import (
    ClassificationResult,
    BatchClassificationResponse,
    BatchClassificationItem,
    TextStats
)
from src.models.model_loader import ModelManager
from src.models.predictor import SpamPredictor
from src.config.settings import settings
from src.utils.exceptions import ValidationError, PredictionError
from api.middleware.auth import get_api_key

# Initialize logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1",
    tags=["classification"],
    dependencies=[Depends(get_api_key)],  # Secure all endpoints in this router
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)

limiter = Limiter(key_func=get_remote_address)

def get_predictor():
    """Dependency to get initialized predictor."""
    # This ModelManager instance should ideally be a singleton or managed by FastAPI's dependency injection
    # to avoid reloading models on every request. For simplicity, we'll instantiate it here.
    # A more robust solution would involve a global instance or a custom dependency provider.
    model_manager = ModelManager()
    if model_manager.model is None or model_manager.vectorizer is None:
        logger.info("Initializing models for API request")
        try:
            model_manager.load_models()
        except Exception as e:
            logger.error(f"Failed to load ML models: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to load ML models"
            )

    # Create predictor instance
    predictor = SpamPredictor(model_manager.model, model_manager.vectorizer)
    logger.info("SpamPredictor initialized for API")
    return predictor


@router.post(
    "/classify",
    response_model=ClassificationResult,
    summary="Classify a single email",
    description="Classify an email as spam or legitimate (ham)",
    responses={
        200: {
            "description": "Successful classification",
            "content": {
                "application/json": {
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
        }
    }
)
async def classify_email(request: ClassifyRequest):
    """
    Classify a single email as spam or legitimate.
    
    Args:
        request: ClassifyRequest with email text
    
    Returns:
        ClassificationResult with prediction and metadata
    """
    try:
        logger.info(f"Classification request received (text length: {len(request.text)})")
        
        # Get predictor
        predictor = get_predictor()
        
        # Perform classification
        result = predictor.predict(request.text)
        
        # Convert to response model
        response = ClassificationResult(
            is_spam=result['is_spam'],
            confidence=result['confidence'],
            spam_probability=result['spam_probability'],
            ham_probability=result['ham_probability'],
            processing_time_ms=result['processing_time_ms'],
            model_version=result['model_version'],
            text_stats=TextStats(**result['text_stats'])
        )
        
        logger.info(f"Classification complete: {'SPAM' if result['is_spam'] else 'HAM'}")
        return response
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except PredictionError as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to classify email"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post(
    "/classify/batch",
    response_model=BatchClassificationResponse,
    summary="Classify multiple emails",
    description="Classify multiple emails in a single request",
    responses={
        200: {"description": "Successful batch classification"}
    }
)
async def classify_batch(request: BatchClassifyRequest):
    """
    Classify multiple emails at once.
    
    Args:
        request: BatchClassifyRequest with list of emails
    
    Returns:
        BatchClassificationResponse with all results
    """
    try:
        start_time = time.time()
        logger.info(f"Batch classification request received ({len(request.emails)} emails)")
        
        # Get predictor
        predictor = get_predictor()
        
        # Process each email
        results = []
        for email_item in request.emails:
            try:
                result = predictor.predict(email_item.text)
                
                classification_result = ClassificationResult(
                    is_spam=result['is_spam'],
                    confidence=result['confidence'],
                    spam_probability=result['spam_probability'],
                    ham_probability=result['ham_probability'],
                    processing_time_ms=result['processing_time_ms'],
                    model_version=result['model_version'],
                    text_stats=TextStats(**result['text_stats'])
                )
                
                results.append(BatchClassificationItem(
                    id=email_item.id,
                    result=classification_result
                ))
                
            except Exception as e:
                logger.error(f"Error processing email {email_item.id}: {str(e)}")
                # Continue processing other emails
                continue
        
        processing_time = (time.time() - start_time) * 1000
        
        response = BatchClassificationResponse(
            results=results,
            total_processed=len(results),
            processing_time_ms=processing_time
        )
        
        logger.info(f"Batch classification complete: {len(results)}/{len(request.emails)} processed")
        return response
        
    except Exception as e:
        logger.error(f"Batch classification error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process batch classification"
        )
