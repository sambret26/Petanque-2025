from datetime import datetime

from utils.enums import MatchStatus
from database import db

class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team1 = db.Column(db.Integer)
    team2 = db.Column(db.Integer)
    panel = db.Column(db.Integer)
    status = db.Column(db.Integer, default=MatchStatus.CREATED.value)
    winner = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, team1, team2, panel, winner=0, status=MatchStatus.CREATED.value):
        self.team1 = team1
        self.team2 = team2
        self.panel = panel
        self.winner = winner
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "team1": self.team1,
            "team2": self.team2,
            "panel": self.panel,
            "status": self.status,
            "winner": self.winner,
        }