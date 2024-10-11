from ursina import *
from ursina.shaders import lit_with_shadows_shader

def run_generic_scene():
    app = Ursina()
    app.border_less = False
    d = DirectionalLight(False)
    d.look_at(Vec3(1,-1,1))
    shader = lit_with_shadows_shader
    en = Entity(model='plane', scale=50, texture='grass',shader=shader)
    sk = Sky(color=color.light_gray)
    cam = EditorCamera(position=Vec3(0,50,-100),rotation=(27,0,0))
    return app

class TriggerTestFailureEntity(Entity):
    def input(self,key):
        if key == "f":
            assert(False)

def run_generic_test_scene():
    app = run_generic_scene()
    f = Text(text='Appuyer sur F pour échouer le test!')
    e = TriggerTestFailureEntity()
    return app

