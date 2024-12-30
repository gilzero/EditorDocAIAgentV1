from markitdown import MarkItDown

def process_document(file_path):
    """Process document using MarkItDown library."""
    try:
        md = MarkItDown()
        result = md.convert(file_path)
        
        metadata = {
            'text_content': result.text_content,
            'author': result.metadata.get('author', 'Unknown'),
            'creation_date': result.metadata.get('creation_date', 'Unknown'),
            'modification_date': result.metadata.get('modification_date', 'Unknown'),
            'title': result.metadata.get('title', 'Unknown'),
            'page_count': result.metadata.get('page_count', 0)
        }
        
        return metadata
    except Exception as e:
        raise Exception(f"Error processing document: {str(e)}")
