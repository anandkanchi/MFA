import os
from datetime import datetime

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Get the absolute path to the project root
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data')
    UPLOAD_FOLDER = os.path.join(DATA_FOLDER, 'uploads')
    PDF_FOLDER = os.path.join(DATA_FOLDER, 'pdfs')
    EXCEL_FOLDER = os.path.join(DATA_FOLDER, 'excel')
    
    @staticmethod
    def ensure_folders_exist():
        """Create all required folders"""
        for folder in [Config.DATA_FOLDER, Config.UPLOAD_FOLDER, Config.PDF_FOLDER, Config.EXCEL_FOLDER]:
            os.makedirs(folder, exist_ok=True)
    
    # API Configuration
    MF_API_TIMEOUT = 30  # seconds
    MAX_DATE_RANGE = 365  # days

# Ensure folders exist when config is loaded
Config.ensure_folders_exist()
