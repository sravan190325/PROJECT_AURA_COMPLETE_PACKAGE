"""
Upload routes for Project Aura.
Handles file upload, validation, and processing.
"""

import os
import logging
from flask import Blueprint, request, render_template, jsonify, session
from werkzeug.utils import secure_filename
from config import Config
from services.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload', __name__, url_prefix='/api')


def allowed_file(filename: str) -> bool:
    """
    Check if a file has an allowed extension.
    
    Args:
        filename: Name of the file to check
    
    Returns:
        True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@upload_bp.route('/upload', methods=['POST'])
def upload_files():
    """
    Handle file uploads and process documents.
    Supports multiple file uploads.
    
    Returns:
        JSON response with processing results
    """
    try:
        # Check if files are in request
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided in request'
            }), 400

        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return jsonify({
                'success': False,
                'error': 'No files selected for upload'
            }), 400

        # Process each file
        results = []
        errors = []

        for file in files:
            if file.filename == '':
                errors.append('Empty filename detected')
                continue

            # Validate file extension
            if not allowed_file(file.filename):
                errors.append(f"'{file.filename}' - Unsupported file type. Use PDF, DOCX, or PPTX")
                continue

            try:
                # Secure the filename
                filename = secure_filename(file.filename)
                
                # Create unique filename to avoid collisions
                import uuid
                unique_filename = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)

                # Save the file
                file.save(filepath)
                logger.info(f"File saved: {filename}")

                # Process the document
                result = DocumentProcessor.process(
                    filepath,
                    filename,
                    max_length=Config.MAX_EXTRACTION_LENGTH
                )

                if result['success']:
                    # Store processed content in session for next step
                    if 'processed_documents' not in session:
                        session['processed_documents'] = []
                    
                    # Prepare document data for session storage
                    doc_data = {
                        'filename': result['filename'],
                        'extension': result['extension'],
                        'metadata': result.get('metadata', {}),
                        'text': result.get('text', ''),
                        'page_count': result.get('page_count', 'N/A'),
                        'has_tables': result.get('has_tables', False),
                        'temp_path': filepath
                    }
                    session['processed_documents'].append(doc_data)
                    
                    results.append({
                        'success': True,
                        'filename': result['filename'],
                        'extension': result['extension'],
                        'metadata': result.get('metadata', {}),
                        'preview': result.get('text', '')[:500] + '...',  # Preview only
                        'page_count': result.get('page_count', 'N/A'),
                        'has_tables': result.get('has_tables', False)
                    })
                else:
                    errors.append(f"'{result['filename']}' - {result.get('error', 'Unknown error')}")
                    # Clean up failed upload
                    if os.path.exists(filepath):
                        os.remove(filepath)

            except Exception as e:
                error_msg = f"'{file.filename}' - Error processing file: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                # Clean up
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass

        # Mark session as modified to ensure it's saved
        session.modified = True

        # Return results
        return jsonify({
            'success': len(results) > 0,
            'processed': len(results),
            'failed': len(errors),
            'results': results,
            'errors': errors if errors else None,
            'total_documents': len(session.get('processed_documents', []))
        }), 200 if len(results) > 0 else 400

    except Exception as e:
        error_msg = f"Unexpected error during file upload: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@upload_bp.route('/documents', methods=['GET'])
def get_documents():
    """
    Retrieve all processed documents from current session.
    
    Returns:
        JSON response with list of processed documents
    """
    try:
        documents = session.get('processed_documents', [])
        
        return jsonify({
            'success': True,
            'count': len(documents),
            'documents': documents
        }), 200

    except Exception as e:
        error_msg = f"Error retrieving documents: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@upload_bp.route('/clear', methods=['POST'])
def clear_session():
    """
    Clear all processed documents from session.
    
    Returns:
        JSON response confirming session cleared
    """
    try:
        # Get files to delete
        documents = session.get('processed_documents', [])
        
        # Delete temporary files
        for doc in documents:
            temp_path = doc.get('temp_path')
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    logger.info(f"Deleted temporary file: {temp_path}")
                except Exception as e:
                    logger.warning(f"Failed to delete {temp_path}: {str(e)}")
        
        # Clear session
        if 'processed_documents' in session:
            del session['processed_documents']
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Session cleared successfully'
        }), 200

    except Exception as e:
        error_msg = f"Error clearing session: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500


@upload_bp.route('/results')
def results():
    """
    Display extraction results page.

    Returns:
        Rendered HTML template with extracted content
    """
    try:
        documents = session.get('processed_documents', [])

        if not documents:
            return render_template('index_blend.html',
                                 error='No documents to display. Please upload documents first.')

        return render_template('results_blend.html', documents=documents)

    except Exception as e:
        error_msg = f"Error loading results: {str(e)}"
        logger.error(error_msg)
        return render_template('index_blend.html', error=error_msg)
