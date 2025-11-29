"""
Integration tests for health and info endpoints.
"""

import pytest
from httpx import AsyncClient
from api.main import app


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Integration tests for health endpoints."""
    
    async def test_health_check(self):
        """Test health check endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert data["status"] == "healthy"
    
    async def test_api_info(self):
        """Test API info endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/info")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "api_version" in data
        assert "app_name" in data
        assert "model_version" in data
        assert "model_loaded" in data
        assert "supported_features" in data
    
    async def test_root_endpoint(self):
        """Test root endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "docs" in data
