"""
Mutual Fund Data Analyzer
Main application entry point
"""

from app import create_app
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    env = os.getenv('FLASK_ENV', 'development')
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Log startup info
    app.logger.info(f"Starting Mutual Fund Analyzer in {env} mode")
    app.logger.info(f"Listening on {host}:{port}")
    
    # Run development server
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

