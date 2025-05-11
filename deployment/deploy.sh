#!/bin/bash
# StegnoX Deployment Script

# Exit on error
set -e

# Display help message
function show_help {
    echo "StegnoX Deployment Script"
    echo "Usage: ./deploy.sh [options]"
    echo ""
    echo "Options:"
    echo "  -e, --env ENV     Set environment (development, staging, production)"
    echo "  -b, --build       Build containers"
    echo "  -u, --up          Start containers"
    echo "  -d, --down        Stop containers"
    echo "  -r, --restart     Restart containers"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh -e production -b -u  # Build and start in production mode"
    echo "  ./deploy.sh -r                   # Restart containers"
    echo "  ./deploy.sh -d                   # Stop containers"
}

# Default values
ENV="development"
BUILD=false
UP=false
DOWN=false
RESTART=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -e|--env)
        ENV="$2"
        shift
        shift
        ;;
        -b|--build)
        BUILD=true
        shift
        ;;
        -u|--up)
        UP=true
        shift
        ;;
        -d|--down)
        DOWN=true
        shift
        ;;
        -r|--restart)
        RESTART=true
        shift
        ;;
        -h|--help)
        show_help
        exit 0
        ;;
        *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
done

# Set environment variables based on environment
if [ "$ENV" = "production" ]; then
    export COMPOSE_FILE="docker-compose.yml:docker-compose.prod.yml"
    echo "Setting up production environment..."
elif [ "$ENV" = "staging" ]; then
    export COMPOSE_FILE="docker-compose.yml:docker-compose.staging.yml"
    echo "Setting up staging environment..."
else
    export COMPOSE_FILE="docker-compose.yml:docker-compose.dev.yml"
    echo "Setting up development environment..."
fi

# Generate random keys if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(openssl rand -hex 32)
    echo "Generated random SECRET_KEY"
fi

if [ -z "$JWT_SECRET_KEY" ]; then
    export JWT_SECRET_KEY=$(openssl rand -hex 32)
    echo "Generated random JWT_SECRET_KEY"
fi

# Execute commands
if [ "$DOWN" = true ]; then
    echo "Stopping containers..."
    docker-compose down
fi

if [ "$BUILD" = true ]; then
    echo "Building containers..."
    docker-compose build
fi

if [ "$UP" = true ]; then
    echo "Starting containers..."
    docker-compose up -d
fi

if [ "$RESTART" = true ]; then
    echo "Restarting containers..."
    docker-compose restart
fi

# If no action specified, show help
if [ "$BUILD" = false ] && [ "$UP" = false ] && [ "$DOWN" = false ] && [ "$RESTART" = false ]; then
    show_help
    exit 1
fi

echo "Deployment completed successfully!"
