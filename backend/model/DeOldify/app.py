import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend

from flask import Flask, request, jsonify
from flask_cors import CORS
from deoldify_model_use import colorize_image

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

@app.route('/colorize', methods=['POST'])
def colorize_endpoint():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image'].read()
    render_factor = int(request.form.get('render_factor', 35))
    artistic = request.form.get('artistic', 'true').lower() == 'true'  # Default to True if not provided
    image_name = request.files['image'].filename

    try:
        colorized_image_bytes = colorize_image(image_file, image_name, render_factor=render_factor, artistic=artistic)
        return jsonify({'image': colorized_image_bytes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
