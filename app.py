"""
File Overview:
This module sets up the Flask application and configures the SQLAlchemy database for the Dreamer Document AI project.

File Path:
app.py
"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.INFO)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


# Initialize SQLAlchemy with a custom model base class
db = SQLAlchemy(model_class=Base)

# Create a Flask application instance
app = Flask(__name__)

# Configure max upload size
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20MB max file size

# Set production configuration
app.config["ENV"] = "production"
app.config["DEBUG"] = False

# Use a strong secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

# Configure the database to use SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dreamer_document_ai.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
}

# Initialize database
db.init_app(app)

# Import routes after app initialization
from routes import *  # noqa

# Create database tables
with app.app_context():
    db.create_all()
