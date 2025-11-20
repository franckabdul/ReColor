"""
Application factory for the Flask colorization service.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
import matplotlib

# Use non-GUI backend for matplotlib
matplotlib.use('Agg')


def setup_logging(app):
    """Configure application logging."""
    # Create logs directory
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # Set log level based on debug mode
    log_level = logging.DEBUG if app.debug else logging.INFO

    # Create formatters
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s %(message)s',
        datefmt='%H:%M:%S'
    )

    # Console handler (simple format)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)

    # File handler (detailed format)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'colorization.log'),
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Configure Flask logger
    app.logger.setLevel(log_level)

    # Suppress verbose libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

    app.logger.info("Logging configured successfully")


def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Load default configuration
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    # Load instance configuration if it exists (local overrides)
    try:
        app.config.from_pyfile('config.py')
    except FileNotFoundError:
        pass

    # Setup logging first
    setup_logging(app)

    app.logger.info("=" * 70)
    app.logger.info("Starting ReColor Image Colorization Service")
    app.logger.info(f"Environment: {config_name}")
    app.logger.info(f"Debug mode: {app.debug}")
    app.logger.info("=" * 70)

    # Initialize CORS
    CORS(app)
    app.logger.info("CORS enabled")

    # Initialize extensions (load model)
    from extensions.deoldify_loader import init_colorizer

    use_gpu = app.config.get('USE_GPU', False)
    gpu_id = app.config.get('GPU_DEVICE_ID', 0)
    artistic = app.config.get('ARTISTIC_MODE', True)

    init_colorizer(use_gpu=use_gpu, gpu_id=gpu_id, artistic=artistic,root_folder=os.path.abspath('.'))

    # Register blueprints
    from routes.image_routes import image_bp
    app.register_blueprint(image_bp)
    app.logger.info("Routes registered")

    app.logger.info("Application initialization complete")
    app.logger.info("=" * 70)

    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
