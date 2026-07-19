from ursina import *
class Player(Entity):
    def __init__(self, cam,**kwargs):
        super().__init__(
            model='cube', 
            color=color.orange, 
            origin=(-0.1, -0.1, -0.5),
            speed=8, 
            collider='box', 
            parent=cam,
            **kwargs
        )
        #self.player_model = Entity(model='player', parent=self)
        self.player_model = Entity(model='cube', parent=self)  # test temporaire
        self.controls = {'left': 'q', 'right': 'd'} # Configuration AZERTY
    #def update(self):
            # Logique de déplacement propre au joueur
            #self.x -= held_keys[self.controls['left']] * time.dt
            #self.x += held_keys[self.controls['right']] * time.dt
    #def input(self, key):
    #    if key == 'space':
    #        self.y += 1
    #        invoke(setattr, self, 'y', self.y - 1, delay=0.25)
