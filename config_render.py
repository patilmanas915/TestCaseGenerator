import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    UPLOAD_FOLDER = 'uploads'
    DOWNLOAD_FOLDER = 'downloads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
    
    # Gemini model configuration
    GEMINI_MODEL = 'gemini-1.5-pro'
    TEMPERATURE = 0.3
    MAX_OUTPUT_TOKENS = 8192
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

class RenderConfig(Config):
    """Production configuration for Render deployment"""
    
    # Override for production
    DEBUG = False
    TESTING = False
    
    # Use temp directories for Render
    UPLOAD_FOLDER = '/tmp/uploads'
    DOWNLOAD_FOLDER = '/tmp/downloads'
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    @classmethod
    def init_app(cls, app):
        """Initialize app for Render deployment"""
        # Ensure directories exist
        os.makedirs('/tmp/uploads', exist_ok=True)
        os.makedirs('/tmp/downloads', exist_ok=True)
        
        # Set up logging
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

# Configuration selector
def get_config():
    """Get configuration based on environment"""
    if os.environ.get('RENDER'):
        return RenderConfig
    return Config
