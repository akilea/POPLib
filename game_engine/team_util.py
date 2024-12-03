from enum import Enum
from ursina import Vec2,color

from popgame.constant import *

class EUnitType(Enum):
    Light = (1,100,20,1.0)
    Medium = (2,200,15,2.0)
    Heavy = (3,350,10,3.0)
    
    def __init__(self, cost:int,max_hp:int,max_velocity:float,damage_multiplier:float):
        self.max_hp = max_hp
        self.max_velocity = max_velocity
        self.max_velocity_squared = max_velocity * max_velocity
        self.damage_multiplier = damage_multiplier
        
class EDamageType(Enum):
    Collision = 1
    VelocityLimit = 2
    Zone = 3

MAX_ALLOWED_SPAWN_SQUARE_HALF_SIZE = 5.0
MAX_ALLOWED_POINTS = 50
RELATIVE_TEAM_DISTANCE = 0.8
RELATIVE_TEAM_HALF_DISTANCE = RELATIVE_TEAM_DISTANCE*0.5

class ETeam(Enum):
    Vincent=  (1<<2, "Vincent",color.olive,Vec2(-RELATIVE_TEAM_DISTANCE,0),"wasd")
    Francois = (1<<1, "Francois",color.magenta,Vec2(RELATIVE_TEAM_DISTANCE,0),"wasd")
    Bettina = (1<<3, "Bettina",color.blue,Vec2(0,RELATIVE_TEAM_DISTANCE),"wasd")
    Gabriel = (1<<4, "Gabriel",color.dark_gray,Vec2(0,-RELATIVE_TEAM_DISTANCE),"wasd")
    Abigail = (1<<5, "Abigail",color.salmon,Vec2(RELATIVE_TEAM_HALF_DISTANCE,RELATIVE_TEAM_HALF_DISTANCE),"wasd")
    Emeric = (1<<6, "Emeric",color.lime,Vec2(RELATIVE_TEAM_HALF_DISTANCE,-RELATIVE_TEAM_HALF_DISTANCE),"wasd")
    Elias = (1<<7, "Elias",color.azure,Vec2(-RELATIVE_TEAM_HALF_DISTANCE,-RELATIVE_TEAM_HALF_DISTANCE),"wasd")
    MarcAndre = (1<<8, "MarcAndre",color.peach,Vec2(-RELATIVE_TEAM_HALF_DISTANCE,RELATIVE_TEAM_HALF_DISTANCE),"wasd")
    Neutral = (1<<9, "Neutral",color.smoke,Vec2(0,0),"wasd")
    Undefined = (1<<10, "Undefined",color.white,Vec2(0,0),"wasd")

    def __init__(self, flag:int, player_name:str,col:color,rel_start_pos:Vec2,control_dict:dict):
        self.color = col
        self.flag = flag
        self.rel_start_pos = rel_start_pos
        self.control_dict = control_dict
        self.player_name = player_name

    @staticmethod
    def get_team_flag_value(team_flag):
        raise DeprecationWarning()

    @staticmethod
    def get_team_color(team_flag):
        raise DeprecationWarning()

    @staticmethod
    def get_team_position(team_flag):
        raise DeprecationWarning()

    @staticmethod
    def get_team_input_control(team_flag):
        raise DeprecationWarning()

    @staticmethod
    def get_team_name(team_flag):
        raise DeprecationWarning()

    @staticmethod
    def contains_only_player(team_mask):
        return team_mask.flag & ETeam.Neutral.flag == 0 and team_mask.flag & ETeam.Undefined.flag == 0 and team_mask.flag < ETeam.Neutral.flag
