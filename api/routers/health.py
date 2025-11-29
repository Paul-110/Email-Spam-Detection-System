"""
Health check and information endpoints.

Provides system health status and API information.
"""

from fastapi import APIRouter
from datetime import datetime

from api.models.responses import HealthResponse, InfoResponse
from src.config.settings import settings
from src.models.model_loader import model_manager
from src.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Create router
router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the API is running and healthy"
)
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        HealthResponse with status and timestamp
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@router.get(
    "/api/v1/info",
    response_model=InfoResponse,
    summary="API information",
    description="Get information about the API and loaded models"
)
async def get_info():
    """
    Get API and model information.
    
    Returns:
        InfoResponse with API details
    """
    model_info = model_manager.get_model_info()
    
    return InfoResponse(
        api_version="1.0.0",
        app_name=settings.APP_NAME,
        model_version=settings.MODEL_VERSION,
        model_loaded=model_info['model_loaded'] and model_info['vectorizer_loaded'],
        supported_features=["single", "batch"]
    )
