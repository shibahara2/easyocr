import easyocr
from flask import Flask, request, jsonify, Response
from pdf2image import convert_from_bytes
from PIL import Image
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to EasyOCR server.\n'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    uploaded_file = request.files['file']
    filename = uploaded_file.filename.lower()

    if filename.endswith('.pdf'):
        images = convert_from_bytes(uploaded_file.read())
    elif filename.endswith('.png') or filename.endswith('.jpg'):
        image = Image.open(uploaded_file.stream)
        images = [image]
    else:
        return jsonify({'error': 'Unsupported file type'}), 415

    results = {}
    reader = easyocr.Reader(['en'])
    for i, image in enumerate(images):
        text = reader.readtext(image, detail = 0)
        results['page-' + str(i+1)] = text

    return Response(json.dumps(results, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556)
