from .settings import Config

# You can define additional configuration classes here if needed
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = False
    # You might want to use a different database for testing
    MONGODB_URI = 'mongodb://localhost:27017/asset_tracker_test'

# Dictionary to easily access different configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name):
    """Helper function to get the config by name."""
    return config.get(config_name, config['default'])