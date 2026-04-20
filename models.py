models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    education = db.Column(db.String(50))
    experience = db.Column(db.Float)
    interview_score = db.Column(db.Float)
    technical_score = db.Column(db.Float)
    score = db.Column(db.Float)
