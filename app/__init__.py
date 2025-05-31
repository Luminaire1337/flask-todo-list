import os
from typing import Dict, Any, Optional
from datetime import datetime
from flask import Flask, render_template

def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:
    """Create and configure the Flask application."""
    # Create the Flask application
    app = Flask(__name__, template_folder="views")
    
    # Configure secret key
    app.config["SECRET_KEY"] = os.environ.get("APP_KEY") or os.urandom(24).hex()
    
    # Apply test configuration if provided
    if test_config:
        app.config.update(test_config)
    
    # Register database connection cleanup after each request
    from app.utils.database_connection import DatabaseConnection
    @app.teardown_appcontext
    def close_db_connections(exception=None):
        """Close database connections at the end of the request."""
        DatabaseConnection.close_all()
        
    # Register utilities with the Jinja context
    from app.utils import time_ago
    @app.context_processor
    def utility_processor() -> Dict[str, Any]:
        return {
            "time_ago": time_ago,
            "now": datetime.now()
        }
    
    # Register blueprints
    from app.controllers import index_blueprint, todo_blueprint
    app.register_blueprint(index_blueprint)
    app.register_blueprint(todo_blueprint)
    
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_code=404, error_message="Page not found"), 404
        
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error_code=500, error_message="Internal server error"), 500
      

    return app

# Create the application instance
app = create_app()
