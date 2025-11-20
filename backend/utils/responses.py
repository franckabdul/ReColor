"""
Consistent JSON response helpers.
"""
from flask import jsonify


def success_response(data, status_code=200):
    """
    Create a successful JSON response.

    Args:
        data: Response data (dict or any JSON-serializable object)
        status_code: HTTP status code (default 200)

    Returns:
        Flask JSON response
    """
    response = {
        'success': True,
        'data': data
    }
    return jsonify(response), status_code


def error_response(message, status_code=400):
    """
    Create an error JSON response.

    Args:
        message: Error message string
        status_code: HTTP status code (default 400)

    Returns:
        Flask JSON response
    """
    response = {
        'success': False,
        'error': {
            'message': message,
            'code': status_code
        }
    }
    return jsonify(response), status_code