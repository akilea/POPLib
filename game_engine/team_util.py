from enum import Enum
from ursina import Vec2,color

from popgame.constant import *

class TeamUtil:
    class ETeam(Enum):
        Francois = 1<<0
        Vincent = 1<<1
        Bettina = 1<<3
        Gabriel = 1<<4
        Abigail = 1<<5
        Emeric = 1<<6
        Elias = 1<<7
        MarcAndre = 1<<8
        Neutral = 1<<9
        Undefined = 1<<10

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

    MAX_ALLOWED_SPAWN_RADIUS = 150.0
    MAX_ALLOWED_POINTS = 100
    team_relative_start_position_dict = {
        ETeam.Francois:Vec2(1,0),
        ETeam.Vincent:Vec2(-1,0),
        ETeam.Bettina:Vec2(0,1),
        ETeam.Gabriel:Vec2(0,-1),
        ETeam.Abigail:Vec2(0.5,0.5),
        ETeam.Emeric:Vec2(0.5,-0.5),
        ETeam.Elias:Vec2(-0.5,-0.5),
        ETeam.MarcAndre:Vec2(-0.5,0.5),
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
    
    @staticmethod
    def get_team_flag_value(team_color : ETeam):
        return team_color.value

    @staticmethod
    def get_team_color(team_color : ETeam):
        return TeamUtil.team_color_dict.get(team_color,TeamUtil.team_color_dict[TeamUtil.ETeam.Undefined])
    
    @staticmethod
    def get_team_position(team_color : ETeam):
        return WORLD_SIZE * TeamUtil.team_relative_start_position_dict.get(team_color,TeamUtil.team_relative_start_position_dict[TeamUtil.ETeam.Undefined])
    
    @staticmethod
    def get_team_input_control(team_color : ETeam):
        return TeamUtil.team_input_dict.get(team_color,TeamUtil.team_input_dict[TeamUtil.ETeam.Undefined])