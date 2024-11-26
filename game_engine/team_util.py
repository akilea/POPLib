from enum import Enum
from ursina import Vec2,color

from popgame.constant import *

class TeamUtil:
    MAX_ALLOWED_SPAWN_SQUARE_HALF_SIZE = 5.0
    MAX_ALLOWED_POINTS = 20
    RELATIVE_TEAM_DISTANCE = 0.8
    RELATIVE_TEAM_HALF_DISTANCE = RELATIVE_TEAM_DISTANCE*0.5
    
    class ETeam(Enum):
        Francois = 1<<1
        Vincent = 1<<2
        Bettina = 1<<4
        Gabriel = 1<<5
        Abigail = 1<<6
        Emeric = 1<<7
        Elias = 1<<8
        MarcAndre = 1<<9
        Neutral = 1<<10
        Undefined = 1<<11

    team_color_dict = {
        ETeam.Francois:color.magenta,
        ETeam.Vincent:color.olive,
        ETeam.Bettina:color.blue,
        ETeam.Gabriel:color.dark_gray,
        ETeam.Abigail:color.salmon,
        ETeam.Emeric:color.lime,
        ETeam.Elias:color.azure,
        ETeam.MarcAndre:color.peach,
        ETeam.Neutral:color.smoke,
        ETeam.Undefined:color.white
    }

    team_relative_start_position_dict = {
        ETeam.Francois:Vec2(RELATIVE_TEAM_DISTANCE,0),
        ETeam.Vincent:Vec2(-RELATIVE_TEAM_DISTANCE,0),
        ETeam.Bettina:Vec2(0,RELATIVE_TEAM_DISTANCE),
        ETeam.Gabriel:Vec2(0,-RELATIVE_TEAM_DISTANCE),
        ETeam.Abigail:Vec2(RELATIVE_TEAM_HALF_DISTANCE,RELATIVE_TEAM_HALF_DISTANCE),
        ETeam.Emeric:Vec2(RELATIVE_TEAM_HALF_DISTANCE,-RELATIVE_TEAM_HALF_DISTANCE),
        ETeam.Elias:Vec2(-RELATIVE_TEAM_HALF_DISTANCE,-RELATIVE_TEAM_HALF_DISTANCE),
        ETeam.MarcAndre:Vec2(-RELATIVE_TEAM_HALF_DISTANCE,RELATIVE_TEAM_HALF_DISTANCE),
        ETeam.Neutral:Vec2(0,0),
        ETeam.Undefined:Vec2(0,0)
    }

    team_input_dict = {
        ETeam.Francois:"wasd",
        ETeam.Vincent:"wasd",
        ETeam.Bettina:"wasd",
        ETeam.Gabriel:"wasd",
        ETeam.Abigail:"wasd",
        ETeam.Emeric:"wasd",
        ETeam.Elias:"wasd",
        ETeam.MarcAndre:"wasd",
        ETeam.Neutral:"wasd",
        ETeam.Undefined:"wasd"
    }
    
    team_string_dict = {
        ETeam.Francois:"François",
        ETeam.Vincent:"Vincent",
        ETeam.Bettina:"Bettina",
        ETeam.Gabriel:"Gabriel",
        ETeam.Abigail:"Abigail",
        ETeam.Emeric:"Emeric",
        ETeam.Elias:"Elias",
        ETeam.MarcAndre:"Marc-André",
        ETeam.Neutral:"Neutral",
        ETeam.Undefined:"Undefined"
    }
    
    @staticmethod
    def get_team_flag_value(team_flag : ETeam):
        return team_flag.value

    @staticmethod
    def get_team_color(team_flag : ETeam):
        return TeamUtil.team_color_dict.get(team_flag,TeamUtil.team_color_dict[TeamUtil.ETeam.Undefined])
    
    @staticmethod
    def get_team_position(team_flag : ETeam):
        return SOFT_BORDER_HALF_SIZE * TeamUtil.team_relative_start_position_dict.get(team_flag,TeamUtil.team_relative_start_position_dict[TeamUtil.ETeam.Undefined])
    
    @staticmethod
    def get_team_input_control(team_flag : ETeam):
        return TeamUtil.team_input_dict.get(team_flag,TeamUtil.team_input_dict[TeamUtil.ETeam.Undefined])
    
    @staticmethod
    def get_team_name(team_flag : ETeam):
        return TeamUtil.team_string_dict.get(team_flag,TeamUtil.team_string_dict[TeamUtil.ETeam.Undefined])
    
    @staticmethod
    def contains_only_player(team_mask : ETeam):
        return team_mask.value & TeamUtil.ETeam.Neutral.value == 0 and team_mask.value & TeamUtil.ETeam.Undefined.value == 0 and team_mask.value < TeamUtil.ETeam.Neutral.value