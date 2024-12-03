from ursina import *
from ursina.prefabs.health_bar import HealthBar
from popgame.game_engine.team_util import *
from popgame.constant import COUNT_DOWN_WAIT_TIME

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

        self._intro_text =  Text(text=intro_txt,color=color.azure,scale=5.0, wordwrap=30,origin=(.1,-0.5),ignore_paused=True)
        self._intro_text.visible_setter(False)
        self._intro_text.create_background(self._intro_text.size*0.5,self._intro_text.size*0.8,color.black50)

        self._start_count_down_text =  Text(text="3",color=color.azure,scale=10.0, wordwrap=30,origin=(.1,-0.5),ignore_paused=True)
        self._start_count_down_text.visible_setter(False)
        self._start_count_down_text.create_background(self._intro_text.size*1.5,self._intro_text.size*0.7,color.black33)

        self._next_text =  Text(text=continue_txt,color=color.azure,scale=2.0, wordwrap=30,origin=(.1,3.0),ignore_paused=True)
        self._next_text.visible_setter(False)
        self._next_text.create_background(self._intro_text.size*0.5,self._intro_text.size*0.8,color.black50)

        self._end_text =  Text(text=end_txt,color=color.azure,scale=5.0, wordwrap=30,origin=(.1,0),ignore_paused=True)
        self._end_text.visible_setter(False)
        self._end_text.create_background(self._intro_text.size*0.5,self._intro_text.size*0.8,color.black50)
        
        self._score_dict = dict()
        self._score_txt_dict = dict()
        self._hp_delta = Vec3(0.0,-0.07,0)
        
        self._team_left_set = set()

    def add_health_bar(self,team_info:ETeamInfo,total_point):
        name = team_info.player_name
        col = team_info.color
        hp_origin = self._hp_delta * (len(self._score_dict) +1)
        scale=Vec2(.3,0.03)
        txt_scale = 0.9* Vec2(1.0/scale.x,1.0/scale.y)
        self._score_dict[team_info] = HealthBar(bar_color=col.tint(-.25), roundness=.1, max_value=MAX_ALLOWED_POINTS, value=total_point, scale=scale,show_lines=False,position=window.top_left+hp_origin,ignore_paused=True)
        self._score_txt_dict[team_info] = Text(text=name,color=col,scale=txt_scale, wordwrap=30,parent=self._score_dict[team_info],position=Vec3(0,0.6,0),ignore_paused=True)
        self._score_txt_dict[team_info].create_background(self._intro_text.size*0.5,self._intro_text.size*0.8,color.black90)

        self._team_left_set.add(team_info)

    def sub_team_score(self,team_flag:ETeamInfo,delta:int):
        self._score_dict[team_flag].value = self._score_dict[team_flag].value - delta
        is_team_eliminated = False
        if self._score_dict[team_flag].value < 0:
            raise Exception("Tannant...")
        if self._score_dict[team_flag].value == 0:
            if team_flag in self._team_left_set:
                self._team_left_set.remove(team_flag)
                is_team_eliminated = True
        return is_team_eliminated
    
    def try_get_winner_team_info(self):
        if len(self._team_left_set) == 0:
            raise Exception("No winner? Should not happen...")
        if len(self._team_left_set) == 1:
            return next(iter(self._team_left_set))
        return None
        
    def show_score(self,is_visible):
        for k,v in self._score_dict.items():
            v.visible_setter(is_visible)
        for k,v in self._score_txt_dict.items():
            v.visible_setter(is_visible)

    def display_intro(self):
        self._intro_text.visible_setter(True)
        self._intro_text.appear(0.08)
        self._next_text.visible_setter(True)
        self.show_score(False)
        self._end_text.visible_setter(False)
        self._start_count_down_text.visible_setter(False)

    def display_countdown(self):
        self._intro_text.visible_setter(False)
        self._next_text.visible_setter(False)
        self.show_score(True)
        self._end_text.visible_setter(False)
        self._start_count_down_text.visible_setter(True)
    
    def display_score(self):
        self._intro_text.visible_setter(False)
        self.show_score(True)
        self._end_text.visible_setter(False)
        self._next_text.visible_setter(False)
        self._start_count_down_text.visible_setter(False)
    
    def display_end(self):
        self._intro_text.visible_setter(False)
        self.show_score(True)
        team_info = next(iter(self._team_left_set))
        if team_info:
            self._end_text.text = f"Winner is {team_info.player_name}"
        self._end_text.visible_setter(True)
        self._end_text.appear(0.1)
        self._next_text.visible_setter(True)
        self._start_count_down_text.visible_setter(False)

    def launch_countdown(self,callable):
        self.display_countdown()
        s = Sequence(
            Func(self._display_countdown,"3"),
            Wait(COUNT_DOWN_WAIT_TIME),
            Func(self._display_countdown,"2"),
            Wait(COUNT_DOWN_WAIT_TIME),
            Func(self._display_countdown,"1"),
            Wait(COUNT_DOWN_WAIT_TIME),
            Func(self._display_countdown,"Go!!!"),
            Func(callable),
            Wait(COUNT_DOWN_WAIT_TIME*0.5),
            Func(self._start_count_down_text.visible_setter,False)
        )
        s.start()

    def _display_countdown(self,msg):
        self._start_count_down_text.text = msg