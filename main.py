from ursina import *


from direct.stdpy import thread # we need threading to load entities in the background (this is specific to ursina, standard threading wouldn't work)



    

def loadLevel():    
    global loading_screen, player
    ground = Entity(model='quad', scale=10, y=-2, collider='box') # dummy entities
  
    player = Entity(model='cube', color=color.orange, scale_y=2)
    player_model = Entity(model='player', parent=player)
    building = Entity(model='building', collider='box')
    
    
    destroy(loading_screen) # delete the loading screen when finished

def showLoadingScreen():    
    global loading_screen,play
    destroy(play) # delete the play button when clicked
    loading_screen = Entity(model='quad', texture='loading_image')
    thread.start_new_thread(function=loadLevel, args=()) # load entities in the background

def showMenu():
    global play
    play = Button('Play', on_click=showLoadingScreen) # A play button that show the loading menu when clicked
# Source - https://stackoverflow.com/a/65962467
# Posted by cr8f2kvi9b7gqpf1, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-19, License - CC BY-SA 4.0

touches_a = ['w','a','s','d']
touches = ['z','q','s','d']
player = None
play = None

def update():
    if player is None:
        return
    player.x -= held_keys[touches_a[1]] * time.dt
    player.x += held_keys[touches_a[3]] * time.dt

def input(key):
    if player is None:
        return
    if key == 'space':
        player.y += 1
        invoke(setattr, player, 'y', player.y-1, delay=.25)

if __name__ == '__main__':
    app = Ursina()

    screen = None # for global statement
    showMenu()
    
    
  
    app.run()


# creation du monde


