from ursina import *
from unit_test.manual_app_runner import run_ursina_for, assert_true, assert_false

#Toutes les méthodes de test doivent avoir le préfixe test_ dans un fichier  avec le préfixe test_.
def test_basique_succes():
    assert 1 == 1

def test_basique_echec():
    assert 1 == 2

#Les fixtures sont contenus dans conftest.py. PyTest les détecte automatiquement dans ce fichier.
def test_sequence(run_test_scene):
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
    s.start()

    #Ligne qui démarre Ursina 8 secondes
    run_ursina_for(run_test_scene,8)
    #Succès par défaut

def test_position(run_test_scene):
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