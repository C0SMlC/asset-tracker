from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from urllib.parse import urlparse
from config.settings import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS with specific settings
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

    # Initialize MongoDB
    client = MongoClient(app.config['MONGODB_URI'])
    
    # Get the database name from the URI or use a default name
    try:
        db_name = urlparse(app.config['MONGODB_URI']).path.lstrip('/')
    except:
        db_name = None
    
    if not db_name:
        db_name = 'asset_tracker'  # Default database name
    
    app.db = client[db_name]

    from app.routes import main
    app.register_blueprint(main)

    return app