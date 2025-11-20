"""
WSGI entrypoint for production deployment.
Usage: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:application
"""
from app import create_app

application = create_app('production')