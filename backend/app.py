from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.answer_generator import generate_answer

app = Flask(__name__)
CORS(app)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

    if not question:
        return jsonify({"answer": "Please ask a valid question."})

    answer = generate_answer(question)
    return jsonify(answer)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
