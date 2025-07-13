from sqlalchemy import desc, asc

from utils.enums import TeamStatus
from models.Team import Team
from database import db

class TeamsRepository:
    
    # GETTERS
    @staticmethod
    def get_by_number(number):
        return Team.query.filter(Team.number == number).first()

    @staticmethod
    def get_waitings(stage, cat): 
        numbers = Team.query.with_entities(Team.number).filter(getattr(Team, f'stage{stage}') == 1, getattr(Team, f'cat_stage{stage}') == cat).order_by(Team.updated_at.asc()).all()
        return [number[0] for number in numbers]

    @staticmethod
    def get_teams_waitings(stage, cat):
        teams = Team.query.filter(getattr(Team, f'stage{stage}') == 1, getattr(Team, f'cat_stage{stage}') == cat).all()
        return teams

    @staticmethod
    def get_all_waitings():
        teams = Team.query.order_by(Team.updated_at.asc()).all()
        return [team.to_dict() for team in teams]

    @staticmethod
    def get_max_team_number():
        return Team.query.with_entities(Team.number).order_by(Team.number.desc()).first()

    @staticmethod
    def count():
        return Team.query.count()

    # INSERT    
    @staticmethod
    def insert_teams(teams):
        db.session.add_all(teams)
        db.session.commit()

    # UPDATE
    @staticmethod
    def unregister_teams(teams_numbers, stage):
        Team.query.filter(Team.number.in_(teams_numbers)).update({f'stage{stage}': 1})
        db.session.commit()

    @staticmethod
    def update_teams(teams):
        for team in teams:
            db.session.merge(team)
        db.session.commit()

    @staticmethod
    def update_teams_status(teams_numbers, stage):
        Team.query.filter(Team.number.in_(teams_numbers)).update({f'stage{stage}': TeamStatus.AFFECTED.value})
        db.session.commit()
    
    # DELETE
    @staticmethod
    def delete_team(team):
        db.session.delete(team)
        db.session.commit()

    @staticmethod
    def delete_all():
        Team.query.delete()
        db.session.commit()