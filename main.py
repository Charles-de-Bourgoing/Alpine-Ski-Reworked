from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from direct.stdpy import thread # we need threading to load entities in the background (this is specific to ursina, standard threading wouldn't work)
from UI import *
from monde import *

def showMenu():
    MenuManager()
    
touches_a = ['w','a','s','d']
touches = ['z','q','s','d']
P1 = None
play = None
editor_camera = None
gun = None
#input = pause_input


if __name__ == '__main__':
    app = Ursina()


    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader

    showMenu()

  
    app.run()