import os
import torch
import tempfile
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *
import io
from PIL import Image
import warnings
import base64

# Set up the device for GPU
device.set(device=DeviceId.GPU0)
torch.backends.cudnn.benchmark = True

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

def colorize_image(image_bytes, file_name, render_factor=35, artistic=True):
    print("Starting colorize_image function.")

    if artistic:
        print("Artistic mode enabled.")
    else:
        print("Artistic mode disabled.")
    
    # Create a temporary directory and file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_path = temp_file.name
        try:
            # Load image from bytes
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            print("Image loaded successfully.")
            
            # Save temporary file
            image.save(temp_path)
            print(f"Image saved temporarily at {temp_path}.")
            
            # Define the result path
            result_dir = 'results'
            result_filename = os.path.splitext(file_name)[0] + "_colorized.jpg"
            result_path = os.path.join(result_dir, result_filename)
            
            # Ensure the results directory exists
            os.makedirs(result_dir, exist_ok=True)
            print(f"Results directory '{result_dir}' ensured.")
            
            # Initialize the colorizer with the specified artistic value
            colorizer = get_image_colorizer(artistic=artistic)
            
            # Process the image
            output_path = colorizer.plot_transformed_image(path=temp_path, render_factor=render_factor, compare=False)
            print(f"Image processing completed. Output path: {output_path}")
            
            # Move the processed image to the expected results directory
            if os.path.exists(output_path):
                os.rename(output_path, result_path)
                print(f"Colorized image moved to {result_path}")
            else:
                raise FileNotFoundError(f"Processed image not found at {output_path}")
            
            # Load the result image
            with open(result_path, 'rb') as f:
                colorized_image_bytes = f.read()
                print("Colorized image loaded successfully.")
        
        finally:
            # Delete the temporary file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    print(f"Temporary file {temp_path} deleted.")
                except Exception as e:
                    print(f"Failed to delete temporary file: {e}")
    
    # Convert to base64
    colorized_image_base64 = base64.b64encode(colorized_image_bytes).decode('utf-8')
    
    return colorized_image_base64
