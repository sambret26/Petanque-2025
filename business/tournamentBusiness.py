from repositories.MatchsRepository import MatchsRepository
from repositories.TeamsRepository import TeamsRepository

matchsRepository = MatchsRepository()
teamsRepository = TeamsRepository()

def init():
    matchsRepository.deleteAll()
    teamsRepository.deleteAll()