"""
Request models for the Email Spam Classifier API.

Defines Pydantic models for validating incoming requests.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional


class ClassifyRequest(BaseModel):
    """Request model for single email classification."""
    
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Email text to classify",
        example="Congratulations! You've won $1,000,000!"
    )
    
    @validator('text')
    def validate_text(cls, v):
        """Validate email text."""
        if not v or not v.strip():
            raise ValueError("Email text cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "URGENT: Your account has been suspended! Click here to verify."
            }
        }


class EmailItem(BaseModel):
    """Single email item for batch processing."""
    
    id: str = Field(
        ...,
        description="Unique identifier for the email",
        example="email_001"
    )
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Email text to classify"
    )


class BatchClassifyRequest(BaseModel):
    """Request model for batch email classification."""
    
    emails: List[EmailItem] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="List of emails to classify"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "emails": [
                    {
                        "id": "email_001",
                        "text": "Meeting tomorrow at 3pm"
                    },
                    {
                        "id": "email_002",
                        "text": "WIN FREE MONEY NOW!!!"
                    }
                ]
            }
        }
