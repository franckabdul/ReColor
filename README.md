# ReColor


## Colorizing Stories, Reviving Memories

ReColor is a professional desktop application that uses AI to breathe new life into black and white photographs and videos. By leveraging the power of the DeOldify deep learning model, ReColor can automatically colorize historical media with remarkable accuracy, helping to revive memories and bring the past into the present.

##  Features

- **AI-Powered Colorization**: Transform black and white photos and videos into vibrant, colorized media using state-of-the-art deep learning technology
- **Image & Video Support**: Colorize both static images and video files
- **User-Friendly Interface**: Simple drag-and-drop functionality makes colorizing media easy for anyone
- **Customizable Settings**: Adjust render factor and choose between artistic and stable colorization models
- **Real-Time Progress Tracking**: Monitor colorization progress with detailed timing information
- **Comprehensive Logging**: Track all operations with detailed logs for debugging and analysis
- **RESTful API**: Well-structured backend API for integration with other applications
- **Instant Download**: Save your colorized media directly to your device

## Supported Formats

### Images
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)

### Videos
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WebM (.webm)

## Prerequisites

- **Node.js**: v14.0 or higher
- **Python**: 3.8 - 3.13
- **Anaconda/Miniconda**: Recommended for Python environment management
- **GPU**: CUDA-compatible GPU recommended for faster processing (CPU mode available)
- **Storage**: At least 2GB free space for models and processed files

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/franckabdul/ReColor.git
cd ReColor
```

### 2. Backend Setup

#### Create Python Environment

```bash
# Create a new conda environment
conda create -n ReColor python=3.13
conda activate ReColor
```

#### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Download Model Weights

Create a `models` directory and download the required model files:

```bash
mkdir -p models
cd models

# Download image colorization model (artistic)
wget https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth

# Optional: Download stable model
# wget https://data.deepai.org/deoldify/ColorizeStable_gen.pth

# Download video colorization model
wget https://data.deepai.org/deoldify/ColorizeVideo_gen.pth

cd ..
```

Alternatively, download manually from:
- [ColorizeArtistic_gen.pth](https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth)
- [ColorizeVideo_gen.pth](https://data.deepai.org/deoldify/ColorizeVideo_gen.pth)

#### Configure Environment (Optional)

Create a `.env` file in the `backend` directory:

```bash
# .env
TORCH_HOME=/path/to/ReColor/backend/models
FLASK_ENV=development
USE_GPU=True
GPU_DEVICE_ID=0
```

Or create an instance configuration at `backend/instance/config.py`:

```python
# instance/config.py
USE_GPU = False  # Set to True if you have a CUDA-compatible GPU
OUTPUT_FOLDER = 'results'
VIDEO_OUTPUT_FOLDER = 'results/videos'
DEFAULT_RENDER_FACTOR = 35
VIDEO_RENDER_FACTOR = 21
```

#### Start the Backend Server

```bash
python3 app.py
```

The backend will start on `http://localhost:5000`

You should see output like:
```
[02:39:38] INFO     Starting ReColor Media Colorization Service
[02:39:44] INFO     Device: CPU (GPU not available or disabled)
[02:39:44] INFO     Image model loaded successfully in 2.45s
[02:39:46] INFO     Video model loaded successfully in 2.12s
[02:39:46] INFO     Application initialization complete
```

### 3. Frontend Setup

```bash
cd ../frontend/electron-app
npm install
```

#### Start the Electron Application

```bash
npm start
```

## Usage

### Image Colorization

1. Launch the ReColor application
2. Click on "New" in the sidebar to start a new project
3. Drag and drop a black and white image onto the upload area, or click to browse
4. Adjust the render factor (10-40) for quality vs. speed tradeoff
5. Click the "Colorize" button to process the image
6. View the before and after comparison
7. Download your colorized image using the download button

### Video Colorization

1. Select a video file (MP4, AVI, MOV, MKV, or WebM)
2. Set the render factor (recommended: 21 for videos)
3. Click "Colorize" and wait for processing
4. Progress will be displayed with timing information
5. Download the colorized video when complete

