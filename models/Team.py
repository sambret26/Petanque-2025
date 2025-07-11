from datetime import datetime

from utils.enums import TeamStatus, CategorieStatus
from database import db

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    round1 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    round2 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    round3 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    round4 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    round5 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    round6 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    round7 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    round8 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    catRound1 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    catRound2 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    catRound3 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    catRound4 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    catRound5 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    catRound6 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    catRound7 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    catRound8 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, number, round1=TeamStatus.NOT_REGISTER.value, round2=TeamStatus.NOT_REGISTER.value, round3=TeamStatus.NOT_REGISTER.value, 
                 round4=TeamStatus.NOT_REGISTER.value, round5=TeamStatus.NOT_REGISTER.value, round6=TeamStatus.NOT_REGISTER.value, 
                 round7=TeamStatus.NOT_REGISTER.value, round8=TeamStatus.NOT_REGISTER.value,
                 catRound1=CategorieStatus.NOT_REGISTER.value, catRound2=CategorieStatus.NOT_REGISTER.value,
                 catRound3=CategorieStatus.NOT_REGISTER.value, catRound4=CategorieStatus.NOT_REGISTER.value, 
                 catRound5=CategorieStatus.NOT_REGISTER.value, catRound6=CategorieStatus.NOT_REGISTER.value, 
                 catRound7=CategorieStatus.NOT_REGISTER.value, catRound8=CategorieStatus.NOT_REGISTER.value):
        self.number = number
        self.round1 = round1
        self.round2 = round2
        self.round3 = round3
        self.round4 = round4
        self.round5 = round5
        self.round6 = round6
        self.round7 = round7
        self.round8 = round8
        self.catRound1 = catRound1
        self.catRound2 = catRound2
        self.catRound3 = catRound3
        self.catRound4 = catRound4
        self.catRound5 = catRound5
        self.catRound6 = catRound6
        self.catRound7 = catRound7
        self.catRound8 = catRound8

    def toDict(self):
        return {
            "id": self.id,
            "number": self.number,
            "round1": self.round1,
            "round2": self.round2,
            "round3": self.round3,
            "round4": self.round4,
            "round5": self.round5,
            "round6": self.round6,
            "round7": self.round7,
            "round8": self.round8,
            "catRound1": self.catRound1,
            "catRound2": self.catRound2,
            "catRound3": self.catRound3,
            "catRound4": self.catRound4,
            "catRound5": self.catRound5,
            "catRound6": self.catRound6,
            "catRound7": self.catRound7,
            "catRound8": self.catRound8
        }