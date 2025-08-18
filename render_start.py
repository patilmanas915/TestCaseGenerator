#!/usr/bin/env python3
"""
Render deployment startup script for AI Test Case Generator
"""
import os
import sys
import logging

def setup_render_environment():
    """Setup environment for Render deployment"""
    os.environ['RENDER'] = 'true'
    os.environ['FLASK_ENV'] = 'production'
    
    # Create necessary directories
    directories = ['/tmp/uploads', '/tmp/downloads', '/tmp/logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_environment():
    """Validate required environment variables"""
    required_vars = ['GEMINI_API_KEY', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    logging.info("Environment validation passed")
    return True

def main():
    """Main application startup for Render"""
    print("🚀 Starting AI Test Case Generator on Render...")
    
    # Setup Render environment
    setup_render_environment()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Import and configure Flask app
    try:
        from app import app
        logging.info("Flask application imported successfully")
        
        # Get port from Render
        port = int(os.environ.get('PORT', 5000))
        logging.info(f"Starting application on port {port}")
        
        # Run the application
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
