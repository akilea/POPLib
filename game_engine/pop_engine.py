from popgame.game_engine.combat_simulator import CombatSimulator
from popgame.game_engine.score_board import ScoreBoard
from popgame.game_engine.team import Team
from ursina import *

class PopEngine(Entity):
    def __init__(self) -> None:
        super().__init__(True,True)
        self._cs = CombatSimulator(self.kill_bcu)
        self._sb = ScoreBoard()
        self._state = -999
        self._wait_update_for_state_change = -1 #Nothing
        
    def go_to_load(self):
        self._cs.build_teams()
        for info,team in self._cs._team_dict.items():
            self._sb.add_health_bar(info,team.compute_total_point())
        self._state = 1
        self._wait_update_for_state_change = 1

    def go_to_preparation_freeze(self):
        self._cs.stop()
        self._sb.display_intro()

    def go_to_simulation(self):
        self._sb.launch_countdown(self._cs.start)

    def go_to_end_game(self):
        self._cs.stop()
        self._sb.display_end()
        
    def register_team(self,team:Team):
        self._cs.register_team(team)
        
    def input(self,key):
        if self._wait_update_for_state_change == -1 and "space" == key:
            if self._state == 1:
                self._wait_update_for_state_change = 0
                self._state = 2

    def update(self):
        if self._wait_update_for_state_change >= 0:
            self._wait_update_for_state_change -= 1
            if self._wait_update_for_state_change < 0:
                if self._state == 0:
                    self.go_to_load()
                if self._state == 1:
                    self.go_to_preparation_freeze()
                if self._state == 2:
                    self.go_to_simulation()
                if self._state == 3:
                    self.go_to_end_game()

    def kill_bcu(self,cuw):
        if self._sb.sub_team_score(cuw.team_info,cuw.unit_type.cost):
            self._cs.elimiate_team(cuw.team_info)
            winner_info = self._sb.try_get_winner_team_info()
            if winner_info:
                self._cs.win_team(winner_info)
                self._state = 3
                self._wait_update_for_state_change = 120
