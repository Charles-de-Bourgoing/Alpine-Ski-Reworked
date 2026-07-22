# physics.py 

# définit l'accélération, gère les colisions...


from ursina import Vec3, time

class SkiPhysics:
    def __init__(self):
        self.velocity = Vec3(0, 0, 0)
        self.gravity = 9.81
        self.friction_snow = 0.99   # Coefficient de glisse (proche de 1 = glisse fort)
        self.turn_speed = 100        # Vitesse de rotation en degrés/sec
        self.acceleration = 30      # Poussée de la pente vers le bas

    def apply_physics(self, player, ray_hit, keys):
        

        
        
        # 1. Orientation (Direction dans laquelle pointent les skis)
        turn = (keys['d'] - (keys['q'] or keys['a'])) * self.turn_speed * time.dt
        player.rotation_y += turn


        

        # 2. Accélération de la pente 
        forward_dir = player.forward
        if ray_hit.hit:
            ground_y = ray_hit.world_point.y

            if player.y <= ground_y + 0.05:
                player.y = ground_y
                
                normal = ray_hit.world_normal
                
                # 1. Projection de la gravite (0, -gravity, 0) sur le plan de la pente
                # Donnee par : g_proj = g - (g . n) * n
                gravity_vec = Vec3(0, -self.gravity, 0)
                slope_acceleration = gravity_vec - normal * gravity_vec.dot(normal)
                
                # Accélération réelle tirée par la pente
                self.velocity += slope_acceleration * time.dt

                # 2. Projection de la vitesse existante sur le plan de la pente
                if self.velocity.y < 0:
                    self.velocity -= normal * self.velocity.dot(normal)

                # 3. Alignement de la vitesse le long de l'axe des skis (friction latérale)
                current_speed = self.velocity.length()
                self.velocity = lerp(self.velocity, forward_dir * current_speed, 5 * time.dt)

                # 4. Friction de la neige
                self.velocity.x *= self.friction_snow
                self.velocity.z *= self.friction_snow
            else:
                # En l'air : gravite standard
                self.velocity.y -= self.gravity * time.dt
        else:
            # En l'air : gravite standard
            self.velocity.y -= self.gravity * time.dt

        # Application du mouvement
        player.position += self.velocity * time.dt