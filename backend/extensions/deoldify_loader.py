"""
DeOldify model loader and initialization.
Ensures the model is loaded only once.
"""
import torch
import warnings
import logging
import os
from pathlib import Path
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer, get_video_colorizer

# Configure logger
logger = logging.getLogger(__name__)

# Global colorizer instances
_image_colorizer = None
_video_colorizer = None

# Store original torch.load
_original_torch_load = torch.load


def _patched_torch_load(*args, **kwargs):
    """
    Patched torch.load that uses weights_only=False for DeOldify compatibility.
    Only use this if you trust the source of the DeOldify models.
    """
    # Set weights_only=False for backward compatibility with DeOldify
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)


def init_colorizer(use_gpu=True, gpu_id=0, artistic=True, root_folder='./'):
    """
    Initialize the DeOldify image colorizer.

    Args:
        use_gpu: Whether to use GPU acceleration
        gpu_id: GPU device ID (0, 1, 2, etc.)
        artistic: Use artistic model (True) or stable model (False)
        root_folder: Path to folder containing 'models' directory
    """
    global _image_colorizer

    if _image_colorizer is not None:
        logger.info("Image colorizer already initialized, skipping...")
        return

    logger.info("=" * 60)
    logger.info("Starting DeOldify image colorizer initialization...")

    # Monkey patch torch.load for DeOldify compatibility with PyTorch 2.6+
    torch.load = _patched_torch_load
    logger.debug("Applied torch.load compatibility patch")

    # Set device
    if use_gpu and torch.cuda.is_available():
        device_id = getattr(DeviceId, f'GPU{gpu_id}')
        device.set(device=device_id)
        torch.backends.cudnn.benchmark = True
        logger.info(f"✓ Device: GPU {gpu_id}")
        logger.info(f"  GPU Name: {torch.cuda.get_device_name(gpu_id)}")
        logger.info(f"  GPU Memory: {torch.cuda.get_device_properties(gpu_id).total_memory / 1024**3:.2f} GB")
    else:
        device.set(device=DeviceId.CPU)
        logger.info("✓ Device: CPU (GPU not available or disabled)")

    # Suppress warnings for cleaner output
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Suppress OpenCV warnings about missing watermark
    os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'

    # Convert root_folder to Path object (DeOldify expects this)
    root_path = Path(root_folder)

    # Load the image colorizer
    logger.info(f"Loading {'artistic' if artistic else 'stable'} model weights...")
    logger.info(f"Model path: {root_path}/models/")
    import time
    start_time = time.time()

    _image_colorizer = get_image_colorizer(artistic=artistic, root_folder=root_path)

    load_time = time.time() - start_time
    logger.info(f"✓ Image model loaded successfully in {load_time:.2f}s")
    logger.info("=" * 60)

    # Restore original torch.load
    torch.load = _original_torch_load


def init_video_colorizer(use_gpu=True, gpu_id=0, root_folder='./'):
    """
    Initialize the DeOldify video colorizer.

    Args:
        use_gpu: Whether to use GPU acceleration
        gpu_id: GPU device ID (0, 1, 2, etc.)
        root_folder: Path to folder containing 'models' directory
    """
    global _video_colorizer

    if _video_colorizer is not None:
        logger.info("Video colorizer already initialized, skipping...")
        return

    logger.info("=" * 60)
    logger.info("Starting DeOldify video colorizer initialization...")

    # Monkey patch torch.load
    torch.load = _patched_torch_load

    # Set device (same as image colorizer)
    if use_gpu and torch.cuda.is_available():
        device_id = getattr(DeviceId, f'GPU{gpu_id}')
        device.set(device=device_id)
        torch.backends.cudnn.benchmark = True
        logger.info(f"✓ Device: GPU {gpu_id}")
    else:
        device.set(device=DeviceId.CPU)
        logger.info("✓ Device: CPU")

    # Suppress warnings
    warnings.filterwarnings("ignore")
    os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'

    # Set TORCH_HOME environment variable to point to model directory
    # This tells PyTorch/DeOldify where to look for cached models
    root_path = Path(root_folder)
    torch_home = root_path / 'models'
    os.environ['TORCH_HOME'] = str(torch_home)
    logger.info(f"Set TORCH_HOME to: {torch_home}")

    # Load the video colorizer
    logger.info(f"Loading video model weights...")
    import time
    start_time = time.time()

    _video_colorizer = get_video_colorizer()

    load_time = time.time() - start_time
    logger.info(f"✓ Video model loaded successfully in {load_time:.2f}s")
    logger.info("=" * 60)

    # Restore original torch.load
    torch.load = _original_torch_load


def get_colorizer():
    """
    Get the initialized image colorizer instance.

    Returns:
        The image colorizer instance

    Raises:
        RuntimeError: If colorizer hasn't been initialized
    """
    if _image_colorizer is None:
        logger.error("Image colorizer not initialized!")
        raise RuntimeError(
            "Image colorizer not initialized. Call init_colorizer() first."
        )
    return _image_colorizer


def get_video_colorizer_instance():
    """
    Get the initialized video colorizer instance.

    Returns:
        The video colorizer instance

    Raises:
        RuntimeError: If video colorizer hasn't been initialized
    """
    if _video_colorizer is None:
        logger.error("Video colorizer not initialized!")
        raise RuntimeError(
            "Video colorizer not initialized. Call init_video_colorizer() first."
        )
    return _video_colorizer