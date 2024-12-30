import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configure max upload size
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max file size

# Set production configuration
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Use a strong secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
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