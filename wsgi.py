"""
WSGI entry point for production deployment.
Used by Gunicorn and other WSGI servers.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import and create Flask app
from app import app

if __name__ == "__main__":
    # This should only be used for development
    app.run()
