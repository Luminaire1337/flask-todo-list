import os
from typing import Optional

# Load environment variables from .env file
if os.path.exists(".env") and not os.environ.get("FLASK_DEBUG"):
    from dotenv import load_dotenv
    load_dotenv()

def get_env_var(name: str, default: Optional[str] = None) -> str:
    """Get environment variable or return default value."""
    value = os.environ.get(name, default)
    return value if value is not None else ""

if __name__ == "__main__":
    from app import app
    
    # Get configuration from environment variables
    debug_mode = get_env_var("FLASK_DEBUG", "True").lower() == "true"
    host = get_env_var("FLASK_HOST", "127.0.0.1")
    port = int(get_env_var("FLASK_PORT", "5000"))
    
    # Run the application with the specified configuration
    app.run(
        debug=debug_mode,
        host=host,
        port=port
    )
