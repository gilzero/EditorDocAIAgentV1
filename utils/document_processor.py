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

        metadata = {
            'text_content': result.text_content,
            'author': result.metadata.get('author', 'Unknown'),
            'creation_date': result.metadata.get('creation_date', 'Unknown'),
            'modification_date': result.metadata.get('modification_date', 'Unknown'),
            'title': result.metadata.get('title', 'Unknown'),
            'page_count': result.metadata.get('page_count', 0)
        }

        app.logger.info("Metadata extracted successfully")
        return metadata
    except Exception as e:
        app.logger.error(f"Error processing document: {str(e)}")
        raise Exception(f"Failed to process document: {str(e)}")