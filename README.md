<div align="center">

<img src="src/assets/sp.svg" width="120" height="120" alt="SpamShield AI Logo">

# SpamShield AI 🛡️ Email Spam Classifier

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live-Demo-orange?style=for-the-badge&logo=streamlit)](https://spamshield-ai-demo.streamlit.app/)

**SpamShield AI - AI-powered email spam classifier**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API](#-api-endpoints) • [Deployment](#-deployment)

</div>

---

## 🌟 Features

### 🧠 Advanced AI Models
- **Hybrid Architecture** - Switch between ultra-fast Naive Bayes and state-of-the-art Transformers.
- **Deep Learning** - Integrated `bert-tiny` (HuggingFace) for semantic understanding.
- **Lazy Loading** - Heavy models load only on demand to keep startup fast.
- **Model Caching** - Optimized memory usage for repeated predictions.

### 🚀 REST API
- **FastAPI Framework** - High-performance async API
- **Auto Documentation** - Swagger UI and ReDoc included
- **Request Validation** - Pydantic models
- **CORS Support** - Ready for web clients
- **Batch Processing** - Classify multiple emails at once

### 🐳 Containerization
- **Docker Support** - Fully containerized application
- **Docker Compose** - Multi-service orchestration
- **Health Checks** - Built-in container health monitoring
- **Volume Persistence** - Logs survive container restarts

### 🧪 Testing
- **Unit Tests** - Comprehensive coverage of core modules
- **Integration Tests** - API endpoint testing
- **Pytest Framework** - Industry-standard testing
- **Coverage Reports** - Track code quality

---

## 📦 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd email-spam-app-main
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -r requirements-api.txt
```

3. **Run the Streamlit UI:**
```bash
streamlit run app_enhanced.py
```
Access at: http://localhost:8501

4. **Run the REST API:**
```bash
python run_api.py
```
Access at: http://localhost:8000/docs

---

## 🎯 Usage

### Web Interface (Streamlit)

1. Open http://localhost:8501
2. Enter or paste email content
3. Click "Analyze Email"
4. View classification results with confidence scores

### REST API

**Classify a single email:**
```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations! You won $1,000,000!"}'
```

**Response:**
```json
{
  "is_spam": true,
  "confidence": 0.95,
  "spam_probability": 0.95,
  "ham_probability": 0.05,
  "processing_time_ms": 12.5,
  "model_version": "1.0",
  "text_stats": {
    "word_count": 5,
    "char_count": 42,
    "avg_word_length": 8.4,
    "uppercase_ratio": 4.8
  }
}
```

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/classify",
    json={"text": "Your email content here"}
)

result = response.json()
print(f"Is spam: {result['is_spam']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

## 📚 Documentation

- **[API Guide](API_GUIDE.md)** - Complete API documentation
- **[Docker Guide](DOCKER_GUIDE.md)** - Containerization and deployment
- **[Installation Guide](INSTALL_GUIDE.md)** - Detailed setup instructions

---

## 🔌 API Endpoints

### Classification

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/classify` | Classify a single email |
| POST | `/api/v1/classify/batch` | Classify multiple emails |

### Health & Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/info` | API information |
| GET | `/docs` | Swagger documentation |
| GET | `/redoc` | ReDoc documentation |

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

**Services:**
- **Streamlit UI**: http://localhost:8501
- **FastAPI**: http://localhost:8000

### Stop Services

```bash
docker-compose down
```

See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for advanced deployment options.

---

## 🧪 Testing

### Run All Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
pytest

# With coverage report
pytest --cov=src --cov=api --cov-report=html
```

### Run Specific Tests

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_predictor.py
```

---

## 🏗️ Project Structure

```
email-spam-app-main/
├── src/                      # Backend modules
│   ├── config/              # Configuration management
│   ├── models/              # ML model handling
│   ├── preprocessing/       # Text processing
│   └── utils/               # Utilities (logging, exceptions)
├── api/                      # REST API
│   ├── routers/             # API endpoints
│   ├── models/              # Request/response schemas
│   └── middleware/          # CORS, etc.
├── tests/                    # Test suite
│   ├── unit/                # Unit tests
│   └── integration/         # API integration tests
├── logs/                     # Application logs
├── app_enhanced.py          # Streamlit UI
├── run_api.py               # API entry point
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-service config
└── requirements*.txt        # Dependencies
```

---

## 🔧 Configuration

Create a `.env` file:

```env
# Application Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=False

# Model Configuration
MODEL_PATH=spam.pkl
VECTORIZER_PATH=vectorizer.pkl
CONFIDENCE_THRESHOLD=0.7

# Performance
MAX_CONTENT_LENGTH=10000
```

---

## 🚀 Deployment

### Cloud Platforms

#### Railway.app
```bash
railway up
```

#### Render.com
Deploy using `render.yaml` configuration.

#### Heroku
```bash
heroku create
git push heroku main
```

See [deployment documentation](docs/deployment.md) for platform-specific guides.

---

## 📊 Performance

- **Classification Speed**: ~10-15ms per email
- **Batch Processing**: ~10ms per email (parallel)
- **Model Loading**: ~500ms (cached after first load)
- **API Response Time**: < 50ms (average)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+
- **Web Framework**: Streamlit, FastAPI
- **ML Library**: scikit-learn, Transformers (HuggingFace), PyTorch
- **Validation**: Pydantic
- **Testing**: pytest
- **Containerization**: Docker
- **API Docs**: Swagger/ReDoc

---

## 📞 Support

For issues or questions:

- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the [API guide](API_GUIDE.md)

Ekky Spurgeon – spurgeonpaul11@outlook.com


---

## 🎯 Roadmap

- [x] Modular backend architecture
- [x] Real Deep Learning (BERT) integration
- [x] Voice Input and History tracking
- [x] Docker containerization
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment

---

<div align="center">

**Made with ❤️ using Python, FastAPI, and Streamlit**

⭐ Star this repo if you find it helpful!

</div>
