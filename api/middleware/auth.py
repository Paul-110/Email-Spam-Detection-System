"""
Authentication middleware for the API.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from src.config.settings import settings
import os

# Define API Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validate API Key.
    
    Args:
        api_key_header: The API key from the request header.
        
    Returns:
        The valid API key.
        
    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    # Get API key from settings or env
    valid_api_key = os.getenv("API_KEY", "default-dev-key")
    
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key header (X-API-Key)",
        )
        
    if api_key_header != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )
        
    return api_key_header
