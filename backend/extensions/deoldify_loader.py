"""
DeOldify model loader and initialization.
Ensures the model is loaded only once.
"""
import torch
import warnings
import logging
import os
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer

# Configure logger
logger = logging.getLogger(__name__)

# Global colorizer instance
_colorizer = None

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


def init_colorizer(use_gpu=True, gpu_id=0, artistic=True,root_folder='./'):
    """
    Initialize the DeOldify colorizer.

    Args:
        use_gpu: Whether to use GPU acceleration
        gpu_id: GPU device ID (0, 1, 2, etc.)
        artistic: Use artistic model (True) or stable model (False)
    """
    global _colorizer

    if _colorizer is not None:
        logger.info("Colorizer already initialized, skipping...")
        return

    logger.info("=" * 60)
    logger.info("Starting DeOldify colorizer initialization...")

    torch.load = _patched_torch_load
    logger.debug("Applied torch.load compatibility patch")

    # Set device
    if use_gpu and torch.cuda.is_available():
        device_id = getattr(DeviceId, f'GPU{gpu_id}')
        device.set(device=device_id)
        torch.backends.cudnn.benchmark = True
        logger.info(f"Device: GPU {gpu_id}")
        logger.info(f"  GPU Name: {torch.cuda.get_device_name(gpu_id)}")
        logger.info(f"  GPU Memory: {torch.cuda.get_device_properties(gpu_id).total_memory / 1024**3:.2f} GB")
    else:
        device.set(device=DeviceId.CPU)
        logger.info(" Device: CPU (GPU not available or disabled)")

    # Suppress warnings for cleaner output
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Suppress OpenCV warnings about missing watermark
    os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'

    # Load the colorizer
    logger.info(f"Loading {'artistic' if artistic else 'stable'} model weights...")
    logger.info(f"Model path: {root_folder}/models/")
    import time
    start_time = time.time()

    _colorizer = get_image_colorizer(artistic=artistic)

    load_time = time.time() - start_time
    logger.info(f"Model loaded successfully in {load_time:.2f}s")
    logger.info("=" * 60)

    # Restore original torch.load
    torch.load = _original_torch_load


def get_colorizer():
    """
    Get the initialized colorizer instance.

    Returns:
        The colorizer instance

    Raises:
        RuntimeError: If colorizer hasn't been initialized
    """
    if _colorizer is None:
        logger.error("Colorizer not initialized!")
        raise RuntimeError(
            "Colorizer not initialized. Call init_colorizer() first."
        )
    return _colorizer