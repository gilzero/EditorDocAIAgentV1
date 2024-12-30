import logging
from markitdown import MarkItDown
from app import app

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
            if hasattr(result, 'document_info'):
                info = result.document_info
                metadata.update({
                    'author': info.get('author', 'Unknown'),
                    'creation_date': info.get('created', 'Unknown'),
                    'modification_date': info.get('modified', 'Unknown'),
                    'title': info.get('title', 'Unknown'),
                    'page_count': info.get('pages', 0)
                })
        except Exception as e:
            app.logger.warning(f"Could not extract additional metadata: {str(e)}")

        app.logger.info("Metadata extraction completed")
        return metadata
    except Exception as e:
        app.logger.error(f"Error processing document: {str(e)}")
        raise Exception(f"Failed to process document: {str(e)}")