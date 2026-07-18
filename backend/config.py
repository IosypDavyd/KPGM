import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f'sqlite:///{BASE_DIR}/kpgm.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_EXPIRATION', 86400))
    )
    
    # Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    TEMP_FOLDER = os.getenv('TEMP_FOLDER', '/tmp/kpgm')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 2147483648))  # 2GB
    
    # API Keys
    SUNO_API_KEY = os.getenv('SUNO_API_KEY')
    SUNO_API_BASE_URL = os.getenv('SUNO_API_BASE_URL', 'https://api.suno.ai')
    
    RUNWAY_API_KEY = os.getenv('RUNWAY_API_KEY')
    RUNWAY_API_BASE_URL = os.getenv('RUNWAY_API_BASE_URL', 'https://api.runwayml.com')
    
    STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
    STABILITY_API_BASE_URL = os.getenv('STABILITY_API_BASE_URL', 'https://api.stability.ai')
    
    # FFmpeg
    FFMPEG_PATH = os.getenv('FFMPEG_PATH', '/usr/bin/ffmpeg')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # CORS
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5000',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5000'
    ]
    
    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Processing
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', 4))
    TIMEOUT = int(os.getenv('TIMEOUT', 3600))  # 1 hour

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=10)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
