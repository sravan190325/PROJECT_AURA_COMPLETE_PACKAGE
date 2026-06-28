"""
PDF document parser using pdfplumber.
Extracts text, tables, and metadata from PDF files.
"""

import pdfplumber
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class PDFParser:
    """
    Parser for PDF documents.
    Extracts text content, tables, and metadata.
    """

    @staticmethod
    def parse(file_path: str, max_length: int = 50000) -> Dict[str, Any]:
        """
        Parse a PDF file and extract its content.
        
        Args:
            file_path: Path to the PDF file
            max_length: Maximum characters to extract (default: 50000)
        
        Returns:
            Dictionary containing:
                - text: Extracted text content
                - tables: List of extracted tables
                - metadata: Document metadata
                - page_count: Number of pages
                - success: Boolean indicating parsing success
                - error: Error message if parsing failed
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                # Extract metadata
                metadata = {
                    'title': pdf.metadata.get('Title', 'Unknown') if pdf.metadata else 'Unknown',
                    'author': pdf.metadata.get('Author', 'Unknown') if pdf.metadata else 'Unknown',
                    'subject': pdf.metadata.get('Subject', 'Unknown') if pdf.metadata else 'Unknown',
                    'pages': len(pdf.pages)
                }

                # Extract text and tables from all pages
                full_text = []
                all_tables = []

                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()
                    if text:
                        full_text.append(f"--- Page {page_num} ---\n{text}")

                    # Extract tables if they exist
                    try:
                        tables = page.extract_tables()
                        if tables:
                            for table in tables:
                                all_tables.append({
                                    'page': page_num,
                                    'data': table
                                })
                    except Exception as e:
                        logger.warning(f"Failed to extract tables from page {page_num}: {str(e)}")
                        continue

                # Combine text and truncate if necessary
                combined_text = '\n\n'.join(full_text)
                if len(combined_text) > max_length:
                    combined_text = combined_text[:max_length] + '\n\n[Content truncated...]'

                return {
                    'success': True,
                    'text': combined_text,
                    'tables': all_tables,
                    'metadata': metadata,
                    'page_count': metadata['pages'],
                    'has_tables': len(all_tables) > 0,
                    'error': None
                }

        except FileNotFoundError:
            error_msg = f"PDF file not found: {file_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'text': '',
                'tables': [],
                'metadata': {},
                'page_count': 0,
                'has_tables': False,
                'error': error_msg
            }

        except Exception as e:
            error_msg = f"Error parsing PDF: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'text': '',
                'tables': [],
                'metadata': {},
                'page_count': 0,
                'has_tables': False,
                'error': error_msg
            }
