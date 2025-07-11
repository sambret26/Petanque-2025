from enum import Enum

class TeamStatus(Enum):
    NOT_REGISTER = 0
    REGISTER = 1 
    AFFECTED = 2 
    LOSER = 3         
    WINNER = 4

class CategorieStatus(Enum):
    NOT_REGISTER = 0
    LOSER = 1 
    WINNERANDLOSER = 2 
    WINNER = 3   

class MatchStatus(Enum):
    CREATED = 0
    IN_PROGRESS = 1
    COMPLETED = 2