"""
Configuration file for AI Emotion Detection Application
"""

import os



class Config:
    """Base configuration class"""

    # Flask configuration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    # Application configuration
    APP_NAME = "AI Emotion Detection"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Advanced Customer Feedback Analytics using Watson NLP Technology"

    # Server configuration
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))

    # Logging configuration
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Emotion detection configuration
    EMOTION_DETECTION = {
        "base_score": 0.3,
        "max_score": 1.0,
        "confidence_threshold": 0.1,
    }

    # Supported emotions
    SUPPORTED_EMOTIONS = ["joy", "sadness", "anger", "fear", "disgust"]

    # Intensity modifiers
    INTENSITY_MODIFIERS = {
        "very": 1.5,
        "really": 1.4,
        "extremely": 1.8,
        "incredibly": 1.7,
        "absolutely": 1.6,
        "slightly": 0.7,
        "somewhat": 0.8,
        "kind of": 0.6,
    }


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    LOG_LEVEL = "WARNING"

    # In production, use environment variables for sensitive data
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name: str = None) -> Config:
    """
    Get configuration object based on environment

    Args:
        config_name (str): Configuration name (development, production, testing)

    Returns:
        Config: Configuration object
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    return config.get(config_name, config["default"])
