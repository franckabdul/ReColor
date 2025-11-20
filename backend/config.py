"""
Application configuration classes.
"""
import os


class Config:
    """Base configuration."""
    # File upload limits
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB for videos

    # Output directories
    OUTPUT_FOLDER = 'results'
    VIDEO_OUTPUT_FOLDER = 'results/videos'

    # Ensure output folders exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(VIDEO_OUTPUT_FOLDER, exist_ok=True)

    # Default colorization settings
    DEFAULT_RENDER_FACTOR = 35
    ARTISTIC_MODE = True

    # Video settings
    VIDEO_RENDER_FACTOR = 21  # Lower for faster processing
    SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}

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
    import torch
    DevelopmentConfig.USE_GPU = torch.cuda.is_available()
except ImportError:
    DevelopmentConfig.USE_GPU = False