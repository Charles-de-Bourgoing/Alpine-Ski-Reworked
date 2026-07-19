from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from direct.stdpy import thread # we need threading to load entities in the background (this is specific to ursina, standard threading wouldn't work)
from UI import *
import monde
import player


    

def loadLevel():    
    global loading_screen, player,gun,editor_camera
    #ground = Entity(model='quad', scale=10, y=-2, collider='box') # dummy entities
    cam = FirstPersonController()
    player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
    #player = Entity(model='cube', origin = (0, 0, -2), color=color.orange, scale_y=2, parent=cam)
    editor_camera = EditorCamera(enabled=False, ignore_paused=True)
    gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False)
    gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
    #player_model = Entity(model='player', parent=player)
    building = Entity(model='building', collider='box')
    Sky()
    sun = DirectionalLight()
    sun.look_at(Vec3(1,-1,-1))
    ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
    editor_camera = EditorCamera(enabled=False, ignore_paused=True)
    pause_handler = Entity(ignore_paused=True, input=pause_input)
    
    
    destroy(loading_screen) # delete the loading screen when finished



def showMenu():
    MenuManager()
    


# Source - https://stackoverflow.com/a/65962467
# Posted by cr8f2kvi9b7gqpf1, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-19, License - CC BY-SA 4.0

touches_a = ['w','a','s','d']
touches = ['z','q','s','d']
player = None
play = None
editor_camera = None
gun = None

def update():
    if player is None:
        return
    player.x -= held_keys[touches_a[1]] * time.dt
    player.x += held_keys[touches_a[3]] * time.dt
    #self.look_at_2d(player.position, 'y')

def input(key):
    if player is None:
        return
    if key == 'space':
        player.y += 1
        invoke(setattr, player, 'y', player.y-1, delay=.25)

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled


if __name__ == '__main__':
    app = Ursina()
    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader

    screen = None # for global statement
    showMenu()
    
    
  
    app.run()


# creation du monde


