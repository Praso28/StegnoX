# StegnoX Deployment Guide

This document provides instructions for deploying the StegnoX application in various environments.

## Prerequisites

- Docker and Docker Compose
- Git
- Python 3.8 or higher (for desktop application builds)
- Node.js 14 or higher (for frontend development)

## Deployment Options

StegnoX can be deployed in several ways:

1. **Docker Deployment**: Deploy using Docker and Docker Compose
2. **Manual Deployment**: Deploy the components manually
3. **Desktop Application**: Build and distribute the desktop application

## Docker Deployment

### Quick Start

The easiest way to deploy StegnoX is using the provided deployment script:

```bash
# Make the script executable
chmod +x deploy.sh

# Deploy in production mode
./deploy.sh -e production -b -u
```

### Environment-Specific Deployment

StegnoX supports different deployment environments:

- **Development**: For local development
- **Staging**: For testing before production
- **Production**: For production deployment

To deploy to a specific environment:

```bash
# Development
./deploy.sh -e development -b -u

# Staging
./deploy.sh -e staging -b -u

# Production
./deploy.sh -e production -b -u
```

### Manual Docker Commands

If you prefer to use Docker Compose directly:

```bash
# Build the containers
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Start the containers
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Stop the containers
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f
```

## Manual Deployment

### Backend Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your_secret_key
   export JWT_SECRET_KEY=your_jwt_secret_key
   export DATABASE_URI=your_database_uri
   ```

3. Run the backend:
   ```bash
   cd backend
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

### Frontend Deployment

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Build the frontend:
   ```bash
   npm run build
   ```

3. Serve the built files:
   ```bash
   # Using nginx
   cp -r build/* /var/www/html/
   ```

## Desktop Application

### Building the Desktop Application

Use the provided build script to create installers for different platforms:

```bash
# Make the script executable
chmod +x build_desktop.py

# Build for all platforms
python build_desktop.py --version 2023.5.1

# Build for a specific platform
python build_desktop.py --platform windows --version 2023.5.1
```

### Distribution

The built installers will be available in the `dist` directory:

- Windows: `dist/StegnoX-<version>-setup.exe`
- macOS: `dist/StegnoX-<version>.dmg`
- Linux: `dist/stegnox-<version>-1.x86_64.rpm` and `dist/stegnox_<version>_amd64.deb`

## Continuous Integration/Continuous Deployment (CI/CD)

StegnoX uses GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/deploy.yml`.

### Setting Up CI/CD

1. Add the following secrets to your GitHub repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub token
   - `DEPLOY_HOST`: Your deployment server hostname
   - `DEPLOY_USERNAME`: Your deployment server username
   - `DEPLOY_KEY`: Your deployment server SSH private key

2. Push to the `main` branch to trigger the deployment workflow.

## Monitoring and Maintenance

### Health Checks

All containers have health checks configured. You can monitor their status with:

```bash
docker-compose ps
```

### Logs

View logs with:

```bash
docker-compose logs -f [service_name]
```

### Backups

It's recommended to regularly backup the following volumes:

- `stegnox-uploads`: User-uploaded images
- `stegnox-storage`: Analysis results
- `stegnox-queue`: Job queue data

```bash
# Example backup command
docker run --rm -v stegnox-uploads:/data -v /backup:/backup alpine tar -czf /backup/uploads-backup.tar.gz /data
```

## Troubleshooting

### Common Issues

1. **Container fails to start**: Check logs with `docker-compose logs [service_name]`
2. **Frontend can't connect to backend**: Ensure the nginx configuration is correct
3. **Worker not processing jobs**: Check Redis connection and worker logs

### Getting Help

If you encounter issues, please:

1. Check the logs for error messages
2. Consult the [troubleshooting guide](troubleshooting.md)
3. Open an issue on GitHub
