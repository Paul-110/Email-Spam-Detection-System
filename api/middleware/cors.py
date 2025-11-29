"""
CORS middleware configuration.

Enables Cross-Origin Resource Sharing for web clients.
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def setup_cors(app: FastAPI):
    """
    Configure CORS middleware.
    
    Args:
        app: FastAPI application instance
    """
    # Allow origins (configure based on environment)
    origins = [
        "http://localhost:3000",  # React default
        "http://localhost:8501",  # Streamlit
        "http://localhost:8000",  # API itself
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8501",
        "http://127.0.0.1:8000",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
