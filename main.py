from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from direct.stdpy import thread # we need threading to load entities in the background (this is specific to ursina, standard threading wouldn't work)
from UI import *
import monde
import player




def showMenu():
    MenuManager()
    


# Source - https://stackoverflow.com/a/65962467
# Posted by cr8f2kvi9b7gqpf1, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-19, License - CC BY-SA 4.0

touches_a = ['w','a','s','d']
touches = ['z','q','s','d']
P1 = None
play = None
editor_camera = None
gun = None
input = pause_input


if __name__ == '__main__':
    app = Ursina()


    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader

    showMenu()

  
    app.run()


# creation du monde


