from sqlalchemy import desc

from utils.enums import MatchStatus
from models.Match import Match
from database import db

class MatchsRepository:
    
    # GETTERS
    @staticmethod
    def getAllMatches():
        matchs = Match.query.order_by(desc(Match.status), Match.team1).all()
        return [match.toDict() for match in matchs]
    
    @staticmethod
    def getMatches(panel):
        matchs = Match.query.filter(Match.panel == panel).order_by(desc(Match.status), Match.team1).all()
        return [match.toDict() for match in matchs]

    @staticmethod
    def getById(id):
        return Match.query.filter(Match.id == id).first()

    @staticmethod
    def getNotLaunched(panel):
        return Match.query.filter(Match.panel == panel, Match.status == 0).all()

    # INSERT
    @staticmethod
    def insertMatch(match):
        db.session.add(match)
        db.session.commit()

    @staticmethod
    def insertMatchs(matchs):
        db.session.add_all(matchs)
        db.session.commit()

    # UPDATE
    @staticmethod
    def startMatch(id):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.IN_PROGRESS.value})
        db.session.commit()

    @staticmethod
    def launchMatches(ids):
        Match.query.filter(Match.id.in_(ids)).update({"status": MatchStatus.IN_PROGRESS.value})
        db.session.commit()

    @staticmethod
    def stopMatch(id):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.CREATED.value, "winner": 0})
        db.session.commit()

    @staticmethod
    def setWinner(id, winner):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.COMPLETED.value, "winner": winner})
        db.session.commit()

    @staticmethod
    def unsetWinner(id):
        Match.query.filter(Match.id == id).update({"status": MatchStatus.IN_PROGRESS.value, "winner": 0})
        db.session.commit()

    # DELETE
    @staticmethod
    def deleteMatch(id):
        Match.query.filter(Match.id == id).delete()
        db.session.commit()

    @staticmethod
    def deleteMatchs(matchsIds):
        Match.query.filter(Match.id.in_(matchsIds)).delete()
        db.session.commit()

    @staticmethod
    def deleteAll():
        Match.query.delete()
        db.session.commit()