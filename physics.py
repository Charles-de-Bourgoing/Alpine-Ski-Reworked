# physics.py 

# définit l'accélération, gère les colisions...


from ursina import Vec3, time

class SkiPhysics:
    def __init__(self):
        self.velocity = Vec3(0, 0, 0)
        self.gravity = 9.81
        self.friction_snow = 0.98   # Coefficient de glisse (proche de 1 = glisse fort)
        self.turn_speed = 100        # Vitesse de rotation en degrés/sec
        self.acceleration = 12      # Poussée de la pente vers le bas

    def apply_physics(self, player, ray_hit, keys):
        

        
        
        # 1. Orientation (Direction dans laquelle pointent les skis)
        turn = (keys['d'] - (keys['q'] or keys['a'])) * self.turn_speed * time.dt
        player.rotation_y += turn


        

        # 2. Accélération de la pente (pousse toujours vers l'axe -Z)
        forward_dir = player.forward
        self.velocity += forward_dir * self.acceleration * time.dt

        # 3. Alignement de l'inertie vers l'avant des skis (friction latérale)
        current_speed = self.velocity.length()
        self.velocity = lerp(self.velocity, forward_dir * current_speed, 5 * time.dt)



        if ray_hit.hit:
            #print("normale: " + str(ray_hit.world_normal))
            ground_y = ray_hit.world_point.y

            # Si le joueur touche ou passe sous le sol
            if player.y <= ground_y:
                #print("player sous sol" + str(player.y) + " ground: " + str(ground_y))
                # Repoussement au-dessus du sol (évite de s'enfoncer)
                player.y = ground_y
                
                # Conversion de la vitesse verticale en glisse selon la normale
                normal = ray_hit.world_normal
                if self.velocity.y < 0:
                    # Projection du vecteur vitesse sur le plan du sol
                    self.velocity -= normal * self.velocity.dot(normal)

                # Accélération due à la pente
                slope_pull = Vec3(normal.x, 0, normal.z) * self.gravity
                self.velocity += slope_pull * time.dt




        #else:
            # En l'air : chute libre
            #self.velocity.y -= self.gravity * time.dt
        # 4. Inertie / Friction : la vitesse s'aligne progressivement sur l'orientation des skis
        self.velocity.y -= self.gravity * time.dt
        
        self.velocity.x *= self.friction_snow
        self.velocity.z *= self.friction_snow
        # 6. Application du mouvement
        player.position += self.velocity * time.dt