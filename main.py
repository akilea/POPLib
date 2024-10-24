from unit_test.scene_creation import run_basic_scene
from ursina import *
from ursina.shaders import lit_with_shadows_shader

app = run_basic_scene() 
application.hot_reloader.hotreload = True
#Votre code

e = Entity(model='cube', scale=5, texture='grass',shader=lit_with_shadows_shader)

#Fin de votre code
app.run()