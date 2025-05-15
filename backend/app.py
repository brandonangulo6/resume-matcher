from flask import Flask, request, jsonify
from flask_cors import CORS
from matcher import get_match_score
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)  # Allows frontend to talk to API

@app.route('/match', methods=['POST'])
def match():
    data = request.json
    resume = data.get("resume", "")
    job = data.get("job", "")

    if not resume or not job:
        return jsonify({"error": "Missing resume or job text"}), 400

    score = get_match_score(resume, job)
    return jsonify({"match_score": round(score, 4)})

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File is not a PDF"}), 400

    try:
        pdf_bytes = file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        job = request.form.get("job", "")
        if not job:
            return jsonify({"error": "Missing job description"}), 400

        score = get_match_score(text, job)
        return jsonify({"match_score": round(score, 4)})

    except Exception as e:
        return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)