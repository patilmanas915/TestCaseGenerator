#!/usr/bin/env python3
"""
Production-ready startup script for AI Test Case Generator
Handles both Docker and local deployments with proper configuration
"""

import os
import sys
import logging
from datetime import datetime

def setup_logging():
    """Configure logging for production"""
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log') if os.path.exists('logs') else logging.StreamHandler()
        ]
    )

def validate_environment():
    """Validate required environment variables"""
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    logging.info("Environment validation passed")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'downloads', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Directory '{directory}' is ready")

def main():
    """Main application startup"""
    print("🚀 Starting AI Test Case Generator...")
    print(f"📅 Startup time: {datetime.now().isoformat()}")
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Import Flask app after environment setup
    try:
        from app import app
        logger.info("Flask application imported successfully")
    except ImportError as e:
        logger.error(f"Failed to import Flask application: {e}")
        sys.exit(1)
    
    # Get configuration
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV', 'production') != 'production'
    
    logger.info(f"Configuration: host={host}, port={port}, debug={debug}")
    
    # Start application
    try:
        if debug:
            logger.info("Starting in development mode")
            app.run(debug=True, host=host, port=port)
        else:
            logger.info("Starting in production mode")
            app.run(debug=False, host=host, port=port)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
