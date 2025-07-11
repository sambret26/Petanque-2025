from repositories.TeamsRepository import TeamsRepository
from utils.enums import CategorieStatus

teams_repository = TeamsRepository()

def get_stage_and_categorie_by_value(panel):
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

# Un vainqueur est forcément dans les gagnants de la manche suivante sauf s'il était dans les perdants de la manche 2
def get_winner_next_value(panel):
    if panel == 3:
        return CategorieStatus.WINNERANDLOSER.value
    return CategorieStatus.WINNER.value

# Un perdants est forcément dans les perdants de la manche suivante sauf s'il était dans les vainqueurs de la manche 2 (auquel cas il est en V/D)
def get_loser_next_value(panel):
    if panel == 2:
        return CategorieStatus.WINNERANDLOSER.value
    return CategorieStatus.LOSER.value

# Un vainqueur est forcément affecté à la manche suivante, sauf s'il est à la manche 3 sans avoir 2 victoires
def is_winner_affected_next_stage(panel):
    if panel in (5, 6, 11):
        return False
    return True

# Un loser ne continue que si on est en manche 1 ou 2
def is_loser_affected_next_stage(stage):
    if stage in (1, 2):
        return True
    return False

# On saute les 1/16 si moins de 129 équipes
def get_next_stage(stage):
    if stage == 3 and teams_repository.count() < 129:
        return 5
    return stage + 1