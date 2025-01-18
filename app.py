"""
@fileoverview This module initializes the Flask application and its extensions.
@filepath app.py
"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)


class Base(DeclarativeBase):
    pass


# Initialize Flask app
app = Flask(__name__)


# CORS Configuration
app.config["CORS_HEADERS"] = "Content-Type"
app.config["CORS_RESOURCES"] = {r"/*": {"origins": "*"}}

# app.py

# Add these lines to configure allowed file extensions and uploads folder
app.config["ALLOWED_EXTENSIONS"] = {"pdf", "docx"}
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "uploads"
)
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Add these lines to configure the debug directory
app.config["DEBUG_DIR"] = os.path.join(app.root_path, "debug")
if not os.path.exists(app.config["DEBUG_DIR"]):
    os.makedirs(app.config["DEBUG_DIR"])

# Configure max upload size
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20MB max file size


# Add these lines to configure the OpenAI model parameters
app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
app.config["OPENAI_MODEL_NAME"] = "gpt-4o"
app.config["OPENAI_TEMPERATURE"] = 0.7
app.config["OPENAI_MAX_TOKENS"] = 4096

# app.py

# Add these lines to configure the pricing tiers and minimum charge
app.config["PRICING_TIERS"] = [
    {"max_chars": 1000, "price": 100},
    {"max_chars": 5000, "price": 200},
    {"max_chars": 10000, "price": 300},
    {"max_chars": 50000, "price": 500},
    {"max_chars": 100000, "price": 800},
    {"max_chars": float("inf"), "price": 1000},
]
app.config["MIN_CHARGE"] = 350  # ¥3.50 in cents

# Use a strong secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///dreamer_document_ai.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
}

# Configure Stripe keys
app.config["STRIPE_SECRET_KEY"] = os.getenv("STRIPE_SECRET_KEY")
app.config["STRIPE_PUBLISHABLE_KEY"] = os.getenv("STRIPE_PUBLISHABLE_KEY")
app.config["STRIPE_PAYMENT_METHOD_CONFIG"] = os.getenv("STRIPE_PAYMENT_METHOD_CONFIG")

# Initialize extensions
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

# Import routes after app initialization
from routes import *  # noqa

# Create database tables
with app.app_context():
    db.create_all()
