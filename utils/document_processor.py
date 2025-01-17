"""
@fileoverview This module processes documents using the MarkItDown library.
@filepath utils/document_processor.py
"""

# Import the MarkItDown library and the Flask app
from markitdown import MarkItDown
from app import app
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')
import os


# Ensure you have the necessary NLTK data files
nltk.download('punkt')

def process_document(file_path):
    """
    Process a document using the MarkItDown library.

    Args:
        file_path (str): The path to the document file to be processed.

    Returns:
        str: The text content of the document.

    Raises:
        Exception: If there is an error during document processing.
    """
    try:
        app.logger.info(f"🚀 Starting to process document: {file_path}")
        md = MarkItDown()
        result = md.convert(file_path)
        app.logger.info("✅ Document conversion successful")

        # Return only the text content
        text_content = getattr(result, 'text_content', '')
        app.logger.info("📄 Text content extraction completed")

        # Save the result object to a text file for debugging
        result_file_path = os.path.join('debug', 'result.txt')
        try:
            with open(result_file_path, 'w', encoding='utf-8') as result_file:
                result_file.write(str(result))
            app.logger.info(f"✅ Result object saved successfully to {result_file_path}")
        except Exception as e:
            app.logger.error(f"❌ Failed to save result object to {result_file_path}: {str(e)}")

        # Save the text content to a text file for debugging
        text_content_file_path = os.path.join('debug', 'text_content.txt')
        try:
            with open(text_content_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text_content)
            app.logger.info(f"✅ Text content saved successfully to {text_content_file_path}")
        except Exception as e:
            app.logger.error(f"❌ Failed to save text content to {text_content_file_path}: {str(e)}")

        # Count characters in the text content
        char_count = len(text_content)
        app.logger.info(f"📝 Character count: {char_count}")

        return text_content
    except Exception as e:
        app.logger.error(f"❌ Error processing document: {str(e)}")
        raise Exception(f"Failed to process document: {str(e)}")