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
    def __init__(self, size=100, subdivision=32, **kwargs):
        print("!!!!!!!!!!!!!!!!!!!!!!")
        self.size = size
        self.subdivision = subdivision
        self.noise=PerlinNoise(octaves=4, seed=1)
        


        super().__init__(
                          texture='snow_texture_6',
                          color = Vec4(230/255, 245/255, 255/255, 1.0),
                          scale=(1,1,1),
                          shader=lit_with_shadows_shader,
                            **kwargs)
        #texture='noise',

        custom_mesh=self.generate_mesh()
        self.collider = 'mesh'




        
    def generate_mesh(self):
        vertices = []
        triangles = []
        uvs = []

        sub = self.subdivision
        step = self.size / sub
        #mesh = self.model
        #scale_x, scale_z = self.scale_x, self.scale_z


        # Generation des sommets en coordonnees reelles (de -size/2 a +size/2)
        for z_idx in range(sub + 1):
            for x_idx in range(sub + 1):
                # Coordonnees locales egales aux coordonnees monde
                local_x = (x_idx * step) - (self.size / 2)
                local_z = (z_idx * step) - (self.size / 2)
                world_x = self.x + local_x
                world_z = self.z + local_z

                # Calcul du relief
                base_slope = -world_z * 0.7
                edge_factor = 1 + (abs(world_x) * 0.05)
                bosses = self.noise([world_x * 0.05, world_z * 0.05]) * 2 * edge_factor
                height = base_slope + bosses

                vertices.append(Vec3(local_x, height, local_z))
                uvs.append((x_idx / sub * 10, z_idx / sub * 10))


        # Construction des triangles (ordre CCW pour normales orientees vers le haut)
        for z_idx in range(sub):
            for x_idx in range(sub):
                i = z_idx * (sub + 1) + x_idx
                # Triangle 1
                triangles.append((i, i + sub + 1, i + 1))
                # Triangle 2
                triangles.append((i + 1, i + sub + 1, i + sub + 2))

        # 3. Assemblage du Mesh Ursina
        m = Mesh(
            vertices=vertices,
            triangles=triangles,
            uvs=uvs,
            mode='triangle'
        )

 
        m.generate_normals()
        m.generate()
        self.model = m
        self.double_sided = True
        self.collider = None
        self.collider = MeshCollider(self, mesh=m)  # Re-générer le collider avec le nouveau maillage

class WorldManager(Entity):
    def __init__(self, player_entity, **kwargs):
        super().__init__(**kwargs)
        self.player = player_entity
        self.taille_chunk = 100
        self.time_elapsed = 0
        self.check_interval = 0.2  # Vérification toutes les 0.2 secondes
        
        # Initialisation des premiers chunks
        self.chunks = [
            TerrainChunk(size=self.taille_chunk, z=0),
            TerrainChunk(size=self.taille_chunk, z=self.taille_chunk),
            TerrainChunk(size=self.taille_chunk, z=self.taille_chunk * 2)
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
            if self.player.z > chunk.z + self.taille_chunk*0.5:
                # On le déplace commercialement devant le chunk le plus éloigné
                plus_loin_z = max(c.z for c in self.chunks)
                chunk.z = plus_loin_z + self.taille_chunk
                # Régénération du relief pour la nouvelle position
                chunk.generate_mesh()
                chunk.collider = 'mesh' # Re-générer la collision !