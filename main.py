from ursina import *


app = Ursina()

player = Entity(model='cube', color=color.orange, scale_y=2)

touches_a = ['w','a','s','d']
touches = ['z','q','s','d']
def update():
    player.x -= held_keys[touches_a[1]] * time.dt
    player.x += held_keys[touches_a[3]] * time.dt

def input(key):
    if key == 'space':
        player.y += 1
        invoke(setattr, player, 'y', player.y-1, delay=.25)
    

# creation du monde



app.run()