# Use Python 3.9 slim image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-api.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-api.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose ports
# 8501 for Streamlit
# 8000 for FastAPI
EXPOSE 8501 8000

# Default command (can be overridden in docker-compose)
CMD ["python", "run_api.py"]
