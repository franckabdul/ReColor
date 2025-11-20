"""
Business logic for video colorization.
Pure Python - no Flask dependencies.
"""
import os
import tempfile
import time
import logging
import shutil
import torch
import functools

# Configure torch safe globals for DeOldify compatibility
torch.serialization.add_safe_globals([functools.partial])

# Configure logger
logger = logging.getLogger(__name__)


class VideoColorizationError(Exception):
    """Custom exception for video colorization errors."""
    pass


def ensure_ffmpeg():
    """Return path to ffmpeg executable or raise VideoColorizationError with instructions."""
    # Try imageio-ffmpeg provided executable
    try:
        import imageio_ffmpeg as _iioff
        exe = _iioff.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback to system ffmpeg on PATH
    exe = shutil.which('ffmpeg')
    if exe:
        return exe

    # Not found -> raise clear error
    raise VideoColorizationError(
        "ffmpeg not found. Install system ffmpeg (e.g. `sudo apt install ffmpeg`), "
        "or install the Python package `imageio-ffmpeg` (`pip install imageio-ffmpeg`) "
        "or add ffmpeg to the PATH."
    )


def get_video_colorizer_instance():
    """Get DeOldify video colorizer instance."""
    try:
        # Adjust import path based on your project structure
        from deoldify import device
        from deoldify.visualize import get_video_colorizer

        # Ensure ffmpeg is available before initializing colorizer
        ensure_ffmpeg()

        # Use context manager for safe globals during model loading
        with torch.serialization.safe_globals([functools.partial]):
            return get_video_colorizer(render_factor=21)

    except ImportError as e:
        raise VideoColorizationError(f"DeOldify not properly installed: {e}")
    except Exception as e:
        raise VideoColorizationError(f"Failed to initialize video colorizer: {e}")


def colorize_video(
        video_bytes: bytes,
        filename: str,
        render_factor: int = 21,
        output_dir: str = 'results/videos'
) -> dict:
    """
    Colorize a grayscale video.

    Args:
        video_bytes: Raw video bytes
        filename: Original filename (for naming output)
        render_factor: Quality factor (10-40, higher = better quality but slower)
        output_dir: Directory to save colorized videos

    Returns:
        Dictionary containing:
            - video_path: Path to colorized video file
            - processing_time: Time taken in seconds
            - frame_count: Number of frames processed
            - fps: Frames per second of original video

    Raises:
        VideoColorizationError: If colorization fails
        ValueError: If input parameters are invalid
    """
    start_time = time.time()

    logger.info("=" * 60)
    logger.info(f"Starting video colorization for: {filename}")
    logger.info(f"Render factor: {render_factor}")
    logger.info(f"Input size: {len(video_bytes) / 1024 / 1024:.2f} MB")

    # Validate inputs
    if not video_bytes:
        logger.error("Empty video bytes received")
        raise ValueError("Video bytes cannot be empty")

    if not 10 <= render_factor <= 40:
        logger.warning(f"Invalid render factor {render_factor}, must be 10-40")
        raise ValueError("Render factor must be between 10 and 40")

    # Ensure ffmpeg is available
    try:
        ffmpeg_path = ensure_ffmpeg()
        logger.info(f"Using ffmpeg at: {ffmpeg_path}")
    except VideoColorizationError as e:
        logger.error(str(e))
        raise

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    temp_input = None

    try:
        # Step 1: Save to temporary file
        step_start = time.time()
        logger.info("Step 1/3: Creating temporary input file...")

        file_ext = os.path.splitext(filename)[1].lower()
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_ext,
                mode='wb'
        ) as temp_file:
            temp_input = temp_file.name
            temp_file.write(video_bytes)
            logger.info(f"  ✓ Temp file: {temp_input}")

        save_time = time.time() - step_start
        logger.debug(f"  Time: {save_time:.3f}s")

        # Step 2: Process with DeOldify
        step_start = time.time()
        logger.info("Step 2/3: Running DeOldify video colorization...")
        logger.info(f"  This may take several minutes depending on video length...")

        try:
            colorizer = get_video_colorizer_instance()

            # Generate output filename
            base_name = os.path.splitext(filename)[0]
            output_filename = f"{base_name}_colorized.mp4"

            # DeOldify will save to result_path
            result_path = colorizer.colorize_from_file_name(
                file_name=temp_input,
                render_factor=render_factor
            )

            logger.info(f"  ✓ Colorization complete")
            logger.info(f"  Output: {result_path}")

        except Exception as e:
            logger.error(f"  ✗ Video colorization failed: {str(e)}")
            raise VideoColorizationError(f"Video colorization failed: {str(e)}")

        colorize_time = time.time() - step_start
        logger.info(f"  Time: {colorize_time:.2f}s")

        # Step 3: Move to final location
        step_start = time.time()
        logger.info("Step 3/3: Moving to results directory...")

        final_path = os.path.join(output_dir, output_filename)

        if os.path.exists(result_path):
            # Move the file
            os.rename(result_path, final_path)
            logger.info(f"  ✓ Saved: {final_path}")
        else:
            raise VideoColorizationError(f"Output video not found at {result_path}")

        move_time = time.time() - step_start
        logger.debug(f"  Time: {move_time:.3f}s")

        # Get video info
        output_size = os.path.getsize(final_path)

        # Calculate total time
        total_time = time.time() - start_time

        logger.info("-" * 60)
        logger.info(f"✓ VIDEO COLORIZATION SUCCESSFUL")
        logger.info(f"  Total time: {total_time:.2f}s ({total_time/60:.1f} minutes)")
        logger.info(f"  Output size: {output_size / 1024 / 1024:.2f} MB")
        logger.info(f"  Output path: {final_path}")
        logger.info("=" * 60)

        return {
            'video_path': final_path,
            'filename': output_filename,
            'processing_time': round(total_time, 2),
            'output_size_mb': round(output_size / 1024 / 1024, 2)
        }

    except VideoColorizationError:
        logger.error(f"Video colorization error after {time.time() - start_time:.2f}s")
        raise
    except Exception as e:
        logger.error(f"Unexpected error after {time.time() - start_time:.2f}s: {str(e)}")
        raise VideoColorizationError(f"Unexpected error: {str(e)}")

    finally:
        # Cleanup: Remove temporary input file
        if temp_input and os.path.exists(temp_input):
            try:
                os.remove(temp_input)
                logger.debug(f"Cleaned up temp file: {temp_input}")
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_input}: {e}")