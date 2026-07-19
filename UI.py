from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.stdpy import thread
from player import Player
from monde import Level
global P1, gun, cam, editor_camera

class MenuManager:
    def __init__(self):
        self.play_button = Button('Play', on_click=self.show_loading_screen)
        self.loading_screen = None


    def show_loading_screen(self):
        destroy(self.play_button)
        self.loading_screen = Entity(model='quad', texture='loading_image')
        # Chargement en arrière-plan
        thread.start_new_thread(function=self.load_level, args=())

    def load_level(self):
        # Instanciation des modules externes
        global level, cam, P1, gun, editor_camera
        level = Level()
        cam = FirstPersonController()
        #cam.input_axis = 'wasd'
        camera.position = (0, 3, -10)  # recule la caméra en arrière et en hauteur
        P1 = Player(cam)                # plus besoin de z=-10 ici
        gun = Entity(model='cube', parent=cam, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False)
        gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
        editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        destroy(self.loading_screen)

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        P1.visible_self = editor_camera.enabled
        P1.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = P1.position

        application.paused = editor_camera.enabled
