# StegnoX Deployment Guide

## Overview

This guide provides instructions for deploying the StegnoX application in various environments. StegnoX can be deployed as a web application using Docker or as a desktop application distributed to end users.

## Web Application Deployment

### Prerequisites

- Docker and Docker Compose
- A server with at least 2GB RAM and 10GB storage
- Domain name (optional, but recommended for production)

### Deployment Steps

#### 1. Prepare the Environment

Create a `.env` file in the deployment directory with the following variables:

```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
DATABASE_URI=sqlite:///stegnox.db
```

For production, use strong, randomly generated keys.

#### 2. Deploy Using Docker Compose

The deployment script provides several options for deploying the application:

```bash
cd deployment
./deploy.sh -e <environment> -b -u
```

Options:
- `-e <environment>`: Environment (development, staging, production)
- `-b`: Build the containers
- `-u`: Start the containers
- `-d`: Stop the containers
- `-r`: Restart the containers
- `-c`: Clean up (remove containers and volumes)

Example for production deployment:

```bash
./deploy.sh -e production -b -u
```

This will:
- Build the containers with production settings
- Start the application in production mode
- Set up the frontend, backend, Redis, and worker services

#### 3. Verify the Deployment

After deployment, verify that the application is running:

```bash
docker-compose ps
```

The frontend should be accessible at http://your-server-ip, and the backend API at http://your-server-ip:5000.

#### 4. Setting Up HTTPS

For production deployments, it's recommended to set up HTTPS using a reverse proxy like Nginx with Let's Encrypt certificates.

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Desktop Application Distribution

### Prerequisites

- Python 3.8 or higher
- Platform-specific build tools:
  - Windows: NSIS and py2exe
  - macOS: py2app
  - Linux: rpm-build and python3-stdeb

### Building the Desktop Application

The desktop build script can create installers for Windows, macOS, and Linux:

```bash
cd desktop
python build_desktop.py --platform <platform> --clean
```

Options:
- `--platform <platform>`: Platform to build for (windows, macos, linux, all)
- `--clean`: Clean build directory before building
- `--version <version>`: Version number for the build

Example for building all platforms:

```bash
python build_desktop.py --platform all --clean --version 1.0.0
```

This will create:
- Windows: `dist/StegnoX-1.0.0-setup.exe`
- macOS: `dist/StegnoX-1.0.0.dmg`
- Linux: RPM and DEB packages in the `dist` directory

### Distributing the Desktop Application

1. Upload the installers to your website or distribution platform.
2. Provide download links to users.
3. Consider setting up an auto-update mechanism for future releases.

## Maintenance Procedures

### Backup Strategy

Implement a regular backup strategy for your data:

```bash
# Backup script for Docker volumes
docker run --rm -v stegnox-uploads:/data -v /backup:/backup alpine tar -czf /backup/uploads-$(date +%Y%m%d).tar.gz /data
docker run --rm -v stegnox-storage:/data -v /backup:/backup alpine tar -czf /backup/storage-$(date +%Y%m%d).tar.gz /data
docker run --rm -v stegnox-queue:/data -v /backup:/backup alpine tar -czf /backup/queue-$(date +%Y%m%d).tar.gz /data
```

Add this script to a cron job to run daily or weekly.

### Updating the Application

To update the application:

```bash
# Pull latest code
git pull

# Run tests
python run_tests.py

# Rebuild and restart containers
cd deployment
./deploy.sh -e production -b -r
```

### Monitoring

Monitor the application using Docker's built-in tools:

```bash
# View container logs
docker-compose logs -f

# Check container status
docker-compose ps

# Monitor container resource usage
docker stats
```

Consider setting up more advanced monitoring using tools like Prometheus and Grafana.

## Troubleshooting

### Common Issues

1. **Container fails to start**: Check the logs for error messages:
   ```bash
   docker-compose logs backend
   ```

2. **Database connection issues**: Verify the database URI in the `.env` file.

3. **File permission issues**: Ensure the Docker volumes have the correct permissions.

### Getting Help

If you encounter any issues, please:

1. Check the logs for error messages.
2. Consult the [Developer Guide](../developer_guide/README.md) for more information.
3. Contact support at support@stegnox.example.com.
