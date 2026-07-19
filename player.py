from ursina import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube',
            color=color.orange,
            origin_y=-0.5,
            collider='box',
            **kwargs
        )
        self.speed = 8
        self.jump_force = 0.5
        self.gravity = 0.5
        self.velocity_y = 0
        self.controls = {'left': 'q', 'right': 'd', 'forward': 'z', 'back': 's', 'jump': 'space'}

    def update(self):
        # Déplacement
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
            self.velocity_y = 0