"""
Application factory for the Flask colorization service.
"""
from flask import Flask
from flask_cors import CORS
import matplotlib

# Use non-GUI backend for matplotlib
matplotlib.use('Agg')


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

    # Initialize CORS
    CORS(app)

    # Initialize extensions (load model)
    from extensions.deoldify_loader import init_colorizer
    init_colorizer()

    # Register blueprints
    from routes.image_routes import image_bp
    app.register_blueprint(image_bp)

    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)