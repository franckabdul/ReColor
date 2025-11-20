"""
DeOldify model loader and initialization.
Ensures the model is loaded only once.
"""
import torch
import warnings
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer


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


def init_colorizer(use_gpu=True, gpu_id=0, artistic=True):
    """
    Initialize the DeOldify colorizer.

    Args:
        use_gpu: Whether to use GPU acceleration
        gpu_id: GPU device ID (0, 1, 2, etc.)
        artistic: Use artistic model (True) or stable model (False)
    """
    global _colorizer

    if _colorizer is not None:
        return  # Already initialized

    # Monkey patch torch.load for DeOldify compatibility with PyTorch 2.6+
    torch.load = _patched_torch_load

    # Set device
    if use_gpu and torch.cuda.is_available():
        device_id = getattr(DeviceId, f'GPU{gpu_id}')
        device.set(device=device_id)
        torch.backends.cudnn.benchmark = True
        print(f"DeOldify initialized on GPU {gpu_id}")
    else:
        device.set(device=DeviceId.CPU)
        print("DeOldify initialized on CPU")

    # Suppress warnings for cleaner output
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Load the colorizer
    _colorizer = get_image_colorizer(artistic=artistic)
    print(f"Colorizer loaded (artistic={artistic})")

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
        raise RuntimeError(
            "Colorizer not initialized. Call init_colorizer() first."
        )
    return _colorizer