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

# Configure max upload size
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20MB max file size

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

# Initialize extensions
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

# Import routes after app initialization
from routes import *  # noqa

# Create database tables
with app.app_context():
    db.create_all()
