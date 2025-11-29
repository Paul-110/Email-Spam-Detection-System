# 🐳 Docker Deployment Guide

## Quick Start

### 1. Build and Run All Services

```bash
# Build and start both UI and API
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

**Access the applications:**
- **Streamlit UI**: http://localhost:8501
- **FastAPI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 2. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Individual Services

### Run Only the API

```bash
docker-compose up api
```

### Run Only the Streamlit UI

```bash
docker-compose up streamlit-ui
```

---

## Docker Commands

### Build the Image

```bash
docker build -t spam-classifier .
```

### Run API Container

```bash
docker run -d \
  --name spam-api \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  spam-classifier python run_api.py
```

### Run Streamlit Container

```bash
docker run -d \
  --name spam-ui \
  -p 8501:8501 \
  -v $(pwd)/logs:/app/logs \
  spam-classifier streamlit run app_enhanced.py --server.address=0.0.0.0
```

---

## Logs and Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f streamlit-ui

# Last 100 lines
docker-compose logs --tail=100
```

### Check Service Health

```bash
# List running containers
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Check Streamlit health
curl http://localhost:8501/_stcore/health
```

---

## Environment Variables

Create a `.env` file in the project root:

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

Then reference in `docker-compose.yml`:

```yaml
services:
  api:
    env_file:
      - .env
```

---

## Production Deployment

### Build for Production

```bash
# Build optimized image
docker build -t spam-classifier:latest .

# Tag for registry
docker tag spam-classifier:latest your-registry/spam-classifier:latest

# Push to registry
docker push your-registry/spam-classifier:latest
```

### Deploy to Server

```bash
# On your server
docker pull your-registry/spam-classifier:latest
docker-compose up -d
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs api
docker-compose logs streamlit-ui

# Check if ports are in use
netstat -an | findstr "8000"
netstat -an | findstr "8501"
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up --build --force-recreate
```

### Remove All Containers and Images

```bash
# Stop and remove everything
docker-compose down --rmi all --volumes --remove-orphans

# Clean Docker system
docker system prune -a
```

---

## Resource Limits (Optional)

Add to `docker-compose.yml`:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## Health Checks

Both services include health checks:

**API Health Check:**
```bash
curl http://localhost:8000/health
```

**Streamlit Health Check:**
```bash
curl http://localhost:8501/_stcore/health
```

---

## Volume Persistence

Logs are persisted in `./logs` directory:

```yaml
volumes:
  - ./logs:/app/logs
```

This ensures logs survive container restarts.

---

## Networking

Services communicate through `spam-classifier-network`:

```yaml
networks:
  spam-classifier-network:
    driver: bridge
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `docker-compose up` | Start services |
| `docker-compose up -d` | Start in background |
| `docker-compose down` | Stop services |
| `docker-compose logs -f` | View logs |
| `docker-compose ps` | List containers |
| `docker-compose restart` | Restart services |
| `docker-compose build` | Rebuild images |

---

## Next Steps

1. ✅ Test locally: `docker-compose up`
2. ✅ Verify both services are running
3. ✅ Check health endpoints
4. ✅ Deploy to production server
5. ✅ Set up monitoring and alerts

---

**🎉 Your application is now containerized and ready for deployment anywhere!**
