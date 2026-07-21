# Monde.py

from ursina import *
from perlin_noise import PerlinNoise
#from lamp import ambient_light



class Level(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4),parent=self)
        #self.building = Entity(model='building', collider='box', texture='brick', parent=self)
        #self.building = Entity(model='cube', collider='box', texture='brick', parent=self)  # test temporaire
        self.sky = Sky(parent=self)
        self.sun = DirectionalLight()
        #scene.ambient_light.color = Vec4(0.2, 0.2, 0.2, 1.0)
        self.sun.color = Vec4(0.9, 0.9, 0.95, 1.0)
    def bake(self): #prépare le niveau
        self.sun.look_at(Vec3(1,-1,-1))

from ursina.shaders import lit_with_shadows_shader # Import du shader

class TerrainChunk(Entity):
    def __init__(self, subdivision=32, **kwargs):
        print("!!!!!!!!!!!!!!!!!!!!!!")

        super().__init__(
                        model=Plane(subdivisions=(subdivision, subdivision)),
                          texture='snow_texture_6',
                          shader=lit_with_shadows_shader,
                            **kwargs)
        #texture='noise',
        self.color = Vec4(230/255, 245/255, 255/255, 1.0)
        self.noise = PerlinNoise(octaves=4, seed=1)
        self.generate_relief()

        
    def generate_relief(self):
        mesh = self.model
        scale_x, scale_z = self.scale_x, self.scale_z

        for v in mesh.vertices:

            # Conversion en coordonnees MONDE reelles
            world_x = self.x + (v[0] * scale_x)
            world_z = self.z + (v[2] * scale_z)

            base_slope = -world_z * 0.7 
            edge_factor = 1 + (abs(world_x) * 0.05)
            bosses = self.noise([world_x * 0.05, world_z * 0.05]) * 2 * edge_factor
            v[1] = base_slope + bosses

        # On multiplie les coordonnées UV locales par 20 pour répéter l'image 20 fois
        mesh.uvs = [[v[0] * 20, v[2] * 20] for v in mesh.vertices]
        mesh.generate_normals()
        for i, n in enumerate(mesh.normals):
            # Si le produit vectoriel a inverse la normale vers le bas/cote, on la redresse
            if n[1] < 0.2:
                
                mesh.normals[i] = Vec3(n[0], abs(n[1]) + 0.8, n[2]).normalized()
                print("normale redressée: " + str(mesh.normals[i]))

        mesh.generate()
        self.collider = 'mesh'

class WorldManager(Entity):
    def __init__(self, player_entity, **kwargs):
        super().__init__(**kwargs)
        self.player = player_entity
        self.taille_chunk = 100
        self.time_elapsed = 0
        self.check_interval = 0.2  # Vérification toutes les 0.2 secondes
        
        # Initialisation des premiers chunks
        self.chunks = [
            TerrainChunk(scale=(self.taille_chunk, 1, self.taille_chunk), z=0),
            TerrainChunk(scale=(self.taille_chunk, 1, self.taille_chunk), z=-self.taille_chunk),
            TerrainChunk(scale=(self.taille_chunk, 1, self.taille_chunk), z=-self.taille_chunk * 2)
        ]

    def update(self):
        # Temporisateur pour ne pas check à chaque frame
        self.time_elapsed += time.dt
        if self.time_elapsed < self.check_interval:
            return
        self.time_elapsed = 0  # Réinitialisation du timer
        
        # Logique de recyclage
        for chunk in self.chunks:
            # Si le joueur a dépassé ce chunk en descendant (axe Z négatif)
            if self.player.z < chunk.z - self.taille_chunk*0.75:
                # On le déplace commercialement devant le chunk le plus éloigné
                plus_loin_z = min(c.z for c in self.chunks)
                chunk.z = plus_loin_z - self.taille_chunk
                # Régénération du relief pour la nouvelle position
                chunk.generate_relief()
                chunk.collider = 'mesh' # Re-générer la collision !