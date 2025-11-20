"""
Business logic for image colorization.
Pure Python - no Flask dependencies.
"""
import os
import io
import base64
import tempfile
import time
import logging
from PIL import Image
from extensions.deoldify_loader import get_colorizer

# Configure logger
logger = logging.getLogger(__name__)


class ColorizationError(Exception):
    """Custom exception for colorization errors."""
    pass


def colorize_image(
        image_bytes: bytes,
        filename: str,
        render_factor: int = 35,
        output_dir: str = 'results'
) -> dict:
    """
    Colorize a grayscale image.

    Args:
        image_bytes: Raw image bytes
        filename: Original filename (for naming output)
        render_factor: Quality factor (10-40, higher = better quality but slower)
        output_dir: Directory to save colorized images

    Returns:
        Dictionary containing:
            - image: Base64-encoded colorized image
            - processing_time: Time taken in seconds
            - steps: Dictionary of step timings

    Raises:
        ColorizationError: If colorization fails
        ValueError: If input parameters are invalid
    """
    start_time = time.time()
    step_times = {}

    logger.info("=" * 60)
    logger.info(f"Starting colorization for: {filename}")
    logger.info(f"Render factor: {render_factor}")
    logger.info(f"Input size: {len(image_bytes) / 1024:.2f} KB")

    # Validate inputs
    if not image_bytes:
        logger.error("Empty image bytes received")
        raise ValueError("Image bytes cannot be empty")

    if not 10 <= render_factor <= 40:
        logger.warning(f"Invalid render factor {render_factor}, must be 10-40")
        raise ValueError("Render factor must be between 10 and 40")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create temporary file for input
    temp_input = None
    temp_output = None

    try:
        # Step 1: Load and validate image
        step_start = time.time()
        logger.info("Step 1/6: Loading image...")

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            logger.info(f"  Image loaded: {image.size[0]}x{image.size[1]} pixels")
        except Exception as e:
            logger.error(f"  Failed to load image: {str(e)}")
            raise ColorizationError(f"Failed to load image: {str(e)}")

        step_times['load_image'] = time.time() - step_start
        logger.debug(f"  Time: {step_times['load_image']:.3f}s")

        # Step 2: Save to temporary file
        step_start = time.time()
        logger.info("Step 2/6: Creating temporary file...")

        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.jpg',
                mode='wb'
        ) as temp_file:
            temp_input = temp_file.name
            image.save(temp_input, 'JPEG', quality=95)
            logger.info(f" Temp file: {temp_input}")

        step_times['save_temp'] = time.time() - step_start
        logger.debug(f"  Time: {step_times['save_temp']:.3f}s")

        # Step 3: Process with DeOldify
        step_start = time.time()
        logger.info("Step 3/6: Running DeOldify colorization...")
        logger.info(f"  This may take a while depending on image size...")

        try:
            colorizer = get_colorizer()
            output_path = colorizer.plot_transformed_image(
                path=temp_input,
                render_factor=render_factor,
                compare=False
            )
            logger.info(f"  Colorization complete")
        except Exception as e:
            logger.error(f"  Colorization failed: {str(e)}")
            raise ColorizationError(f"Colorization failed: {str(e)}")

        step_times['colorize'] = time.time() - step_start
        logger.info(f"  Time: {step_times['colorize']:.3f}s")

        # Step 4: Verify output exists
        step_start = time.time()
        logger.info("Step 4/6: Verifying output...")

        if not os.path.exists(output_path):
            logger.error(f"  Output file not found: {output_path}")
            raise ColorizationError("Colorized image was not generated")

        output_size = os.path.getsize(output_path)
        logger.info(f"  Output file exists: {output_size / 1024:.2f} KB")

        step_times['verify'] = time.time() - step_start

        # Step 5: Move to results directory
        step_start = time.time()
        logger.info("Step 5/6: Saving to results directory...")

        base_name = os.path.splitext(filename)[0]
        result_filename = f"{base_name}_colorized.jpg"
        result_path = os.path.join(output_dir, result_filename)

        os.rename(output_path, result_path)
        temp_output = result_path
        logger.info(f"   Saved: {result_path}")

        step_times['move_file'] = time.time() - step_start
        logger.debug(f"  Time: {step_times['move_file']:.3f}s")

        # Step 6: Read and encode
        step_start = time.time()
        logger.info("Step 6/6: Encoding to base64...")

        with open(result_path, 'rb') as f:
            colorized_bytes = f.read()

        colorized_base64 = base64.b64encode(colorized_bytes).decode('utf-8')
        logger.info(f"  Encoded: {len(colorized_base64)} characters")

        step_times['encode'] = time.time() - step_start
        logger.debug(f"  Time: {step_times['encode']:.3f}s")

        # Calculate total time
        total_time = time.time() - start_time

        logger.info("-" * 60)
        logger.info(f"COLORIZATION SUCCESSFUL")
        logger.info(f"  Total time: {total_time:.2f}s")
        logger.info(f"  Colorization: {step_times['colorize']:.2f}s ({step_times['colorize']/total_time*100:.1f}%)")
        logger.info(f"  Other operations: {total_time - step_times['colorize']:.2f}s")
        logger.info("=" * 60)

        return {
            'image': colorized_base64,
            'processing_time': round(total_time, 2),
            'step_times': {k: round(v, 3) for k, v in step_times.items()}
        }

    except ColorizationError:
        logger.error(f"Colorization error after {time.time() - start_time:.2f}s")
        raise
    except Exception as e:
        logger.error(f"Unexpected error after {time.time() - start_time:.2f}s: {str(e)}")
        raise ColorizationError(f"Unexpected error: {str(e)}")

    finally:
        # Cleanup: Remove temporary input file
        if temp_input and os.path.exists(temp_input):
            try:
                os.remove(temp_input)
                logger.debug(f"Cleaned up temp file: {temp_input}")
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_input}: {e}")