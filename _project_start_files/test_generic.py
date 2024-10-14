import pytest
from popgame.unit_test.manual_app_runner import run_ursina_for
from popgame.unit_test.conftest import start_ursina,run_test_scene

from ursina import *

def test_ursina_scene_vide(run_test_scene):
    run_ursina_for(run_test_scene,5)
    #Succes par défaut

def test_ursina_scene_test(run_test_scene):
    run_ursina_for(run_test_scene,5)
    
def test_position_sequence(run_test_scene):
    e = Entity(model='cube', collider='box', texture='shore', texture_scale=Vec2(2), color=hsv(.3,1,.5))
    s = Sequence(
    Wait(2),
    Func(e.animate_x,value=10, duration=1),  
    Func(print, 'Done!'),
    loop=False,
    )
    s.start()

    run_ursina_for(run_test_scene,6)
    #On peut tester après que Ursina ait roulé
    assert(e.position.x > 9.0)