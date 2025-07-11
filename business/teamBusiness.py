from repositories.TeamsRepository import TeamsRepository
from utils.enums import CategorieStatus, TeamStatus
from models.Team import Team
from utils import utils

teamsRepository = TeamsRepository()

def count():
    return teamsRepository.count()

def getWaitings(panel):
    if panel == -1:
        return teamsRepository.getAllWaitings()
    round, cat = utils.getRoundAndCategorieByValue(int(panel))
    return teamsRepository.getWaitings(round, cat)

def register(number):
    teams = []
    maxTeamNumber = teamsRepository.getMaxTeamNumber()
    if maxTeamNumber == None:
        maxTeamNumber = 0
    else:
        maxTeamNumber = int(maxTeamNumber[0])
    for number in range (maxTeamNumber+1, maxTeamNumber+number+1):
        team = Team(number=number, catRound1=CategorieStatus.WINNER.value, round1=TeamStatus.REGISTER.value)
        teams.append(team)
    teamsRepository.insertTeams(teams)

def unregister(teamNumber):
    team = teamsRepository.getByNumber(teamNumber)
    if team == None:
        return False
    teamsRepository.deleteTeam(team)
    return True

def luckyLoser(panel, team):
    team = teamsRepository.getByNumber(team)
    round, cat = utils.getRoundAndCategorieByValue(int(panel))
    nextRound = utils.getNextRound(round)
    if team == None:
        return 201 # Equipe inconnue
    if getattr(team, f'round{nextRound}') != TeamStatus.NOT_REGISTER.value:
        return 202 # En lice au tour suivant
    if getattr(team, f'round{round}') > TeamStatus.REGISTER.value:
        return 203 # Match en cours sur ce tour
    if getattr(team, f'round{round}') == TeamStatus.NOT_REGISTER.value:
        setattr(team, f'round{round}', TeamStatus.REGISTER.value)
        setattr(team, f'catRound{round}', cat)
        teamsRepository.updateTeams([team])
        return 204 # Pas encore inscrite à ce tour
    if getattr(team, f'catRound{round}') == cat:
        return 205 # Dejà inscrite sur ce tour
    if getattr(team, f'catRound{round}') > cat:
        setattr(team, f'catRound{round}', cat)
        teamsRepository.updateTeams([team])
        return 206 # Rétrogradation
    setattr(team, f'round{round}', TeamStatus.REGISTER.value)
    setattr(team, f'catRound{round}', cat)
    teamsRepository.updateTeams([team])
    return 207 # Avancé