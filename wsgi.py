import os
import sys

# Set UTF-8 as default encoding
os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Load environment variables
from dotenv import load_dotenv
env_path = os.path.join(project_dir, '.env')
load_dotenv(env_path)

# Import Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
