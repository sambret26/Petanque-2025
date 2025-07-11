import random

from utils.enums import MatchStatus, TeamStatus, CategorieStatus
from repositories.MatchsRepository import MatchsRepository
from repositories.TeamsRepository import TeamsRepository
from models.Match import Match
from utils import utils

matchsRepository = MatchsRepository()
teamsRepository = TeamsRepository()

def getMatches(panel):
    if panel == -1:
        return matchsRepository.getAllMatches()
    return matchsRepository.getMatches(panel)

def generate(panel):
    round, cat = utils.getRoundAndCategorieByValue(panel)
    teamsWaitings = teamsRepository.getTeamsWaitings(round, cat)
    matchs = []
    teamsToUpdate = []
    generateMatchs(matchs, teamsToUpdate, teamsWaitings, panel)
    matchsRepository.insertMatchs(matchs)
    teamsRepository.updateTeamsStatus(teamsToUpdate, round)

def ungenerate(panel):
    round, _ = utils.getRoundAndCategorieByValue(panel)
    matchs = matchsRepository.getNotLaunched(panel)
    teamsNumber = []
    for match in matchs:
        teamsNumber.append(match.team1)
        teamsNumber.append(match.team2)
    matchsRepository.deleteMatchs([match.id for match in matchs])
    teamsRepository.unregisterTeams(teamsNumber, round)

def launchMatches(panel):
    matchs = matchsRepository.getNotLaunched(panel)
    matchsRepository.launchMatches([match.id for match in matchs])

def changeStatus(matchId):
    status = matchsRepository.getById(matchId).status
    if status == MatchStatus.CREATED.value:
        matchsRepository.startMatch(matchId)
    elif status == MatchStatus.IN_PROGRESS.value:
        matchsRepository.stopMatch(matchId)

def setWinner(matchId, winner):
    match = matchsRepository.getById(matchId)
    round, _ = utils.getRoundAndCategorieByValue(match.panel)
    nextRound = utils.getNextRound(round)
    ko1 = False
    ko2 = False
    # Mise à jour du vainqueur
    team = teamsRepository.getByNumber(winner)
    setattr(team, f'round{round}', TeamStatus.WINNER.value)
    if utils.isWinnerAffectedNextRound(match.panel):
        nextRoundValue = getattr(team, f'round{nextRound}')
        if (nextRoundValue < TeamStatus.AFFECTED.value):
            setattr(team, f'round{nextRound}', TeamStatus.REGISTER.value)
            setattr(team, f'catRound{nextRound}', utils.getWinnerNextValue(match.panel))
        else:
            ko1 = True
    teamsRepository.updateTeams([team])

    # Mise à jour du perdant
    loser = match.team1 if match.team1 != winner else match.team2
    team = teamsRepository.getByNumber(loser)
    setattr(team, f'round{round}', TeamStatus.LOSER.value)
    if utils.isLoserAffectedNextRound(round):
        nextRoundValue = getattr(team, f'round{nextRound}')
        if (nextRoundValue < TeamStatus.AFFECTED.value):
            setattr(team, f'round{nextRound}', TeamStatus.REGISTER.value)
            setattr(team, f'catRound{nextRound}', utils.getLoserNextValue(match.panel))
        else:
            ko2 = True
    teamsRepository.updateTeams([team])

    # Mise à jour du match
    matchsRepository.setWinner(matchId, winner)
    if ko1 and ko2:
        return 203
    if ko1:
        return 202
    if ko2:
        return 201
    return 200

def unsetWinner(matchId):
    match = matchsRepository.getById(matchId)
    round, _ = utils.getRoundAndCategorieByValue(int(match.panel))
    nextRound = utils.getNextRound(round)
    # Mise à jour des équipes
    team1 = teamsRepository.getByNumber(match.team1)
    team2 = teamsRepository.getByNumber(match.team2)
    team1NextRound = getattr(team1, f'round{nextRound}')
    team2NextRound = getattr(team2, f'round{nextRound}')
    if team1NextRound > TeamStatus.REGISTER.value:
        return 201
    if team2NextRound > TeamStatus.REGISTER.value:
        return 201
    setattr(team1, f'round{round}', TeamStatus.AFFECTED.value)
    setattr(team1, f'round{nextRound}', TeamStatus.NOT_REGISTER.value)
    setattr(team1, f'catRound{nextRound}', CategorieStatus.NOT_REGISTER.value)
    setattr(team2, f'round{round}', TeamStatus.AFFECTED.value)
    setattr(team2, f'round{nextRound}', TeamStatus.NOT_REGISTER.value)
    setattr(team2, f'catRound{nextRound}', CategorieStatus.NOT_REGISTER.value)
    teamsRepository.updateTeams([team1, team2])

    # Mise à jour du match
    matchsRepository.unsetWinner(matchId)
    return 200

def createMatch(panel, teamNumber1, teamNumber2):
    team1 = teamsRepository.getByNumber(teamNumber1)
    team2 = teamsRepository.getByNumber(teamNumber2)
    round, _ = utils.getRoundAndCategorieByValue(panel)
    if getattr(team1, f'round{round}') != 1 or getattr(team2, f'round{round}') != 1:
        return None, 201
    match = Match(teamNumber1, teamNumber2, panel)
    setattr(team1, f'round{round}', TeamStatus.AFFECTED.value)
    setattr(team2, f'round{round}', TeamStatus.AFFECTED.value)
    teamsRepository.updateTeams([team1, team2])
    matchsRepository.insertMatch(match)
    return match.toDict(), 200

def deleteMatch(matchId):
    match = matchsRepository.getById(matchId)
    if not match:
        return 201
    round, _ = utils.getRoundAndCategorieByValue(match.panel)
    team1 = teamsRepository.getByNumber(match.team1)
    team2 = teamsRepository.getByNumber(match.team2)
    setattr(team1, f'round{round}', TeamStatus.REGISTER.value)
    setattr(team2, f'round{round}', TeamStatus.REGISTER.value)
    teamsRepository.updateTeams([team1, team2])
    matchsRepository.deleteMatch(matchId)
    return 200

def generateMatchs(matchs, teamsToUpdate, teams, panel):
    random.shuffle(teams)
    max = len(teams) if len(teams) % 2 == 0 else len(teams) - 1
    for i in range (0, max, 2):
        team1 = teams[i].number if teams[i].number < teams[i+1].number else teams[i+1].number
        team2 = teams[i].number if teams[i].number > teams[i+1].number else teams[i+1].number
        matchs.append(Match(team1, team2, panel))
        teamsToUpdate.append(teams[i].number)
        teamsToUpdate.append(teams[i+1].number)
