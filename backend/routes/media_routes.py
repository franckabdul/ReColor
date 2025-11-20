"""
HTTP endpoints for image and video colorization.
"""
import os
import time
import logging
from flask import Blueprint, request, current_app, send_file
from services.deoldify_service import colorize_image, ColorizationError
from services.video_service import colorize_video, VideoColorizationError
from utils.responses import success_response, error_response

# Configure logger
logger = logging.getLogger(__name__)

media_bp = Blueprint('media', __name__)


@media_bp.route('/colorize/image', methods=['POST'])
def colorize_image_endpoint():
    """
    Colorize an uploaded image.

    Expected form data:
        - image: Image file
        - render_factor: Optional quality factor (10-40, default from config)

    Returns:
        JSON with base64-encoded colorized image and timing info
    """
    request_start = time.time()
    client_ip = request.remote_addr

    logger.info(f">>> New image colorization request from {client_ip}")

    # Validate file upload
    if 'image' not in request.files:
        logger.warning(f"Request missing image file from {client_ip}")
        return error_response('No image file provided', 400)

    image_file = request.files['image']

    if image_file.filename == '':
        logger.warning(f"Empty filename from {client_ip}")
        return error_response('Empty filename', 400)

    logger.info(f"File received: {image_file.filename}")

    # Validate file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    file_ext = os.path.splitext(image_file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        logger.warning(f"Invalid file type: {file_ext} from {client_ip}")
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
        logger.info(f"Render factor: {render_factor}")
    except ValueError:
        logger.warning(f"Invalid render_factor value from {client_ip}")
        return error_response('Invalid render_factor value', 400)

    # Read image bytes
    try:
        read_start = time.time()
        image_bytes = image_file.read()
        read_time = time.time() - read_start
        logger.debug(f"Image read in {read_time:.3f}s ({len(image_bytes) / 1024:.2f} KB)")
    except Exception as e:
        logger.error(f"Failed to read image from {client_ip}: {str(e)}")
        return error_response(f'Failed to read image: {str(e)}', 400)

    # Process image
    try:
        result = colorize_image(
            image_bytes=image_bytes,
            filename=image_file.filename,
            render_factor=render_factor,
            output_dir=current_app.config['OUTPUT_FOLDER']
        )

        total_request_time = time.time() - request_start

        logger.info(f"<<< Request completed in {total_request_time:.2f}s")

        return success_response({
            'image': result['image'],
            'filename': f"{os.path.splitext(image_file.filename)[0]}_colorized.jpg",
            'processing_time': result['processing_time'],
            'total_request_time': round(total_request_time, 2),
            'step_times': result['step_times']
        })

    except ColorizationError as e:
        logger.error(f"Colorization error: {str(e)}")
        return error_response(str(e), 500)
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.exception(f"Unexpected error processing request from {client_ip}")
        return error_response('Internal server error', 500)


@media_bp.route('/colorize/video', methods=['POST'])
def colorize_video_endpoint():
    """
    Colorize an uploaded video.

    Expected form data:
        - video: Video file
        - render_factor: Optional quality factor (10-40, default 21)

    Returns:
        JSON with download URL for colorized video
    """
    request_start = time.time()
    client_ip = request.remote_addr

    logger.info(f">>> New video colorization request from {client_ip}")

    # Validate file upload
    if 'video' not in request.files:
        logger.warning(f"Request missing video file from {client_ip}")
        return error_response('No video file provided', 400)

    video_file = request.files['video']

    if video_file.filename == '':
        logger.warning(f"Empty filename from {client_ip}")
        return error_response('Empty filename', 400)

    logger.info(f"File received: {video_file.filename}")

    # Validate file extension
    allowed_extensions = current_app.config['SUPPORTED_VIDEO_FORMATS']
    file_ext = os.path.splitext(video_file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        logger.warning(f"Invalid file type: {file_ext} from {client_ip}")
        return error_response(
            f'Invalid file type. Allowed: {", ".join(allowed_extensions)}',
            400
        )

    # Get render factor from request
    try:
        render_factor = int(
            request.form.get(
                'render_factor',
                current_app.config['VIDEO_RENDER_FACTOR']
            )
        )
        logger.info(f"Render factor: {render_factor}")
    except ValueError:
        logger.warning(f"Invalid render_factor value from {client_ip}")
        return error_response('Invalid render_factor value', 400)

    # Read video bytes
    try:
        read_start = time.time()
        video_bytes = video_file.read()
        read_time = time.time() - read_start
        logger.debug(f"Video read in {read_time:.3f}s ({len(video_bytes) / 1024 / 1024:.2f} MB)")
    except Exception as e:
        logger.error(f"Failed to read video from {client_ip}: {str(e)}")
        return error_response(f'Failed to read video: {str(e)}', 400)

    # Process video
    try:
        result = colorize_video(
            video_bytes=video_bytes,
            filename=video_file.filename,
            render_factor=render_factor,
            output_dir=current_app.config['VIDEO_OUTPUT_FOLDER']
        )

        total_request_time = time.time() - request_start

        logger.info(f"<<< Video request completed in {total_request_time:.2f}s")

        return success_response({
            'filename': result['filename'],
            'video_path': result['video_path'],
            'processing_time': result['processing_time'],
            'total_request_time': round(total_request_time, 2),
            'output_size_mb': result['output_size_mb'],
            'download_url': f"/download/video/{result['filename']}"
        })

    except VideoColorizationError as e:
        logger.error(f"Video colorization error: {str(e)}")
        return error_response(str(e), 500)
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.exception(f"Unexpected error processing video request from {client_ip}")
        return error_response('Internal server error', 500)


@media_bp.route('/download/video/<filename>', methods=['GET'])
def download_video(filename):
    """
    Download a colorized video file.

    Args:
        filename: Name of the video file to download

    Returns:
        Video file as attachment
    """
    logger.info(f"Download request for video: {filename}")

    try:
        video_path = os.path.join(
            current_app.config['VIDEO_OUTPUT_FOLDER'],
            filename
        )

        if not os.path.exists(video_path):
            logger.warning(f"Video file not found: {video_path}")
            return error_response('Video file not found', 404)

        logger.info(f"Serving video: {video_path}")
        return send_file(
            video_path,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )

    except Exception as e:
        logger.exception(f"Error serving video file: {str(e)}")
        return error_response('Failed to serve video file', 500)


@media_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    logger.debug("Health check requested")
    return success_response({'status': 'healthy', 'models_loaded': True})