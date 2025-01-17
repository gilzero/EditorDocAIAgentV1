"""
@fileoverview This module initializes and runs the Flask application for the Dreamer Document AI project.
@filepath main.py
"""

from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
