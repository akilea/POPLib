from popgame.game_engine.combat_simulator import CombatSimulator
from popgame.game_engine.score_board import ScoreBoard
from ursina import *

class PopEngine(Entity):
    def __init__(self) -> None:
        super().__init__(True,True)
        self._cs = CombatSimulator(self.on_bcu_death)
        self._sb = ScoreBoard()
        self._state = -999
        self._wait_update_for_state_change = -1 #Nothing
        
    def go_to_load(self):
        self._cs.build_teams()
        for t in self._cs._team_set:
            self._sb.add_health_bar(t.team_flag)
        self._state = 1
        self._wait_update_for_state_change = 1

    def go_to_preparation_freeze(self):
        self._cs.stop()
        self._sb.display_intro()

    def go_to_simulation(self):
        self._sb.launch_countdown(self._cs.start)

    def go_to_end_game(self):
        self._cs.end()
        self._sb.display_end()

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

    def on_bcu_death(self,cul):
        if self._sb.sub_team_score(cul.team_flag,1) == 1:
            raise Exception("On va au gagnant!")