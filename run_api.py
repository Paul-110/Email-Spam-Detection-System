"""
Entry point for running the FastAPI server.

Run this script to start the Email Spam Classifier API.
"""

import uvicorn
from src.config.settings import settings


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