### API Usage

#### Colorize an Image

```bash
curl -X POST http://localhost:5000/colorize/image \
  -F "image=@path/to/image.jpg" \
  -F "render_factor=35"
```

Response:
```json
{
  "success": true,
  "data": {
    "image": "base64_encoded_image_data...",
    "filename": "image_colorized.jpg",
    "processing_time": 15.23,
    "total_request_time": 15.45,
    "step_times": {
      "load_image": 0.125,
      "save_temp": 0.089,
      "colorize": 14.876,
      "verify": 0.012,
      "move_file": 0.023,
      "encode": 0.105
    }
  }
}
```

#### Colorize a Video

```bash
curl -X POST http://localhost:5000/colorize/video \
  -F "video=@path/to/video.mp4" \
  -F "render_factor=21"
```

Response:
```json
{
  "success": true,
  "data": {
    "filename": "video_colorized.mp4",
    "video_path": "/path/to/results/videos/video_colorized.mp4",
    "processing_time": 245.67,
    "total_request_time": 246.12,
    "output_size_mb": 15.34,
    "download_url": "/download/video/video_colorized.mp4"
  }
}
```

#### Download Colorized Video

```bash
curl -O http://localhost:5000/download/video/video_colorized.mp4
```

#### Health Check

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "models_loaded": true
  }
}
```

## 🏗️ Project Structure

```
ReColor/
│
├── backend/
│   ├── app.py                      # Application factory
│   ├── wsgi.py                     # Production WSGI entry point
│   ├── config.py                   # Configuration classes
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── extensions/
│   │   └── deoldify_loader.py      # Model initialization & management
│   │
│   ├── services/
│   │   ├── deoldify_service.py     # Image colorization logic
│   │   └── video_service.py        # Video colorization logic
│   │
│   ├── routes/
│   │   └── media_routes.py         # API endpoints (images & videos)
│   │
│   ├── utils/
│   │   └── responses.py            # JSON response helpers
│   │
│   ├── models/                     # Model weights & cached models
│   │   ├── ColorizeArtistic_gen.pth    # Artistic image model
│   │   ├── ColorizeStable_gen.pth      # Stable image model
│   │   ├── ColorizeVideo_gen.pth       # Video colorization model
│   │   └── hub/
│   │       └── checkpoints/            # Cached PyTorch models
│   │
│   ├── results/                    # Colorized output files
│   │   ├── *.jpg                       # Colorized images
│   │   └── videos/                     # Colorized videos
│   │
│   ├── logs/                       # Application logs
│   │   └── colorization.log
│   │
│   ├── video/                      # Temporary video processing
│   │   └── bwframes/                   # Extracted video frames
│   │
│   ├── static/                     # Static assets (if needed)
│   └── result_images/              # Legacy result directory
│
└── frontend/
    ├── main.js                     # Electron main process
    ├── preload.js                  # Electron preload script
    ├── package.json                # Node.js dependencies
    ├── package-lock.json           # Dependency lock file
    │
    ├── HTML/                       # Application pages
    │   ├── index.html                  # Main page
    │   ├── new.html                    # New colorization page
    │   ├── history.html                # History page
    │   ├── settings.html               # Settings page
    │   └── help.html                   # Help page
    │
    ├── css/                        # Stylesheets
    │   ├── style.css                   # Global styles
    │   ├── home.css                    # Home page styles
    │   ├── new.css                     # New page styles
    │   ├── history.css                 # History page styles
    │   ├── settings.css                # Settings page styles
    │   └── help.css                    # Help page styles
    │
    ├── javascript/                 # Frontend logic
    │   ├── script.js                   # Global scripts
    │   ├── index.js                    # Home page logic
    │   ├── new.js                      # Colorization logic
    │   ├── history.js                  # History management
    │   ├── settings.js                 # Settings management
    │   └── help.js                     # Help page logic
    │
    ├── Images/                     # Sample images & assets
    │   ├── ReColor.png                 # Application logo
    │   ├── Black and white/            # Sample B&W images
    │   │   ├── 16 year old woman in 1943.jpg
    │   │   ├── American family 1954.jpg
    │   │   ├── boys.jpg
    │   │   ├── couple portrait 1940.jpg
    │   │   └── ... (more samples)
    │   └── Result/                     # Sample colorized results
    │       ├── 16 year old woman in 1943.jpg
    │       ├── American family 1954.jpg
    │       └── ... (more results)
    │
    └── config/                     # Configuration files
        └── config.json                 # Frontend configuration
