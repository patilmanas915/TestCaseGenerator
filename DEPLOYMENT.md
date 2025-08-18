# AI Test Case Generator - Deployment Guide

## Deployment Options

### 1. Local Development Deployment

#### Prerequisites
- Python 3.8+
- Google Gemini API Key

#### Steps
1. **Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   # Copy environment file
   copy .env.example .env
   
   # Edit .env file with your values:
   # - Set your GEMINI_API_KEY
   # - Set a strong SECRET_KEY
   ```

3. **Run Application**
   ```bash
   # Development mode
   python app.py
   
   # Production mode with Gunicorn
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

4. **Access Application**
   - Open browser: http://localhost:5000

### 2. Docker Deployment

#### Prerequisites
- Docker installed on your system
- Google Gemini API Key

#### Steps
1. **Build Docker Image**
   ```bash
   docker build -t ai-testcase-generator .
   ```

2. **Run Container**
   ```bash
   # Basic run
   docker run -p 5000:5000 -e GEMINI_API_KEY=your_api_key ai-testcase-generator
   
   # With environment file
   docker run -p 5000:5000 --env-file .env ai-testcase-generator
   
   # With volume mounting for persistent data
   docker run -p 5000:5000 \
     --env-file .env \
     -v $(pwd)/uploads:/app/uploads \
     -v $(pwd)/downloads:/app/downloads \
     ai-testcase-generator
   ```

3. **Access Application**
   - Open browser: http://localhost:5000

### 3. Docker Compose Deployment

#### Prerequisites
- Docker and Docker Compose
- Google Gemini API Key

#### Steps
1. **Create docker-compose.yml** (provided)
2. **Configure Environment**
   ```bash
   copy .env.example .env
   # Edit .env with your values
   ```
3. **Deploy**
   ```bash
   docker-compose up -d
   ```
4. **Monitor**
   ```bash
   docker-compose logs -f
   ```

### 4. Cloud Deployment Options

#### Heroku Deployment
1. **Install Heroku CLI**
2. **Setup**
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_api_key
   heroku config:set SECRET_KEY=your_secret_key
   git push heroku main
   ```

#### Railway Deployment
1. **Connect GitHub repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically on push**

#### DigitalOcean App Platform
1. **Connect repository**
2. **Configure environment variables**
3. **Deploy with auto-scaling**

#### AWS/Google Cloud/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Deploy Docker image to cloud registries
- Configure load balancers and auto-scaling

### 5. Production Considerations

#### Security
- Use strong SECRET_KEY
- Keep GEMINI_API_KEY secure
- Enable HTTPS in production
- Configure proper firewall rules

#### Performance
- Use multiple Gunicorn workers
- Configure reverse proxy (Nginx)
- Enable caching where appropriate
- Monitor resource usage

#### Monitoring
- Set up application logs
- Monitor health endpoint (/health)
- Configure alerting for failures
- Track API usage and costs

#### Scaling
- Use load balancers for multiple instances
- Configure auto-scaling based on CPU/memory
- Consider using Redis for session storage
- Implement proper error handling

### 6. Environment Variables

Required environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `SECRET_KEY`: Flask secret key for sessions

Optional environment variables:
- `PORT`: Application port (default: 5000)
- `HOST`: Application host (default: 0.0.0.0)
- `WORKERS`: Number of Gunicorn workers (default: 4)
- `FLASK_ENV`: Environment (development/production)

### 7. Health Check

The application includes a health check endpoint at `/health` that returns:
```json
{
    "status": "healthy",
    "timestamp": "2025-08-18T10:30:00Z",
    "version": "1.0.0"
}
```

### 8. Troubleshooting

#### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify GEMINI_API_KEY is set correctly
3. **File Upload Issues**: Check upload folder permissions
4. **Memory Issues**: Increase container/server memory limits

#### Logs
- Application logs are written to stdout
- Check Docker logs: `docker logs container_name`
- Monitor error rates and response times
