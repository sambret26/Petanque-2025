from repositories.TeamsRepository import TeamsRepository
from utils.enums import CategorieStatus, TeamStatus
from models.Team import Team
from utils import utils

teams_repository = TeamsRepository()

def count():
    return teams_repository.count()

def get_waitings(panel):
    if panel == -1:
        return teams_repository.get_all_waitings()
    stage, cat = utils.get_stage_and_categorie_by_value(int(panel))
    return teams_repository.get_waitings(stage, cat)

def register(number):
    teams = []
    max_team_number = teams_repository.get_max_team_number()
    if max_team_number == None:
        max_team_number = 0
    else:
        max_team_number = int(max_team_number[0])
    for number in range (max_team_number+1, max_team_number+number+1):
        team = Team(number=number, stage1=TeamStatus.REGISTER.value, cat_stage1=CategorieStatus.WINNER.value)
        teams.append(team)
    teams_repository.insert_teams(teams)

def unregister(team_number):
    team = teams_repository.get_by_number(team_number)
    if team == None:
        return False
    teams_repository.delete_team(team)
    return True

def lucky_loser(panel, team):
    team = teams_repository.get_by_number(team)
    stage, cat = utils.get_stage_and_categorie_by_value(int(panel))
    next_stage = utils.get_next_stage(stage)
    if team == None:
        return 201 # Equipe inconnue
    if getattr(team, f'stage{next_stage}') != TeamStatus.NOT_REGISTER.value:
        return 202 # En lice au tour suivant
    if getattr(team, f'stage{stage}') > TeamStatus.REGISTER.value:
        return 203 # Match en cours sur ce tour
    if getattr(team, f'stage{stage}') == TeamStatus.NOT_REGISTER.value:
        setattr(team, f'stage{stage}', TeamStatus.REGISTER.value)
        setattr(team, f'cat_stage{stage}', cat)
        teams_repository.update_teams([team])
        return 204 # Pas encore inscrite à ce tour
    if getattr(team, f'cat_stage{stage}') == cat:
        return 205 # Dejà inscrite sur ce tour
    if getattr(team, f'cat_stage{stage}') > cat:
        setattr(team, f'cat_stage{stage}', cat)
        teams_repository.update_teams([team])
        return 206 # Rétrogradation
    setattr(team, f'stage{stage}', TeamStatus.REGISTER.value)
    setattr(team, f'cat_stage{stage}', cat)
    teams_repository.update_teams([team])
    return 207 # Avancé