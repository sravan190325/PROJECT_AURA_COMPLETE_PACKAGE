"""
Routes package for Project Aura.
Contains all API endpoints and route handlers.
"""

from flask import Blueprint

# Import blueprints (using relative import)
from .upload_routes import upload_bp

__all__ = ['upload_bp']
