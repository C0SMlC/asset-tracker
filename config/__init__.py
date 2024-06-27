from .settings import Config

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = False
    MONGODB_URI = 'mongodb://localhost:27017/asset_tracker_test'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name):
    """Helper function to get the config by name."""
    return config.get(config_name, config['default'])