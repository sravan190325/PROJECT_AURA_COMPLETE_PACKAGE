"""
Project Aura - AI-Powered Project Planning Assistant
Phase 1: Document Upload & Content Extraction
Phase 2: Claude Integration & Project Detection

Main Flask application entry point.
"""

import os
from flask import Flask, render_template, session
from dotenv import load_dotenv
from routes.upload_routes import upload_bp
from routes.project_routes import project_bp
from routes.workbook_routes import workbook_bp
from config import Config

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.TEMP_FOLDER, exist_ok=True)
os.makedirs('workbooks', exist_ok=True)

# Register blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(project_bp)
app.register_blueprint(workbook_bp)


@app.route('/')
def index():
    """Landing page with file upload interface."""
    return render_template('index_blend.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy'}, 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return {
        'success': False,
        'error': 'File size exceeds maximum limit (10MB). Please upload a smaller file.'
    }, 413


@app.errorhandler(400)
def bad_request(error):
    """Handle bad request error."""
    return {
        'success': False,
        'error': 'Invalid request. Please check your input and try again.'
    }, 400


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error."""
    return {
        'success': False,
        'error': 'An internal server error occurred. Please try again later.'
    }, 500


if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        use_reloader=True
    )
