from repositories.TeamsRepository import TeamsRepository
from utils.enums import CategorieStatus

teamsRepository = TeamsRepository()

def getRoundAndCategorieByValue(panel):
    if panel == 1:
        return 1, CategorieStatus.WINNER.value
    elif panel == 2:
        return 2, CategorieStatus.WINNER.value
    elif panel == 3:
        return 2, CategorieStatus.LOSER.value
    elif panel == 4:
        return 3, CategorieStatus.WINNER.value
    elif panel == 5:
        return 3, CategorieStatus.WINNERANDLOSER.value
    elif panel == 6:
        return 3, CategorieStatus.LOSER.value
    elif panel == 7:
        return 4, CategorieStatus.WINNER.value
    elif panel == 8:
        return 5, CategorieStatus.WINNER.value
    elif panel == 9:
        return 6, CategorieStatus.WINNER.value
    elif panel == 10:
        return 7, CategorieStatus.WINNER.value
    elif panel == 11:
        return 8, CategorieStatus.WINNER.value
    return 0, CategorieStatus.NOT_REGISTER.value

# Un vainqueur est forcément dans les gagnants du round suivant sauf s'il était dans les perdants du round 2
def getWinnerNextValue(panel):
    if panel == 3:
        return CategorieStatus.WINNERANDLOSER.value
    return CategorieStatus.WINNER.value

# Un perdants est forcément dans les perdants du round suivant sauf s'il était dans les vainqueurs du round 2 (auquel cas il est en V/D)
def getLoserNextValue(panel):
    if panel == 2:
        return CategorieStatus.WINNERANDLOSER.value
    return CategorieStatus.LOSER.value

# Un vainqueur est forcément affecté au round suivant, sauf s'il est au round3 sans avoir 2 victoires
def isWinnerAffectedNextRound(panel):
    if panel in (5, 6, 11):
        return False
    return True

# Un loser ne continue que si on est en round 1 ou 2
def isLoserAffectedNextRound(round):
    if round in (1, 2):
        return True
    return False

# On saute les 1/16 si moins de 129 équipes
def getNextRound(round):
    if round == 3 and teamsRepository.count() < 129:
        return 5
    return round + 1