```

## ⚙Configuration

### Render Factor Guidelines

**Images:**
- **10-20**: Fast processing, lower quality, good for testing
- **25-35**: Balanced quality and speed (recommended: 35)
- **35-40**: Highest quality, slower processing

**Videos:**
- **10-15**: Fast processing, acceptable quality
- **18-24**: Balanced (recommended: 21)
- **25-30**: Higher quality, significantly slower

### Model Types

- **Artistic**: More vibrant, saturated colors. Best for creative projects and artistic expression
- **Stable**: More conservative, historically accurate colors. Best for archival and documentary work

### GPU vs CPU

- **GPU**: 10-50x faster processing, recommended for videos and batch processing
- **CPU**: Slower but works on any system, sufficient for occasional image colorization

## Logging

ReColor includes comprehensive logging:

- **Console Logs**: Real-time progress and status updates
- **File Logs**: Detailed logs saved to `backend/logs/colorization.log`
- **Log Rotation**: Automatic rotation at 10MB with 5 backup files

Log levels:
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages for non-critical issues
- `ERROR`: Error messages for failures

## Technologies Used

### Backend
- **Flask 3.0+**: Lightweight Python web framework
- **DeOldify**: State-of-the-art colorization models
- **PyTorch 2.0+**: Deep learning framework
- **FastAI 2.7+**: High-level deep learning library
- **OpenCV**: Video processing and frame extraction
- **Pillow**: Image processing

### Frontend
- **Electron.js**: Cross-platform desktop application framework
- **HTML/CSS/JavaScript**: User interface
- **SweetAlert2**: Beautiful alerts and notifications

## Troubleshooting

### Model Loading Issues

**Problem**: `FileNotFoundError: models/ColorizeArtistic_gen.pth`

**Solution**: Download the model files and place them in `backend/models/`

### PyTorch Compatibility

**Problem**: `pickle.UnpicklingError: Weights only load failed`

**Solution**: The code includes a compatibility patch for PyTorch 2.6+. This is handled automatically.

### GPU Not Detected

**Problem**: Running on CPU despite having a GPU

**Solution**:
1. Ensure CUDA is installed: `nvidia-smi`
2. Install PyTorch with CUDA support:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```
3. Set `USE_GPU=True` in config

### OpenCV Watermark Warning

**Problem**: `WARN global loadsave.cpp:275 findDecoder imread_('./resource_images/watermark.png')`

**Solution**: This warning is automatically suppressed by setting `OPENCV_LOG_LEVEL='ERROR'`

### Large Video Processing

**Problem**: Video processing takes too long or runs out of memory

**Solution**:
- Lower the render factor (try 15-18)
- Process shorter clips
- Use GPU if available
- Increase system swap space

## 🚀 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:application
```

### Using Docker (Coming Soon)

```bash
docker build -t recolor-backend .
docker run -p 5000:5000 recolor-backend
```

## License

This project is licensed under the ISC License - see the LICENSE file for details.

## Acknowledgments

- **DeOldify**: This project uses the [DeOldify](https://github.com/jantic/DeOldify) model created by Jason Antic for image and video colorization
- **FastAI**: Built on top of the FastAI deep learning library
- **PyTorch**: Powered by PyTorch for deep learning capabilities

## Author

**Franck Nasibu**

## Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

