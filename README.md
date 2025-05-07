# ReColor

![ReColor Logo](FrontEnd/Images/ReColor.png)

## Colorizing Stories, Reviving Memories

ReColor is a desktop application that uses AI to breathe new life into black and white photographs. By leveraging the power of the DeOldify deep learning model, ReColor can automatically colorize historical images with remarkable accuracy, helping to revive memories and bring the past into the present.

## Features

- **AI-Powered Colorization**: Transform black and white photos into vibrant, colorized images using state-of-the-art deep learning technology
- **User-Friendly Interface**: Simple drag-and-drop functionality makes colorizing images easy for anyone
- **Customizable Settings**: Adjust render factor and choose between artistic and stable colorization models
- **Image History**: Keep track of your colorized images
- **Instant Download**: Save your colorized images directly to your device

## Installation

### Prerequisites

- Node.js and npm
- Python 3.7 or higher
- CUDA-compatible GPU (recommended for faster processing)

### Frontend Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ReColor.git
   cd ReColor/FrontEnd
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the Electron application:
   ```
   npm start
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd ../backend/model/DeOldify
   ```

2. Install the required Python packages:
   ```
   pip install flask flask-cors pillow deoldify
   ```

3. Start the Flask server:
   ```
   python app.py
   ```

## Usage

1. Launch the ReColor application
2. Click on "New" in the sidebar to start a new colorization project
3. Drag and drop a black and white image onto the upload area, or click to browse for a file
4. Click the "Colorize" button to process the image
5. View the before and after comparison
6. Download your colorized image using the download button

## Technologies Used

### Frontend
- Electron.js - Desktop application framework
- HTML/CSS/JavaScript - User interface
- SweetAlert2 - User notifications and alerts

### Backend
- Flask - Python web framework for the API
- DeOldify - Deep learning model for image colorization
- PyTorch - Deep learning framework

## Project Structure

```
ReColor/
├── FrontEnd/
│   ├── HTML/ - Application pages
│   ├── css/ - Styling
│   ├── javascript/ - Frontend logic
│   ├── Images/ - Sample images and results
│   ├── main.js - Electron main process
│   ├── preload.js - Electron preload script
│   └── package.json - Frontend dependencies
├── backend/
│   └── model/
│       └── DeOldify/
│           ├── app.py - Flask API server
│           └── deoldify_model_use.py - DeOldify model integration
└── README.md - Project documentation
```

## Settings

ReColor allows you to customize your colorization experience:

- **Render Factor**: Adjust the quality and detail of colorization (higher values produce better results but take longer to process)
- **Model Type**: Choose between "Artistic" (more vibrant but potentially less accurate colors) and "Stable" (more conservative but generally more accurate colors)
- **History**: Enable or disable saving your colorization history

## Credits

- **DeOldify**: This project uses the [DeOldify](https://github.com/jantic/DeOldify) model for image colorization
- **Author**: Franck Nasibu

## License

This project is licensed under the ISC License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the creators of DeOldify for making their amazing colorization technology available
- Special thanks to all contributors and testers who helped improve this application