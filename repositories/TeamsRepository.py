from sqlalchemy import desc, asc

from utils.enums import TeamStatus
from models.Team import Team
from database import db

class TeamsRepository:
    
    # GETTERS
    @staticmethod
    def getByNumber(number):
        return Team.query.filter(Team.number == number).first()

    @staticmethod
    def getWaitings(round, cat): 
        numbers = Team.query.with_entities(Team.number).filter(getattr(Team, f'round{round}') == 1, getattr(Team, f'catRound{round}') == cat).order_by(Team.updated_at.asc()).all()
        return [number[0] for number in numbers]

    @staticmethod
    def getTeamsWaitings(round, cat):
        teams = Team.query.filter(getattr(Team, f'round{round}') == 1, getattr(Team, f'catRound{round}') == cat).all()
        return teams

    @staticmethod
    def getAllWaitings():
        teams = Team.query.all()
        return [team.toDict() for team in teams]

    @staticmethod
    def getMaxTeamNumber():
        return Team.query.with_entities(Team.number).order_by(Team.number.desc()).first()

    @staticmethod
    def count():
        return Team.query.count()

    # INSERT    
    @staticmethod
    def insertTeams(teams):
        db.session.add_all(teams)
        db.session.commit()

    # UPDATE
    @staticmethod
    def unregisterTeams(teamsNumbers, round_number):
        Team.query.filter(Team.number.in_(teamsNumbers)).update({f'round{round_number}': 1})
        db.session.commit()

    @staticmethod
    def updateTeams(teams):
        for team in teams:
            db.session.merge(team)
        db.session.commit()

    @staticmethod
    def updateTeamsStatus(teamsNumbers, round_number):
        Team.query.filter(Team.number.in_(teamsNumbers)).update({f'round{round_number}': TeamStatus.AFFECTED.value})
        db.session.commit()
    
    # DELETE
    @staticmethod
    def deleteTeam(team):
        db.session.delete(team)
        db.session.commit()

    @staticmethod
    def deleteAll():
        Team.query.delete()
        db.session.commit()