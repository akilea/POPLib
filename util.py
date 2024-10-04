from ursina import *
from ursina.shaders import *
from ursina.lights import DirectionalLight

def init_scene():
    app = Ursina(borderless=False)

    shader = lit_with_shadows_shader
    Entity(model='plane', scale=16, texture='grass', shader=shader)
    sun = DirectionalLight(shadow_map_resolution=(2048,2048))
    sun.look_at(Vec3(-1,-1,-10))
    scene.fog_density = (1, 50)

    Sky(color=color.light_gray)


    EditorCamera()
    #app.toggle_wireframe()
    # camera.position = Vec3(1,10,0)
    # camera.look_at(Vec3(0,0,0))
    return app
