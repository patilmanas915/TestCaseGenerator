# Production Configuration
import os
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig:
    """Production configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # File upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    DOWNLOAD_FOLDER = os.environ.get('DOWNLOAD_FOLDER', 'downloads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
    
    # Gemini model configuration
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-1.5-pro')
    TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.3))
    MAX_OUTPUT_TOKENS = int(os.environ.get('MAX_OUTPUT_TOKENS', 8192))
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ProductionConfig.ALLOWED_EXTENSIONS

class DevelopmentConfig:
    """Development configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Flask settings
    DEBUG = True
    TESTING = False
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    DOWNLOAD_FOLDER = 'downloads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
    
    # Gemini model configuration
    GEMINI_MODEL = 'gemini-1.5-pro'
    TEMPERATURE = 0.3
    MAX_OUTPUT_TOKENS = 8192
    
    # Security settings (relaxed for development)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in DevelopmentConfig.ALLOWED_EXTENSIONS

# Configuration selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
