# app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app(testing=False):
    """Create and configure the Flask app"""
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "max_age": 3600
        }
    })
    if testing:
        app.config['TESTING'] = True
        # Add any test-specific configuration
    
    # Import and register routes
    from app.api.routes import bp as api_bp
    app.register_blueprint(api_bp)
    
    return app