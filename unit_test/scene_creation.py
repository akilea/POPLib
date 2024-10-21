from ursina import *
from ursina.shaders import lit_with_shadows_shader
from .sample_texture import *

DEFAULT_WORLD_SCREEN_BORDER_BOUNDARY_SIZE = 40.0
DEFAULT_WORLD_SCREEN_BORDER_BOUNDARY_HALF_SIZE = 40.0
DEFAULT_WORLD_SCREEN_BORDER_BOUNDARY_MAX = Vec2(DEFAULT_WORLD_SCREEN_BORDER_BOUNDARY_HALF_SIZE,DEFAULT_WORLD_SCREEN_BORDER_BOUNDARY_HALF_SIZE)
DEFAULT_WORLD_SCREEN_BORDER_BOUNDARY_MIN = -DEFAULT_WORLD_SCREEN_BORDER_BOUNDARY_MAX
DEFAULT_WORLD_SIZE = 50.0
DEFAULT_WORLD_HEIGHT = 3.0
DEFAULT_WORLD_HALF_HEIGHT = DEFAULT_WORLD_HEIGHT*0.5
DEFAULT_WORLD_HALF_SIZE = DEFAULT_WORLD_SIZE*0.5
DEFAULT_VELOCITY_MIN = 0.0
DEFAULT_VELOCITY_MAX = 20.0

def run_generic_scene():
    app = Ursina()
    app.border_less = False
    d = DirectionalLight(False)
    d.look_at(Vec3(1,-1,1))
    en = Entity(model='plane', scale=DEFAULT_WORLD_SIZE, texture='grass',shader=lit_with_shadows_shader)
    sk = Sky(color=color.light_gray)
    cam = EditorCamera(position=Vec3(0,50,-100),rotation=(27,0,0))
    return app

def run_level_grass_scene():
    app = run_generic_scene()
    border_right = Entity(model='cube', scale=Vec3(1,DEFAULT_WORLD_HEIGHT,DEFAULT_WORLD_SIZE), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_right.set_position(Vec3(DEFAULT_WORLD_HALF_SIZE,DEFAULT_WORLD_HALF_HEIGHT,0))

    border_left = Entity(model='cube', scale=Vec3(1,DEFAULT_WORLD_HEIGHT,DEFAULT_WORLD_SIZE), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_left.set_position(Vec3(-DEFAULT_WORLD_HALF_SIZE,DEFAULT_WORLD_HALF_HEIGHT,0))

    border_up = Entity(model='cube', scale=Vec3(DEFAULT_WORLD_SIZE,DEFAULT_WORLD_HEIGHT,0.0), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_up.set_position(Vec3(0,DEFAULT_WORLD_HALF_HEIGHT,DEFAULT_WORLD_HALF_SIZE))

    border_dpwn = Entity(model='cube', scale=Vec3(DEFAULT_WORLD_SIZE,DEFAULT_WORLD_HEIGHT,0.0), texture=brick_wall,shader=lit_with_shadows_shader,texture_scale=Vec2(10,1))
    border_dpwn.set_position(Vec3(0,DEFAULT_WORLD_HALF_HEIGHT,-DEFAULT_WORLD_HALF_SIZE))
    return app

class TriggerTestFailureEntity(Entity):
    def input(self,key):
        if key == "f":
            assert(False)

def run_generic_test_scene():
    app = run_generic_scene()
    f = Text(text='Appuyer sur F pour échouer le test!')
    f.position = Vec3(-1,0.15,0)
    f.origin = Vec2(0,0)
    f.color = color.red
    e = TriggerTestFailureEntity()
    return app

def create_expected_result_text(expect_result : str)->None:
    f = Text(text=expect_result)
    f.color = color.green
    f.position = Vec3(-0.7,0.15,0)