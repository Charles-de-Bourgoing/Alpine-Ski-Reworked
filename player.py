from ursina import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube', 
            color=color.orange, 
            scale_y=2, 
            **kwargs
        )
        self.player_model = Entity(model='player', parent=self)
        self.controls = {'left': 'a', 'right': 'd'} # Configuration QWERTY -> AZERTY

    def update(self):
        # Logique de déplacement propre au joueur
        self.x -= held_keys[self.controls['left']] * time.dt
        self.x += held_keys[self.controls['right']] * time.dt

    def input(self, key):
        if key == 'space':
            self.y += 1
            invoke(setattr, self, 'y', self.y - 1, delay=0.25)