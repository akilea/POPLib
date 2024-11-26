from ursina import *
from ursina.prefabs.health_bar import HealthBar
from popgame.game_engine.team_util import TeamUtil

class ScoreBoard():
    def __init__(self):
        intro_txt = dedent('''
            <red>Welcome to<default>\n
            Peck Order Pandemonium!''').strip()
        
        continue_txt = dedent('''
            <red>Space to continue...<default>''').strip()

        end_txt = dedent('''
            <red>Winner is<default>\n
            PATATE''').strip()

        self._intro_text =  Text(text=intro_txt,color=color.azure,scale=5.0, wordwrap=30,origin=(.1,-0.5))
        self._intro_text.visible_setter(False)

        self._next_text =  Text(text=continue_txt,color=color.azure,scale=2.0, wordwrap=30,origin=(.1,0.7))
        self._next_text.visible_setter(False)

        self._end_text =  Text(text=end_txt,color=color.azure,scale=5.0, wordwrap=30,origin=(.1,0))
        self._end_text.visible_setter(False)
        
        self._score_dict = dict()
        self._score_txt_dict = dict()
        self._hp_delta = Vec3(0.0,-0.07,0)
        
    def add_health_bar(self,team_flag:TeamUtil.ETeam):
        name = TeamUtil.get_team_name(team_flag)
        col = TeamUtil.get_team_color(team_flag)
        hp_origin = self._hp_delta * (len(self._score_dict) +1)
        scale=Vec2(.3,0.03)
        txt_scale = 0.9* Vec2(1.0/scale.x,1.0/scale.y)
        self._score_dict[team_flag] = HealthBar(bar_color=col.tint(-.25), roundness=.1, max_value=TeamUtil.MAX_ALLOWED_POINTS, value=TeamUtil.MAX_ALLOWED_POINTS, scale=scale,show_lines=False,position=window.top_left+hp_origin)
        self._score_txt_dict[team_flag] = Text(text=name,color=col,scale=txt_scale, wordwrap=30,parent=self._score_dict[team_flag],position=Vec3(0,0.6,0))

    def sub_team_score(self,team_flag:TeamUtil.ETeam,delta:int):
        self._score_dict[team_flag].value = self._score_dict[team_flag].value - delta

    def show_score(self,is_visible):
        for k,v in self._score_dict.items():
            v.visible_setter(is_visible)
        for k,v in self._score_txt_dict.items():
            v.visible_setter(is_visible)

    def display_intro(self):
        self._intro_text.visible_setter(True)
        self._intro_text.appear(0.1)
        self._next_text.visible_setter(True)
        self.show_score(True)
        self._end_text.visible_setter(False)
    
    def display_score(self):
        self._intro_text.visible_setter(False)
        self.show_score(True)
        self._end_text.visible_setter(False)
        self._next_text.visible_setter(False)
    
    def display_end(self):
        self._intro_text.visible_setter(False)
        self.show_score(True)
        self._end_text.visible_setter(True)
        self._end_text.appear(0.1)
        self._next_text.visible_setter(True)