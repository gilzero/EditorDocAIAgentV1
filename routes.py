import os
import logging
from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from models import Document
from utils.document_processor import process_document
from utils.ai_analyzer import analyze_document

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
UPLOAD_FOLDER = '/tmp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            app.logger.error("No file part in the request")
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            app.logger.error("No file selected")
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            app.logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed'}), 400

        try:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
        except Exception as e:
            app.logger.error(f"Failed to create upload folder: {str(e)}")
            return jsonify({'error': 'Server configuration error'}), 500

        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            file.save(temp_path)
            app.logger.info(f"File saved successfully at {temp_path}")
        except Exception as e:
            app.logger.error(f"Failed to save file: {str(e)}")
            return jsonify({'error': 'Failed to save file'}), 500

        try:
            # Process document
            app.logger.info("Starting document processing")
            doc_metadata = process_document(temp_path)
            app.logger.info("Document processed successfully")

            # Analyze document
            app.logger.info("Starting document analysis")
            analysis_result = analyze_document(doc_metadata['text_content'])
            app.logger.info("Document analyzed successfully")

            # Save to database
            document = Document(
                filename=filename,
                original_filename=file.filename,
                file_size=os.path.getsize(temp_path),
                mime_type=file.content_type,
                doc_metadata=doc_metadata,
                analysis_summary=analysis_result['summary']
            )
            db.session.add(document)
            db.session.commit()
            app.logger.info("Document saved to database")

            # Clean up temp file
            try:
                os.remove(temp_path)
                app.logger.info("Temporary file removed")
            except Exception as e:
                app.logger.warning(f"Failed to remove temporary file: {str(e)}")

            return jsonify({
                'success': True,
                'metadata': doc_metadata,
                'analysis': analysis_result
            })

        except Exception as e:
            app.logger.error(f"Error processing file: {str(e)}")
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500