# Email Spam Classifier API - Quick Start Guide

## 🚀 Running the API

### Option 1: Using the run script
```bash
python run_api.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API Documentation

After starting the server, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔗 Endpoints

### Classification
- `POST /api/v1/classify` - Classify a single email
- `POST /api/v1/classify/batch` - Classify multiple emails

### Health & Info
- `GET /health` - Health check
- `GET /api/v1/info` - API information

## 💡 Example Usage

### cURL
```bash
# Classify an email
curl -X POST "http://localhost:8000/api/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations! You won $1,000,000!"}'

# Health check
curl "http://localhost:8000/health"
```

### Python
```python
import requests

# Classify email
response = requests.post(
    "http://localhost:8000/api/v1/classify",
    json={"text": "Your email content here"}
)
result = response.json()
print(f"Is spam: {result['is_spam']}")
print(f"Confidence: {result['confidence']}")
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/api/v1/classify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Email content here' })
});

const result = await response.json();
console.log('Is spam:', result.is_spam);
```

## 📦 Installing API Dependencies

```bash
pip install -r requirements-api.txt
```

## 🛠️ Configuration

The API uses the same configuration as the Streamlit app from `src/config/settings.py`.

You can set environment variables in `.env` file or via system environment.

## 📝 Logs

API logs are written to: `logs/app.log`

## 🔒 Security Features

- Input validation with Pydantic
- Request size limits
- CORS configuration
- Error message sanitization

## ⚡ Performance

- Async request handling
- Model caching
- Efficient batch processing
