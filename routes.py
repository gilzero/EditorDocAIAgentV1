import os
import logging
from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from app import app, db
from models import Document, Payment
from utils.document_processor import process_document
from utils.ai_analyzer import analyze_document
from utils.stripe_utils import create_payment_intent, confirm_payment_intent, STRIPE_PUBLISHABLE_KEY

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
UPLOAD_FOLDER = '/tmp'
ANALYSIS_COST = 300  # ¥3.00 in cents

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
        analysis_options = request.form.get('analysis_options', {})  # Get analysis options if provided

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

            # Save document to database
            document = Document(
                filename=filename,
                original_filename=file.filename,
                file_size=os.path.getsize(temp_path),
                mime_type=file.content_type,
                doc_metadata=doc_metadata
            )
            db.session.add(document)
            db.session.commit()

            # Create payment intent with payment method configuration
            payment_intent = create_payment_intent(
                ANALYSIS_COST,
                currency='cny'
            )

            # Clean up temp file
            try:
                os.remove(temp_path)
                app.logger.info("Temporary file removed")
            except Exception as e:
                app.logger.warning(f"Failed to remove temporary file: {str(e)}")

            return jsonify({
                'document_id': document.id,
                'client_secret': payment_intent.client_secret,
                'publishable_key': STRIPE_PUBLISHABLE_KEY,
                'amount': ANALYSIS_COST,
                'currency': 'cny'
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

@app.route('/payment/success', methods=['POST'])
def payment_success():
    try:
        data = request.get_json()
        payment_intent_id = data.get('payment_intent_id')
        document_id = data.get('document_id')
        analysis_options = data.get('analysis_options', {})  # Get analysis options

        if not payment_intent_id or not document_id:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Verify payment intent
        payment_intent = confirm_payment_intent(payment_intent_id)

        if payment_intent.status != 'succeeded':
            return jsonify({'error': 'Payment not successful'}), 400

        # Get document
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        # Create payment record
        payment = Payment(
            stripe_payment_id=payment_intent_id,
            amount=payment_intent.amount,
            currency=payment_intent.currency,
            status=payment_intent.status,
            document_id=document_id
        )
        db.session.add(payment)

        # Process the document with AI using analysis options
        analysis_result = analyze_document(
            document.doc_metadata['text_content'],
            analysis_options=analysis_options
        )
        document.analysis_summary = analysis_result['summary']

        db.session.commit()

        return jsonify({
            'success': True,
            'analysis': analysis_result
        })

    except Exception as e:
        app.logger.error(f"Payment processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500