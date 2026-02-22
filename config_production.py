"""
Production Configuration for Mutual Fund Analyzer
"""
import os
from config import Config

class ProductionConfig(Config):
    """Production configuration"""
    
    # Flask Settings
    DEBUG = False
    TESTING = False
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PREFERRED_URL_SCHEME = 'https'
    
    # Server Settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Performance
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year for static files
    
    # Cloud Storage
    CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET', '')
    USE_CLOUD_STORAGE = os.getenv('USE_CLOUD_STORAGE', 'False') == 'True'
    
    # Database (if using Cloud SQL)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    # API Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per hour"
    
    # Timeout settings
    TIMEOUT = 120
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload
