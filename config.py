"""
Configuration settings for Project Aura application.
"""

import os
from datetime import timedelta

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'project-aura-dev-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    TESTING = False

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # File upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    TEMP_FOLDER = os.path.join(BASE_DIR, 'temp')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx'}
    ALLOWED_MIMETYPES = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }

    # Document processing settings
    MAX_EXTRACTION_LENGTH = 50000  # Max characters to extract per document
    PDF_EXTRACTION_METHOD = 'pdfplumber'  # pdfplumber or PyPDF2
    EXTRACT_TABLES = True
    EXTRACT_IMAGES = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'test_uploads')
    TEMP_FOLDER = os.path.join(BASE_DIR, 'test_temp')
