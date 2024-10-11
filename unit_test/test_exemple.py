import pytest
from ursina import *
from .util import run_generic_test_scene

AVG_FPS = 60
def to_frames(seconds):
    return seconds * AVG_FPS

def run_ursina_for(app,seconds):
    for i in range(0,to_frames(seconds)):
        app.step()

@pytest.fixture
def start_ursina(): 
    app = Ursina()
    yield app
    app.shutdown()

@pytest.fixture
def run_test_scene():
    app = run_generic_test_scene()
    yield app
    app.shutdown()

def test_exemple_sequence(run_test_scene):
    e = Entity(model='cube', collider='box', texture='shore', texture_scale=Vec2(2), color=hsv(.3,1,.5))
    s = Sequence(
    Wait(2),
    Func(e.animate_x,value=10, duration=1),  
    Wait(1),
    Func(e.fade_out, duration=1),
    Wait(1),
    Func(print, 'Done!'),
    loop=False,
    )
    s.append(Func(assert_true))
    s.start()
    #Ligne qui démarre Ursina 8 secondes
    run_ursina_for(run_test_scene,8)


#Callback utilitaire
def assert_true():
    assert True

def assert_false():
    assert False