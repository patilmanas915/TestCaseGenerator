#!/bin/bash

# Production Deployment Script for AI Test Case Generator
# This script sets up and deploys the application in production mode

set -e  # Exit on any error

echo "🚀 Starting AI Test Case Generator Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_error "Please edit .env file with your actual values before continuing!"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Load environment variables
source .env

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your-gemini-api-key-here" ]; then
    print_error "GEMINI_API_KEY is not set in .env file!"
    exit 1
fi

print_status "Environment variables loaded successfully"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads downloads logs

# Set proper permissions
chmod 755 uploads downloads logs

# Build Docker image
print_status "Building Docker image..."
docker build -t ai-testcase-generator:latest .

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Start services
print_status "Starting services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check if application is healthy
print_status "Checking application health..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:5000/health &> /dev/null; then
        print_status "✅ Application is healthy and ready!"
        break
    else
        if [ $attempt -eq $max_attempts ]; then
            print_error "❌ Application failed to start properly"
            docker-compose logs
            exit 1
        fi
        print_status "Attempt $attempt/$max_attempts - waiting for application..."
        sleep 5
        ((attempt++))
    fi
done

# Display deployment information
echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Information:"
echo "=========================="
echo "Application URL: http://localhost:5000"
echo "Health Check: http://localhost:5000/health"
echo "Environment: Production"
echo "Workers: 4"
echo ""
echo "📊 Container Status:"
docker-compose ps
echo ""
echo "📝 Useful Commands:"
echo "View logs: docker-compose logs -f"
echo "Stop application: docker-compose down"
echo "Restart application: docker-compose restart"
echo "Update application: docker-compose up -d --build"
echo ""
echo "🔧 Monitoring:"
echo "Check health: curl http://localhost:5000/health"
echo "View metrics: docker stats"
echo ""

# Optional: Open browser (uncomment if needed)
# if command -v xdg-open &> /dev/null; then
#     xdg-open http://localhost:5000
# elif command -v open &> /dev/null; then
#     open http://localhost:5000
# fi

print_status "Deployment script completed!"
