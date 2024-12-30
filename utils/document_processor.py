import logging
from markitdown import MarkItDown
from app import app
from datetime import datetime

def process_document(file_path):
    """Process document using MarkItDown library."""
    try:
        app.logger.info(f"Starting to process document: {file_path}")
        md = MarkItDown()
        result = md.convert(file_path)
        app.logger.info("Document conversion successful")

        # Extract metadata with proper error handling
        metadata = {
            'text_content': getattr(result, 'text_content', ''),
            'author': 'Unknown',
            'creation_date': 'Unknown',
            'modification_date': 'Unknown',
            'title': 'Unknown',
            'page_count': 0
        }

        # Try to get additional metadata if available
        try:
            # First try the document_info attribute
            if hasattr(result, 'document_info') and isinstance(result.document_info, dict):
                info = result.document_info
                metadata.update({
                    'author': info.get('author', info.get('creator', 'Unknown')),
                    'creation_date': format_date(info.get('created')),
                    'modification_date': format_date(info.get('modified')),
                    'title': info.get('title', info.get('subject', 'Unknown')),
                    'page_count': info.get('pages', info.get('page_count', 0))
                })
                app.logger.info("Metadata extracted from document_info")
            # Try alternative metadata sources
            elif hasattr(result, 'metadata') and isinstance(result.metadata, dict):
                metadata.update({
                    'author': result.metadata.get('author', 'Unknown'),
                    'creation_date': format_date(result.metadata.get('creation_date')),
                    'modification_date': format_date(result.metadata.get('modification_date')),
                    'title': result.metadata.get('title', 'Unknown'),
                    'page_count': result.metadata.get('page_count', 0)
                })
                app.logger.info("Metadata extracted from metadata attribute")
        except Exception as e:
            app.logger.warning(f"Could not extract additional metadata: {str(e)}")

        # Ensure numeric values are properly formatted
        metadata['page_count'] = int(metadata['page_count']) if str(metadata['page_count']).isdigit() else 0

        app.logger.info("Metadata extraction completed")
        return metadata
    except Exception as e:
        app.logger.error(f"Error processing document: {str(e)}")
        raise Exception(f"Failed to process document: {str(e)}")

def format_date(date_str):
    """Format date string to a consistent format or return 'Unknown'."""
    if not date_str:
        return 'Unknown'
    try:
        # Try parsing common date formats
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return date_str if isinstance(date_str, str) else 'Unknown'
    except Exception:
        return 'Unknown'