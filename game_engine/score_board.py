from ursina import *

class ScoreBoard(Entity):
    def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        self._intro_text =  Text(text="Bienvenue au Pecking Order Pandemonium!")
        self._intro_text.disable
        
        self._end_text =  Text(text="Bravo au gagnant")
        self._end_text.disable
        
        self._score_master = Entity()
        self._score_master.disable
        
        #HealthBar and 
        
    def display_intro(self):
        self._intro_text.enable
        self._score_master.disable
        self._end_text.disable
    
    def display_score(self):
        self._intro_text.disable
        self._score_master.enable
        self._end_text.disable
    
    def display_end(self):
        self._intro_text.disable
        self._score_master.enable
        self._end_text.enable