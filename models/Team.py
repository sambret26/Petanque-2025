from datetime import datetime

from utils.enums import TeamStatus, CategorieStatus
from database import db

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    stage1 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    stage2 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    stage3 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    stage4 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    stage5 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    stage6 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    stage7 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    stage8 = db.Column(db.Integer, default=TeamStatus.NOT_REGISTER.value)
    cat_stage1 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    cat_stage2 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    cat_stage3 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    cat_stage4 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    cat_stage5 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    cat_stage6 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    cat_stage7 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    cat_stage8 = db.Column(db.Integer, default=CategorieStatus.NOT_REGISTER.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, number, stage1=TeamStatus.NOT_REGISTER.value, cat_stage1=CategorieStatus.NOT_REGISTER.value):
        self.number = number
        self.stage1 = stage1
        self.stage2 = TeamStatus.NOT_REGISTER.value
        self.stage3 = TeamStatus.NOT_REGISTER.value
        self.stage4 = TeamStatus.NOT_REGISTER.value
        self.stage5 = TeamStatus.NOT_REGISTER.value
        self.stage6 = TeamStatus.NOT_REGISTER.value
        self.stage7 = TeamStatus.NOT_REGISTER.value
        self.stage8 = TeamStatus.NOT_REGISTER.value
        self.cat_stage1 = cat_stage1
        self.cat_stage2 = CategorieStatus.NOT_REGISTER.value
        self.cat_stage3 = CategorieStatus.NOT_REGISTER.value
        self.cat_stage4 = CategorieStatus.NOT_REGISTER.value
        self.cat_stage5 = CategorieStatus.NOT_REGISTER.value
        self.cat_stage6 = CategorieStatus.NOT_REGISTER.value
        self.cat_stage7 = CategorieStatus.NOT_REGISTER.value
        self.cat_stage8 = CategorieStatus.NOT_REGISTER.value

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "stage1": self.stage1,
            "stage2": self.stage2,
            "stage3": self.stage3,
            "stage4": self.stage4,
            "stage5": self.stage5,
            "stage6": self.stage6,
            "stage7": self.stage7,
            "stage8": self.stage8,
            "cat_stage1": self.cat_stage1,
            "cat_stage2": self.cat_stage2,
            "cat_stage3": self.cat_stage3,
            "cat_stage4": self.cat_stage4,
            "cat_stage5": self.cat_stage5,
            "cat_stage6": self.cat_stage6,
            "cat_stage7": self.cat_stage7,
            "cat_stage8": self.cat_stage8
        }