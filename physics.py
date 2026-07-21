# physics.py 

# définit l'accélération, gère les colisions...


from ursina import Vec3, time

class SkiPhysics:
    def __init__(self):
        self.velocity = Vec3(0, 0, 0)
        self.gravity = 9.81
        self.friction_snow = 0.98   # Coefficient de glisse (proche de 1 = glisse fort)
        self.turn_speed = 90        # Vitesse de rotation en degrés/sec
        self.acceleration = 12      # Poussée de la pente vers le bas

    def apply_physics(self, player, raycast_hit):
        # 1. Orientation (Direction dans laquelle pointent les skis)
        turn = (held_keys['d'] - held_keys['q']) * self.turn_speed * time.dt
        player.rotation_y += turn

        # 2. Vecteur directionnel des skis (axe avant)
        forward_dir = player.forward

        # 3. Accélération de la pente (pousse toujours vers l'axe -Z)
        self.velocity.z -= self.acceleration * time.dt

        # 4. Inertie / Friction : la vitesse s'aligne progressivement sur l'orientation des skis
        self.velocity.x *= self.friction_snow
        self.velocity.z *= self.friction_snow

        # 5. Gravité et Collision Sol
        if raycast_hit.hit:
            # Repoussement au-dessus du sol (évite de s'enfoncer)
            target_y = raycast_hit.world_point.y + 0.5
            if player.y < target_y:
                player.y = target_y
                self.velocity.y = 0
        else:
            # En l'air : chute libre
            self.velocity.y -= self.gravity * time.dt

        # 6. Application du mouvement
        player.position += self.velocity * time.dt