# Docker Setup for NobleCause.ai

This document provides instructions for running the NobleCause.ai application using Docker and Docker Compose.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Architecture

The application consists of four services:

1. **Frontend** - SvelteKit application served by nginx (port 5173)
2. **Backend** - FastAPI application (port 8000)
3. **PostgreSQL** - Database for application data (port 5432)
4. **ChromaDB** - Vector database for embeddings (port 8001)

## Quick Start

1. **Clone the repository and navigate to the project root**
   ```bash
   cd /path/to/NobleCause.ai
   ```

2. **Ensure your OpenRouter API key is set in backend/.env**
   ```bash
   # Check that backend/.env contains:
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

3. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Backend API Docs: http://localhost:8000/docs
   - ChromaDB: http://localhost:8001

## Docker Commands

### Start services (build if needed)
```bash
docker-compose up --build
```

### Start services in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Stop services and remove volumes (⚠️ deletes all data)
```bash
docker-compose down -v
```

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
docker-compose logs chromadb
```

### Rebuild specific service
```bash
docker-compose build backend
docker-compose build frontend
```

## Environment Variables

The following environment variables are configured:

### Backend Service
- `OPENROUTER_API_KEY` - Your OpenRouter API key (from backend/.env)
- `DATABASE_URL` - PostgreSQL connection string
- `CHROMA_HOST` - ChromaDB hostname
- `CHROMA_PORT` - ChromaDB port

### Frontend Service
- `VITE_API_URL` - Backend API URL for the frontend

## Data Persistence

The following volumes are created for data persistence:
- `postgres_data` - PostgreSQL database files
- `chromadb_data` - ChromaDB vector database files

Data will persist between container restarts unless volumes are explicitly removed.

## Health Checks

Both PostgreSQL and ChromaDB services include health checks:
- **PostgreSQL**: Checks database connectivity
- **ChromaDB**: Checks API heartbeat endpoint

The backend service waits for both databases to be healthy before starting.

## Development

### Backend Development
To make changes to the backend:
1. Modify files in the `backend/` directory
2. Rebuild the backend service: `docker-compose build backend`
3. Restart: `docker-compose up backend`

### Frontend Development
To make changes to the frontend:
1. Modify files in the `frontend/` directory
2. Rebuild the frontend service: `docker-compose build frontend`
3. Restart: `docker-compose up frontend`

## Troubleshooting

### Port Conflicts
If you encounter port conflicts, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "5174:80"  # Change 5173 to 5174 for frontend
  - "8001:8000" # Change 8000 to 8001 for backend
```

### Database Connection Issues
1. Ensure PostgreSQL is healthy: `docker-compose ps`
2. Check logs: `docker-compose logs postgres`
3. Verify environment variables in docker-compose.yml

### ChromaDB Issues
1. Check ChromaDB health: `docker-compose ps`
2. View logs: `docker-compose logs chromadb`
3. Test API: `curl http://localhost:8001/api/v1/heartbeat`

### Build Issues
1. Clear Docker cache: `docker system prune -a`
2. Rebuild without cache: `docker-compose build --no-cache`

## Production Considerations

For production deployment:

1. **Environment Variables**: Use proper secrets management
2. **SSL/TLS**: Configure HTTPS with reverse proxy (nginx/traefik)
3. **Database**: Use managed database services
4. **Monitoring**: Add health check endpoints and monitoring
5. **Scaling**: Consider using Docker Swarm or Kubernetes
6. **Backup**: Implement database backup strategies

## File Structure

```
.
├── docker-compose.yml          # Main orchestration file
├── backend/
│   ├── Dockerfile             # Backend container definition
│   ├── .dockerignore          # Backend build exclusions
│   └── ...
├── frontend/
│   ├── Dockerfile             # Frontend container definition
│   ├── .dockerignore          # Frontend build exclusions
│   └── ...
└── DOCKER_README.md           # This file