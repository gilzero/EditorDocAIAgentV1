import os
import logging
import uuid
from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from app import app, db
from models import Document, Payment
from utils.document_processor import process_document
from utils.ai_analyzer import analyze_document
from utils.stripe_utils import (
    create_payment_intent,
    confirm_payment_intent,
    STRIPE_PUBLISHABLE_KEY,
)

ALLOWED_EXTENSIONS = {"pdf", "docx"}

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ANALYSIS_COST = 300  # ¥3.00 in cents


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            app.logger.error("🚫 No file part in the request")
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        analysis_options = request.form.get(
            "analysis_options", {}
        )  # Get analysis options if provided

        if file.filename == "":
            app.logger.error("🚫 No file selected")
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            app.logger.error(f"🚫 Invalid file type: {file.filename}")
            return (
                jsonify(
                    {"error": "Invalid file type. Only PDF and DOCX files are allowed"}
                ),
                400,
            )

        # Print the original file name and its extension
        original_filename = file.filename
        file_extension = (
            original_filename.rsplit(".", 1)[1].lower()
            if "." in original_filename
            else "No extension"
        )
        print(
            f"📄 Original file name: {original_filename}, Extension: {file_extension}"
        )

        try:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
        except Exception as e:
            app.logger.error(f"⚠️ Failed to create upload folder: {str(e)}")
            return jsonify({"error": "Server configuration error"}), 500

        # Use the original filename and append a unique identifier for saving
        filename = secure_filename(original_filename)

        # Split the filename to get the name and extension
        name, extension = os.path.splitext(filename)

        # Append a UUID to the filename to ensure uniqueness, preserving the extension
        unique_filename = f"{uuid.uuid4().hex}.{name}{extension}"
        save_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        try:
            file.save(save_path)
            app.logger.info(f"✅ File saved successfully at {save_path}")
        except Exception as e:
            app.logger.error(f"⚠️ Failed to save file: {str(e)}")
            return jsonify({"error": "Failed to save file"}), 500

        try:
            # Process document
            app.logger.info("🔄 Starting document processing")
            process_document(save_path)
            app.logger.info("✅ Document processed successfully")

            # Save document to database
            document = Document(
                filename=filename,
                original_filename=file.filename,
                file_size=os.path.getsize(save_path),
                mime_type=file.content_type,
            )
            db.session.add(document)
            db.session.commit()

            # Create payment intent with payment method configuration
            payment_intent = create_payment_intent(ANALYSIS_COST, currency="cny")

            return jsonify(
                {
                    "document_id": document.id,
                    "client_secret": payment_intent.client_secret,
                    "publishable_key": STRIPE_PUBLISHABLE_KEY,
                    "amount": ANALYSIS_COST,
                    "currency": "cny",
                }
            )

        except Exception as e:
            app.logger.error(f"❌ Error processing file: {str(e)}")
            if os.path.exists(save_path):
                try:
                    os.remove(save_path)
                except:
                    pass
            return jsonify({"error": str(e)}), 500

    except Exception as e:
        app.logger.error(f"❌ Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/payment/success", methods=["POST"])
def payment_success():
    try:
        data = request.get_json()
        payment_intent_id = data.get("payment_intent_id")
        document_id = data.get("document_id")
        analysis_options = data.get("analysis_options", {})  # Get analysis options

        if not payment_intent_id or not document_id:
            return jsonify({"error": "Missing required parameters"}), 400

        # Verify payment intent
        payment_intent = confirm_payment_intent(payment_intent_id)

        if payment_intent.status != "succeeded":
            return jsonify({"error": "Payment not successful"}), 400

        # Get document
        document = Document.query.get(document_id)
        if not document:
            return jsonify({"error": "Document not found"}), 404

        # Create payment record
        payment = Payment(
            stripe_payment_id=payment_intent_id,
            amount=payment_intent.amount,
            currency=payment_intent.currency,
            status=payment_intent.status,
            document_id=document_id,
        )
        db.session.add(payment)

        # Process the document with AI using analysis options
        analysis_result = analyze_document(
            "",  # Removed document.doc_metadata['text_content']
            analysis_options=analysis_options,
        )
        document.analysis_summary = analysis_result["summary"]

        db.session.commit()

        return jsonify({"success": True, "analysis": analysis_result})

    except Exception as e:
        app.logger.error(f"❌ Payment processing error: {str(e)}")
        return jsonify({"error": str(e)}), 500
