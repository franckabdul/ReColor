"""
Business logic for image colorization.
Pure Python - no Flask dependencies.
"""
import os
import io
import base64
import tempfile
from PIL import Image
from extensions.deoldify_loader import get_colorizer

class ColorizationError(Exception):
    """Custom exception for colorization errors."""
    pass


def colorize_image(
        image_bytes: bytes,
        filename: str,
        render_factor: int = 35,
        output_dir: str = 'results'
) -> str:
    """
    Colorize a grayscale image.

    Args:
        image_bytes: Raw image bytes
        filename: Original filename (for naming output)
        render_factor: Quality factor (10-40, higher = better quality but slower)
        output_dir: Directory to save colorized images

    Returns:
        Base64-encoded colorized image

    Raises:
        ColorizationError: If colorization fails
        ValueError: If input parameters are invalid
    """
    # Validate inputs
    if not image_bytes:
        raise ValueError("Image bytes cannot be empty")

    if not 10 <= render_factor <= 40:
        raise ValueError("Render factor must be between 10 and 40")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create temporary file for input
    temp_input = None
    temp_output = None

    try:
        # Step 1: Load and validate image
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        except Exception as e:
            raise ColorizationError(f"Failed to load image: {str(e)}")

        # Step 2: Save to temporary file
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.jpg',
                mode='wb'
        ) as temp_file:
            temp_input = temp_file.name
            image.save(temp_input, 'JPEG')

        # Step 3: Process with DeOldify
        try:
            colorizer = get_colorizer()
            output_path = colorizer.plot_transformed_image(
                path=temp_input,
                render_factor=render_factor,
                compare=False
            )
        except Exception as e:
            raise ColorizationError(f"Colorization failed: {str(e)}")

        # Step 4: Verify output exists
        if not os.path.exists(output_path):
            raise ColorizationError("Colorized image was not generated")

        # Step 5: Move to results directory
        base_name = os.path.splitext(filename)[0]
        result_filename = f"{base_name}_colorized.jpg"
        result_path = os.path.join(output_dir, result_filename)

        os.rename(output_path, result_path)
        temp_output = result_path

        # Step 6: Read colorized image
        with open(result_path, 'rb') as f:
            colorized_bytes = f.read()

        # Step 7: Convert to base64
        colorized_base64 = base64.b64encode(colorized_bytes).decode('utf-8')

        return colorized_base64

    except ColorizationError:
        raise
    except Exception as e:
        raise ColorizationError(f"Unexpected error: {str(e)}")

    finally:
        # Cleanup: Remove temporary input file
        if temp_input and os.path.exists(temp_input):
            try:
                os.remove(temp_input)
            except Exception as e:
                print(f"Warning: Failed to delete temp file {temp_input}: {e}")