from sqlalchemy import desc

from utils.enums import MatchStatus
from models.Match import Match
from database import db

class MatchsRepository:
    
    # GETTERS
    @staticmethod
    def get_all():
        matchs = Match.query.order_by(desc(Match.status), Match.team1).all()
        return [match.to_dict() for match in matchs]
    
    @staticmethod
    def get_by_panel(panel):
        matchs = Match.query.filter(Match.panel == panel).order_by(desc(Match.status), Match.team1).all()
        return [match.to_dict() for match in matchs]

    @staticmethod
    def get_by_id(id):
        return Match.query.filter(Match.id == id).first()

    @staticmethod
    def get_not_launched(panel):
        return Match.query.filter(Match.panel == panel, Match.status == 0).all()

    # INSERT
    @staticmethod
    def insert_match(match):
        db.session.add(match)
        db.session.commit()

    @staticmethod
    def insert_matchs(matchs):
        db.session.add_all(matchs)
        db.session.commit()

    # UPDATE
    @staticmethod
    def start_match(id):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.IN_PROGRESS.value})
        db.session.commit()

    @staticmethod
    def launch_matches(ids):
        Match.query.filter(Match.id.in_(ids)).update({"status": MatchStatus.IN_PROGRESS.value})
        db.session.commit()

    @staticmethod
    def stop_match(id):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.CREATED.value, "winner": 0})
        db.session.commit()

    @staticmethod
    def set_winner(id, winner):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.COMPLETED.value, "winner": winner})
        db.session.commit()

    @staticmethod
    def unset_winner(id):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.IN_PROGRESS.value, "winner": 0})
        db.session.commit()

    # DELETE
    @staticmethod
    def delete_match(id):
        Match.query.filter(Match.id == id).delete()
        db.session.commit()

    @staticmethod
    def delete_matchs(ids):
        Match.query.filter(Match.id.in_(ids)).delete()
        db.session.commit()

    @staticmethod
    def delete_all():
        Match.query.delete()
        db.session.commit()