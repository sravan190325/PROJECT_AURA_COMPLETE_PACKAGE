"""
Document processor service.
Routes document parsing to appropriate parser based on file type.
"""

import logging
from typing import Dict, Any, Optional
from services.pdf_parser import PDFParser
from services.docx_parser import DOCXParser
from services.pptx_parser import PPTXParser

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Main document processor.
    Routes file parsing to appropriate service based on file extension.
    """

    # Mapping of file extensions to parsers
    PARSERS = {
        'pdf': PDFParser,
        'docx': DOCXParser,
        'pptx': PPTXParser
    }

    # Mapping of MIME types to extensions
    MIME_TO_EXT = {
        'application/pdf': 'pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx'
    }

    @staticmethod
    def get_file_extension(filename: str) -> Optional[str]:
        """
        Extract file extension from filename.
        
        Args:
            filename: Name of the file
        
        Returns:
            File extension (lowercase) or None if not recognized
        """
        if not filename or '.' not in filename:
            return None
        
        ext = filename.rsplit('.', 1)[1].lower()
        return ext if ext in DocumentProcessor.PARSERS else None

    @staticmethod
    def validate_file(filename: str, mime_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate if a file is supported for processing.
        
        Args:
            filename: Name of the file
            mime_type: MIME type of the file (optional)
        
        Returns:
            Dictionary with validation result and details
        """
        ext = DocumentProcessor.get_file_extension(filename)
        
        if not ext:
            return {
                'valid': False,
                'error': f"Unsupported file type. Allowed: PDF, DOCX, PPTX",
                'extension': None
            }
        
        # If MIME type provided, validate it matches extension
        if mime_type:
            expected_mime = None
            for mime, file_ext in DocumentProcessor.MIME_TO_EXT.items():
                if file_ext == ext:
                    expected_mime = mime
                    break
            
            if expected_mime and mime_type != expected_mime:
                return {
                    'valid': False,
                    'error': f"File extension (.{ext}) does not match MIME type ({mime_type})",
                    'extension': ext
                }
        
        return {
            'valid': True,
            'extension': ext,
            'error': None
        }

    @staticmethod
    def process(file_path: str, filename: str, max_length: int = 50000) -> Dict[str, Any]:
        """
        Process a document and extract its content.
        
        Args:
            file_path: Full path to the file
            filename: Original filename
            max_length: Maximum characters to extract
        
        Returns:
            Dictionary containing:
                - success: Boolean indicating if processing was successful
                - filename: Original filename
                - extension: File extension
                - content: Extracted content (if successful)
                - error: Error message (if failed)
        """
        # Validate file
        validation = DocumentProcessor.validate_file(filename)
        if not validation['valid']:
            return {
                'success': False,
                'filename': filename,
                'extension': None,
                'content': None,
                'error': validation['error']
            }

        ext = validation['extension']
        
        try:
            # Get appropriate parser
            parser_class = DocumentProcessor.PARSERS[ext]
            
            # Parse the document
            logger.info(f"Processing {ext.upper()} file: {filename}")
            result = parser_class.parse(file_path, max_length)
            
            # Add filename and extension to result
            result['filename'] = filename
            result['extension'] = ext
            
            if result['success']:
                logger.info(f"Successfully processed {filename}")
            else:
                logger.error(f"Failed to process {filename}: {result.get('error')}")
            
            return result

        except KeyError:
            error_msg = f"No parser found for extension: {ext}"
            logger.error(error_msg)
            return {
                'success': False,
                'filename': filename,
                'extension': ext,
                'content': None,
                'error': error_msg
            }

        except Exception as e:
            error_msg = f"Unexpected error processing {filename}: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'filename': filename,
                'extension': ext,
                'content': None,
                'error': error_msg
            }
