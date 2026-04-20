from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Candidate
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def calculate_score(data):
    education_scores = {
        "secondary": 1,
        "diploma": 2,
        "bachelor": 3,
        "bachelor_edu": 4,
        "master": 5,
        "phd": 6
    }

    score = (
        education_scores.get(data["education"], 0) * 0.3 +
        data["experience"] * 0.2 +
        data["interview_score"] * 0.3 +
        data["technical_score"] * 0.2
    )

    return round(score, 2)

@app.route("/add_candidate", methods=["POST"])
def add_candidate():
    data = request.json
    score = calculate_score(data)

    candidate = Candidate(
        name=data["name"],
        education=data["education"],
        experience=data["experience"],
        interview_score=data["interview_score"],
        technical_score=data["technical_score"],
        score=score
    )

    db.session.add(candidate)
    db.session.commit()

    return jsonify({"message": "Candidate added", "score": score})

@app.route("/get_candidates", methods=["GET"])
def get_candidates():
    candidates = Candidate.query.all()

    return jsonify([
        {
            "name": c.name,
            "education": c.education,
            "score": c.score
        } for c in candidates
    ])

@app.route("/")
def home():
    return "SmartComp AI Backend Running 🚀"

if __name__ == "__main__":
    app.run(debug=True)
