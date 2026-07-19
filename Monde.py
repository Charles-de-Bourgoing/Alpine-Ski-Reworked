# Monde.py

from ursina import *
global monde



class Level(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ground = Entity(model='quad', scale=10, y=-2, collider='box', parent=self)
        self.building = Entity(model='building', collider='box', parent=self)
