import os
from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from models import Document
from utils.document_processor import process_document
from utils.ai_analyzer import analyze_document

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        filename = secure_filename(file.filename)
        temp_path = os.path.join('/tmp', filename)
        file.save(temp_path)

        # Process document
        doc_metadata = process_document(temp_path)
        analysis_result = analyze_document(doc_metadata['text_content'])

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

        # Clean up temp file
        os.remove(temp_path)

        return jsonify({
            'success': True,
            'metadata': doc_metadata,
            'analysis': analysis_result
        })

    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': 'Error processing file'}), 500