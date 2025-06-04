# web-gallery/backend/app.py
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/media/usb'
app = Flask(__name__)
CORS(app)  # <---- přidá CORS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/media')
def list_media():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        files = [f for f in files if not f.startswith('._')]  # filtr skrytých macOS
        files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
        start = int(request.args.get('start', 0))
        count = int(request.args.get('count', 5))
        return jsonify(files[start:start+count])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/media/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'File uploaded', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
