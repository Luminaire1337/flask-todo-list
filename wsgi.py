"""WSGI entry point for production deployment."""
import os

# Load environment variables from .env file
if os.path.exists(".env") and not os.environ.get("FLASK_DEBUG"):
    from dotenv import load_dotenv
    load_dotenv()

# Import the application after loading environment variables
from app import app

if __name__ == "__main__":
    app.run()
