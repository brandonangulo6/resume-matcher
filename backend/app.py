from flask import Flask, request, jsonify
from flask_cors import CORS
from matcher import get_match_score

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

if __name__ == "__main__":
    app.run(debug=True)