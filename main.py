from unit_test.util import run_generic_scene
from ursina import *
from ursina.shaders import lit_with_shadows_shader

app = run_generic_scene() 
application.hot_reloader.hotreload = True
#Votre code

e = Entity(model='cube', scale=5, texture='grass',shader=lit_with_shadows_shader)

#Fin de votre code
app.run()