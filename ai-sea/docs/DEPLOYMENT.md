# AI-SEA Deployment Guide

## Local Development

### Backend
```bash
cd ai-sea/backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd ai-sea/frontend
# Open dashboard.html in browser
# Or serve with:
python -m http.server 8080
```

## Production Deployment

### Docker

```bash
# Build image
docker build -t ai-sea-backend:1.0 -f ai-sea/backend/Dockerfile .

# Run container
docker run -d \
  -p 8000:8000 \
  --name ai-sea \
  ai-sea-backend:1.0

# With MongoDB
docker run -d \
  -p 27017:27017 \
  --name ai-sea-mongo \
  mongo:latest

# Run backend with MongoDB link
docker run -d \
  -p 8000:8000 \
  --link ai-sea-mongo:mongodb \
  -e MONGODB_URL=mongodb://mongodb:27017 \
  --name ai-sea \
  ai-sea-backend:1.0
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./ai-sea/backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
    depends_on:
      - mongodb
  
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

Run with:
```bash
docker-compose up -d
```

### Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-sea-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-sea
  template:
    metadata:
      labels:
        app: ai-sea
    spec:
      containers:
      - name: ai-sea
        image: ai-sea-backend:1.0
        ports:
        - containerPort: 8000
        env:
        - name: MONGODB_URL
          value: "mongodb://mongodb-service:27017"
---
apiVersion: v1
kind: Service
metadata:
  name: ai-sea-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: ai-sea
```

Deploy:
```bash
kubectl apply -f deployment.yaml
```

## GitHub Pages (Frontend)

### Option 1: docs/ folder

1. Copy frontend to docs:
```bash
mkdir -p docs
cp ai-sea/frontend/dashboard.html docs/index.html
```

2. Update WebSocket URL in docs/index.html:
```javascript
const wsUrl = "wss://your-backend.com/ws";
```

3. Enable GitHub Pages in Settings → Pages → Source: docs/

### Option 2: gh-pages branch

```bash
# Create gh-pages branch
git checkout --orphan gh-pages

# Copy frontend
cp ai-sea/frontend/dashboard.html index.html

# Update WebSocket URL
# Edit index.html and change ws://localhost:8000/ws to your production URL

# Commit and push
git add index.html
git commit -m "Deploy AI-SEA dashboard"
git push origin gh-pages

# Enable GitHub Pages in Settings → Pages → Source: gh-pages
```

### Update Configuration

In dashboard.html, update the WebSocket URL:

```javascript
// For GitHub Pages deployment, use your backend URL
const wsUrl = "wss://your-backend-domain.com/ws";

// For local development
// const wsUrl = "ws://localhost:8000/ws";
```

## Environment Variables

Create `.env` file:

```bash
# Backend Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_sea
LOG_LEVEL=INFO

# Ethics Engine Configuration
PHI_THRESHOLD=0.005
NSR_ENABLED=true
OLF_ENABLED=true

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=*
```

## Monitoring

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

### Logs

```bash
# Docker logs
docker logs ai-sea -f

# Kubernetes logs
kubectl logs -f deployment/ai-sea-backend
```

### Metrics

Add Prometheus monitoring:

```python
# In main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

Access metrics at `/metrics`

## Security Considerations

1. **HTTPS**: Always use HTTPS/WSS in production
2. **Authentication**: Add API key authentication
3. **Rate Limiting**: Implement request throttling
4. **CORS**: Restrict allowed origins
5. **Environment Variables**: Never commit secrets

## Scaling

### Horizontal Scaling

Deploy multiple backend instances behind a load balancer:

```yaml
# Scale Kubernetes deployment
kubectl scale deployment ai-sea-backend --replicas=10
```

### Database Scaling

Use MongoDB Atlas or replica sets for high availability.

### Caching

Add Redis for session management and caching:

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="ai-sea:")
```

## Troubleshooting

### Backend won't start
- Check Python version (3.9+)
- Verify all dependencies installed
- Check port 8000 is available

### WebSocket connection fails
- Verify backend is running
- Check CORS configuration
- Ensure WebSocket URL is correct
- Check firewall settings

### Dashboard not updating
- Open browser console for errors
- Verify WebSocket connection
- Check backend logs

## Backup and Recovery

### Database Backup

```bash
# MongoDB backup
mongodump --db ai_sea --out /backup/ai-sea-$(date +%Y%m%d)

# Restore
mongorestore --db ai_sea /backup/ai-sea-20260404
```

### Logs Backup

```bash
# Export logs
curl http://localhost:8000/logs?limit=10000 > logs-backup.json
```

---

**Deployment Complete!** 🚀

Your AI-SEA framework is now running in production.
