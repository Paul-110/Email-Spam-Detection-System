"""
Integration tests for API classification endpoints.
"""

import pytest
from httpx import AsyncClient
from api.main import app


@pytest.mark.asyncio
class TestClassifyEndpoints:
    """Integration tests for classification endpoints."""
    
    async def test_classify_spam_email(self):
        """Test classifying spam email via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/classify",
                json={"text": "WIN FREE MONEY NOW!!! Click here!!!"}
            )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "is_spam" in data
        assert "confidence" in data
        assert data["is_spam"] is True
    
    async def test_classify_ham_email(self):
        """Test classifying legitimate email via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/classify",
                json={"text": "Meeting tomorrow at 3pm in the conference room"}
            )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_spam"] is False
    
    async def test_classify_empty_text(self):
        """Test that empty text returns validation error."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/classify",
                json={"text": ""}
            )
        
        assert response.status_code == 422
    
    async def test_classify_missing_text(self):
        """Test that missing text field returns error."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/classify",
                json={}
            )
        
        assert response.status_code == 422
    
    async def test_batch_classify(self):
        """Test batch classification endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/classify/batch",
                json={
                    "emails": [
                        {"id": "1", "text": "Meeting tomorrow"},
                        {"id": "2", "text": "WIN FREE MONEY!!!"}
                    ]
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        assert "total_processed" in data
        assert len(data["results"]) == 2
        assert data["total_processed"] == 2
    
    async def test_batch_classify_empty_list(self):
        """Test batch classification with empty list."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/classify/batch",
                json={"emails": []}
            )
        
        assert response.status_code == 422
