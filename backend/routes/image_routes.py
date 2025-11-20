"""
HTTP endpoints for image colorization.
"""
import os
from flask import Blueprint, request, current_app
from services.deoldify_service import colorize_image, ColorizationError
from utils.responses import success_response, error_response


image_bp = Blueprint('image', __name__)


@image_bp.route('/colorize', methods=['POST'])
def colorize_endpoint():
    """
    Colorize an uploaded image.

    Expected form data:
        - image: Image file
        - render_factor: Optional quality factor (10-40, default from config)

    Returns:
        JSON with base64-encoded colorized image
    """
    # Validate file upload
    if 'image' not in request.files:
        return error_response('No image file provided', 400)

    image_file = request.files['image']

    if image_file.filename == '':
        return error_response('Empty filename', 400)

    # Validate file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    file_ext = os.path.splitext(image_file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        return error_response(
            f'Invalid file type. Allowed: {", ".join(allowed_extensions)}',
            400
        )

    # Get render factor from request
    try:
        render_factor = int(
            request.form.get(
                'render_factor',
                current_app.config['DEFAULT_RENDER_FACTOR']
            )
        )
    except ValueError:
        return error_response('Invalid render_factor value', 400)

    # Read image bytes
    try:
        image_bytes = image_file.read()
    except Exception as e:
        return error_response(f'Failed to read image: {str(e)}', 400)

    # Process image
    try:
        colorized_base64 = colorize_image(
            image_bytes=image_bytes,
            filename=image_file.filename,
            render_factor=render_factor,
            output_dir=current_app.config['OUTPUT_FOLDER']
        )

        return success_response({
            'image': colorized_base64,
            'filename': f"{os.path.splitext(image_file.filename)[0]}_colorized.jpg"
        })

    except ColorizationError as e:
        return error_response(str(e), 500)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return error_response('Internal server error', 500)


@image_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return success_response({'status': 'healthy'})


