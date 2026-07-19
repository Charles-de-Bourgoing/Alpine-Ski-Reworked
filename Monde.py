# Monde.py

from ursina import *
global monde



class Level(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4),parent=self)
        #self.building = Entity(model='building', collider='box', texture='brick', parent=self)
        self.building = Entity(model='cube', collider='box', texture='brick', parent=self)  # test temporaire
        self.sky = Sky(parent=self)
        self.sun = DirectionalLight()
    def bake(self): #prépare le niveau
        self.sun.look_at(Vec3(1,-1,-1))
