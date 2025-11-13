# Docker Deployment Guide

## Prerequisites
- Docker Desktop installed
- Docker Compose installed

## Quick Start

### 1. Build and Run with Docker Compose
```bash
docker-compose up --build
```

### 2. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

### 3. Stop the Application
```bash
docker-compose down
```

## Docker Commands

### Build Images
```bash
docker-compose build
```

### Run in Background
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Services
```bash
docker-compose restart
```

### Remove Volumes
```bash
docker-compose down -v
```

## Architecture

The application runs in 3 containers:
1. **PostgreSQL Database** (port 5432)
2. **FastAPI Backend** (port 8001)
3. **React Frontend** (port 3000)

## Troubleshooting

**Port already in use:**
```bash
docker-compose down
lsof -ti:8001 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**Rebuild from scratch:**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```
