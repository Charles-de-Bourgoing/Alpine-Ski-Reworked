from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.stdpy import thread
from player import Player
from monde import *
global P1, gun, cam, editor_camera

class MenuManager:
    def __init__(self):
        self.play_button = Button('Play', on_click=self.show_loading_screen)
        self.loading_screen = None

    def show_loading_screen(self):
        destroy(self.play_button)
        self.loading_screen = Entity(model='quad', texture='loading_image')
        thread.start_new_thread(function=self.load_level, args=())

    def load_level(self):
        global level, P1, gun
        level = Level()
        P1 = Player()  # Le joueur est une entité indépendante
        gun = Entity(model='cube', parent=P1, position=(0.5, -0.25, 0.25), scale=(0.3, 0.2, 1), color=color.red)
        WManager = WorldManager(P1)
        destroy(self.loading_screen)

# Fonction globale pour suivre le joueur avec la caméra
def update():
    if 'P1' in globals() and P1:
        # Positionne la caméra derrière et au-dessus du joueur
        camera.position = P1.position + Vec3(0, 4, -10)
        camera.look_at(P1)