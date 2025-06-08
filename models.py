from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answers = db.Column(db.JSON)
    raw_score = db.Column(db.Float)
    standard_score = db.Column(db.Float)
    risk_group = db.Column(db.String(50))
    user_data = db.Column(db.JSON)  # Store user data as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Result {self.id}>' 