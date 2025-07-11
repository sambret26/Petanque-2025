from repositories.MatchsRepository import MatchsRepository
from repositories.TeamsRepository import TeamsRepository

matchs_repository = MatchsRepository()
teams_repository = TeamsRepository()

def init():
    matchs_repository.delete_all()
    teams_repository.delete_all()