import os
import sys
from flask import Flask, request, jsonify
from pypdf import PdfReader
import json
from resumeparsermain import parserfn
from flask_cors import CORS

sys.path.insert(0, os.path.abspath(os.getcwd()))

UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process', methods=['POST'])
def ats():
    doc = request.files['pdf_doc']
    doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    data = _read_file_from_path(doc_path)
    data = parserfn(data)
    print("Parsed data:", data)  # Debug print statement
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return jsonify({"error": "Failed to parse JSON data"}), 400
    return jsonify(json_data)


def _read_file_from_path(path):
    reader = PdfReader(path)
    data = ""
    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no]
        data += page.extract_text()
    return data

if __name__ == "__main__":
    app.run(port=8000, debug=True)
