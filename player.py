from ursina import *
from physics import SkiPhysics

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube',
            scale=(0.8, 1.8, 0.5), # Proportion plus proche d'un skieur
            color=color.orange,
            origin_y=-0.5,
            collider='box',
            **kwargs
        )
        self.physics = SkiPhysics()
        #self.speed = 8
        #self.jump_force = 0.5
        #self.gravity = 0.5
        #self.velocity_y = 0
        self.controls = {'left': 'q', 'right': 'd', 'forward': 'z', 'back': 's', 'jump': 'space'}

        def snap_to_ground(self):
            # Raycast vers le bas depuis une hauteur sûre (ex: Y=100)
            ray = raycast(self.world_position + Vec3(0, 100, 0), Vec3(0, -1, 0), distance=200)
            if ray.hit:
                self.y = ray.world_point.y + 0.5 # Mettre le pivot légèrement au-dessus

        snap_to_ground(self)  # Appel initial pour positionner le joueur sur le sol
        camera.parent = self            # La caméra suit le joueur et pivote avec lui
        camera.position = (0, 4, -10)   # Offset relatif : 4m au-dessus, 10m derrière le pivot
        camera.rotation = (15, 0, 0)    # Incline la caméra de 15° vers le bas

    def update(self):
        # Raycast sous le joueur pour détecter la hauteur exacte du terrain déformé
        #hit_info = raycast(self.world_position + Vec3(0, 1, 0), Vec3(0, -1, 0), distance=3, ignore=(self,))
        
        # Application du moteur physique
                # 0. Raycast de sécurité : part de 5 unités AU-DESSUS du joueur
        ray_origin = self.world_position + Vec3(0, 5, 0)
        ray_hit = raycast(ray_origin, Vec3(0, -1, 0), distance=10, ignore=(self,))
        
        self.physics.apply_physics(self, ray_hit,held_keys)
        
        
        
        """# Déplacement
        direction = Vec3(
            (held_keys[self.controls['right']] - held_keys[self.controls['left']]),
            0,
            (held_keys[self.controls['forward']] - held_keys[self.controls['back']])
        ).normalized()
        self.position += direction * self.speed * time.dt

        # Saut et gravité
        if held_keys[self.controls['jump']] and self.y <= 0.5:
            self.velocity_y = self.jump_force
        self.velocity_y -= self.gravity * time.dt
        self.y += self.velocity_y * time.dt

        # Collision avec le sol
        if self.y < 0.5:
            self.y = 0.5
            self.velocity_y = 0"""