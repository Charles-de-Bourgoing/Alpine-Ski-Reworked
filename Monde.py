# Monde.py

from ursina import *
global monde
from perlin_noise import PerlinNoise



class Level(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ground = Entity(model='quad', scale=10, y=-2, collider='box', parent=self)
        self.building = Entity(model='building', collider='box', parent=self)


class TerrainChunk(Entity):
    def __init__(self, subdivision=32, **kwargs):
        super().__init__(
            model=Plane(subdivisions=(subdivision, subdivision)), 
            texture='snow_texture', 
            **kwargs
        )
        self.subdivision = subdivision
        self.generate_relief()
        
    def generate_relief(self):
        # Récupération des vertices du mesh Ursina
        mesh = self.model
        for v in mesh.vertices:
            # Coordonnées globales absolues pour la continuité du bruit
            global_x = v[0] + self.x
            global_z = v[2] + self.z
            
            # 1. Calcul de la pente de base
            base_slope = -global_z * 0.1 
            
            # 2. Ajout du bruit pour les bosses (Perlin Noise)
            # Plus on s'éloigne du centre (global_x), plus le relief est fort (vallées)
            edge_factor = abs(global_x) * 0.5
            bosses = pnoise2(global_x * 0.1, global_z * 0.1) * edge_factor
            
            # Application de la hauteur
            v[1] = base_slope + bosses
            
        # Re-calcul des normales pour la lumière et application des changements
        mesh.generate()