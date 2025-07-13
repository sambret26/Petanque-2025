import random

from utils.enums import MatchStatus, TeamStatus, CategorieStatus
from repositories.MatchsRepository import MatchsRepository
from repositories.TeamsRepository import TeamsRepository
from models.Match import Match
from utils import utils

matchs_repository = MatchsRepository()
teams_repository = TeamsRepository()

def get_matches(panel):
    if panel == -1:
        return matchs_repository.get_all()
    return matchs_repository.get_by_panel(panel)

def generate(panel):
    stage, cat = utils.get_stage_and_categorie_by_value(panel)
    waitings = teams_repository.get_teams_waitings(stage, cat)
    matchs = []
    updates = []
    success = generate_matchs(matchs, updates, waitings, panel)
    if success:
        matchs_repository.insert_matchs(matchs)
        teams_repository.update_teams_status(updates, stage)
        return 200
    return 201

def ungenerate(panel):
    stage, _ = utils.get_stage_and_categorie_by_value(panel)
    matchs = matchs_repository.get_not_launched(panel)
    teams = []
    for match in matchs:
        teams.append(match.team1)
        teams.append(match.team2)
    matchs_repository.delete_matchs([match.id for match in matchs])
    teams_repository.unregister_teams(teams, stage)

def launch_matches(panel):
    matchs = matchs_repository.get_not_launched(panel)
    matchs_repository.launch_matches([match.id for match in matchs])

def change_status(match_id):
    status = matchs_repository.get_by_id(match_id).status
    if status == MatchStatus.CREATED.value:
        matchs_repository.start_match(match_id)
    elif status == MatchStatus.IN_PROGRESS.value:
        matchs_repository.stop_match(match_id)

def set_winner(match_id, winner):
    match = matchs_repository.get_by_id(match_id)
    stage, _ = utils.get_stage_and_categorie_by_value(match.panel)
    next_stage = utils.get_next_stage(stage)
    ko1 = False
    ko2 = False
    # Mise à jour du vainqueur
    team = teams_repository.get_by_number(winner)
    setattr(team, f'stage{stage}', TeamStatus.WINNER.value)
    if utils.is_winner_affected_next_stage(match.panel):
        next_stage_value = getattr(team, f'stage{next_stage}')
        if (next_stage_value < TeamStatus.AFFECTED.value):
            setattr(team, f'stage{next_stage}', TeamStatus.REGISTER.value)
            setattr(team, f'cat_stage{next_stage}', utils.get_winner_next_value(match.panel))
        else:
            ko1 = True
    teams_repository.update_teams([team])

    # Mise à jour du perdant
    loser = match.team1 if match.team1 != winner else match.team2
    team = teams_repository.get_by_number(loser)
    setattr(team, f'stage{stage}', TeamStatus.LOSER.value)
    if utils.is_loser_affected_next_stage(stage):
        next_stage_value = getattr(team, f'stage{next_stage}')
        if (next_stage_value < TeamStatus.AFFECTED.value):
            setattr(team, f'stage{next_stage}', TeamStatus.REGISTER.value)
            setattr(team, f'cat_stage{next_stage}', utils.get_loser_next_value(match.panel))
        else:
            ko2 = True
    teams_repository.update_teams([team])

    # Mise à jour du match
    matchs_repository.set_winner(match_id, winner)
    if ko1 and ko2:
        return 203
    if ko1:
        return 202
    if ko2:
        return 201
    return 200

def unset_winner(match_id):
    match = matchs_repository.get_by_id(match_id)
    stage, _ = utils.get_stage_and_categorie_by_value(int(match.panel))
    next_stage = utils.get_next_stage(stage)
    # Mise à jour des équipes
    team1 = teams_repository.get_by_number(match.team1)
    team2 = teams_repository.get_by_number(match.team2)
    team1_next_stage = getattr(team1, f'stage{next_stage}')
    team2_next_stage = getattr(team2, f'stage{next_stage}')
    if team1_next_stage > TeamStatus.REGISTER.value:
        return 201
    if team2_next_stage > TeamStatus.REGISTER.value:
        return 201
    setattr(team1, f'stage{stage}', TeamStatus.AFFECTED.value)
    setattr(team1, f'stage{next_stage}', TeamStatus.NOT_REGISTER.value)
    setattr(team1, f'cat_stage{next_stage}', CategorieStatus.NOT_REGISTER.value)
    setattr(team2, f'stage{stage}', TeamStatus.AFFECTED.value)
    setattr(team2, f'stage{next_stage}', TeamStatus.NOT_REGISTER.value)
    setattr(team2, f'cat_stage{next_stage}', CategorieStatus.NOT_REGISTER.value)
    teams_repository.update_teams([team1, team2])

    # Mise à jour du match
    matchs_repository.unset_winner(match_id)
    return 200

def create_match(panel, team_number1, team_number2):
    match_in_db = matchs_repository.get_by_teams(team_number1, team_number2)
    if match_in_db != None:
        return None, 202
    team1 = teams_repository.get_by_number(team_number1)
    team2 = teams_repository.get_by_number(team_number2)
    stage, _ = utils.get_stage_and_categorie_by_value(panel)
    if getattr(team1, f'stage{stage}') != 1 or getattr(team2, f'stage{stage}') != 1:
        return None, 201
    if team_number1 < team_number2:
        match = Match(team_number1, team_number2, panel)
    else:
        match = Match(team_number2, team_number1, panel)
    setattr(team1, f'stage{stage}', TeamStatus.AFFECTED.value)
    setattr(team2, f'stage{stage}', TeamStatus.AFFECTED.value)
    teams_repository.update_teams([team1, team2])
    matchs_repository.insert_match(match)
    return match.to_dict(), 200

def delete_match(match_id):
    match = matchs_repository.get_by_id(match_id)
    if not match:
        return 201
    stage, _ = utils.get_stage_and_categorie_by_value(match.panel)
    team1 = teams_repository.get_by_number(match.team1)
    team2 = teams_repository.get_by_number(match.team2)
    setattr(team1, f'stage{stage}', TeamStatus.REGISTER.value)
    setattr(team2, f'stage{stage}', TeamStatus.REGISTER.value)
    teams_repository.update_teams([team1, team2])
    matchs_repository.delete_match(match_id)
    return 200

def generate_matchs(matchs, update, teams, panel):
    matchs_in_db = matchs_repository.get_teams_list()
    random.shuffle(teams)
    value = len(teams) if len(teams) % 2 == 0 else len(teams) - 1
    i = 0
    retry = 1
    while i < value:
        team1 = teams[i].number if teams[i].number < teams[i+1].number else teams[i+1].number
        team2 = teams[i].number if teams[i].number > teams[i+1].number else teams[i+1].number
        if (str(team1) + "_" + str(team2) in matchs_in_db):
            if (i+retry+1 < len(teams)):
                temp = teams[i+1]
                teams[i+1] = teams[i+retry+1]
                teams[i+retry+1] = temp
            else :
                return False
            if retry > 5:
                return False
            retry += 1
            continue
        matchs.append(Match(team1, team2, panel))
        update.append(teams[i].number)
        update.append(teams[i+1].number)
        i += 2
    return True