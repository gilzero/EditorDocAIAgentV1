"""
@file-overview This module processes documents using the MarkItDown library.
@filepath utils/document_processor.py
"""

# Import the MarkItDown library and the Flask app
from markitdown import MarkItDown, FileConversionException
from app import app
import os
from pdfminer.psexceptions import PSSyntaxError
from pypdf import PdfReader


def process_document(file_path):
    """
    Process a document using multiple PDF processing libraries with fallback options.

    Args:
        file_path (str): The path to the document file to be processed.

    Returns:
        dict: A dictionary containing the text content and metadata of the document.

    Raises:
        Exception: If all document processing methods fail.
    """

    # Create debug directory if it doesn't exist
    debug_dir = app.config["DEBUG_DIR"]

    text_content = None
    error_messages = []

    # Try MarkItDown first
    try:
        app.logger.info(
            f"🚀 Attempting to process document with MarkItDown: {file_path}"
        )
        md = MarkItDown()
        result = md.convert(file_path)
        text_content = getattr(result, "text_content", "")
        app.logger.info("✅ MarkItDown conversion successful")

    except (FileConversionException, PSSyntaxError) as e:
        error_messages.append(f"MarkItDown failed: {str(e)}")
        app.logger.warning(f"⚠️ MarkItDown failed, attempting pypdf fallback: {str(e)}")

        # Try pypdf as fallback
        try:
            text_content = _extract_text_with_pypdf(file_path)
            app.logger.info("✅ pypdf fallback successful")
        except Exception as e:
            error_messages.append(f"pypdf fallback failed: {str(e)}")
            app.logger.error(f"❌ pypdf fallback failed: {str(e)}")

    # If all methods failed
    if text_content is None:
        raise Exception(
            f"All document processing methods failed:\n" + "\n".join(error_messages)
        )

    # Save debug output
    text_content_file_path = os.path.join(debug_dir, "text_content.txt")
    try:
        with open(text_content_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(text_content)
        app.logger.info(f"✅ Text content saved to {text_content_file_path}")
    except Exception as e:
        app.logger.error(f"❌ Failed to save debug output: {str(e)}")

    # Process metadata
    char_count = len(text_content)
    meta_title = os.path.splitext(os.path.basename(file_path))[0]
    meta_title = meta_title.rsplit("_", 1)[0]  # Strip UUID

    meta_date = str(os.path.getmtime(file_path))

    # Log metadata
    app.logger.info(f"📝 Title: {meta_title}")
    app.logger.info(f"📝 Character count: {char_count}")
    app.logger.info(f"📝 Upload date: {meta_date}")

    return {
        "text_content": text_content,
        "char_count": char_count,
        "title": meta_title,
        "date_of_upload": meta_date,
    }


def _extract_text_with_pypdf(file_path):
    """
    Extract text from PDF using pypdf as a fallback method.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted text content
    """
    try:
        reader = PdfReader(file_path)
        text_content = ""
        for page in reader.pages:
            text_content += page.extract_text() + "\n"
        return text_content
    except Exception as e:
        app.logger.error(f"❌ pypdf extraction failed: {str(e)}")
        raise
