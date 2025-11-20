"""
Application configuration classes.
"""
import os
import torch


class Config:
    """Base configuration."""
    # File upload limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Output directory for colorized images
    OUTPUT_FOLDER = 'results'

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    DEFAULT_RENDER_FACTOR = 35
    ARTISTIC_MODE = True

    # Device settings
    USE_GPU = True
    GPU_DEVICE_ID = 0


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    USE_GPU = torch.cuda.is_available() if 'torch' in dir() else True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Add production-specific settings here
    # e.g., logging, monitoring, etc.


# Helper to check if GPU is available
try:
    DevelopmentConfig.USE_GPU = torch.cuda.is_available()
except ImportError:
    DevelopmentConfig.USE_GPU = False