# physics.py 

# définit l'accélération, gère les colisions...


from ursina import Vec3, time

class SkiPhysics:
    def __init__(self):
        self.velocity = Vec3(0, 0, 0)
        self.gravity = 15
        #self.friction_snow = 0.99   # Coefficient de glisse (proche de 1 = glisse fort)
        self.turn_speed = 100        # Vitesse de rotation en degrés/sec
        #self.acceleration = 30      # Poussée de la pente vers le bas

        # Paramètres de la suspension (jambes)
        self.rest_height = 1.0       # Hauteur cible au-dessus du sol (mètres)
        self.stiffness = 0.05       # Raideur du ressort (k) : plus élevé = plus ferme
        self.damping = 1          # Amortissement (c) : évite le comportement "trampoline"

        # Attributs d'état exposés pour l'UI et la télémétrie
        self.current_height = self.rest_height
        self.suspension_compression = 0.0  # 0 = repos, >0 = comprimé, <0 = détendu

        #Pour le mode bâtons
        self.use_poles_mode = False
        self.pole_push_force = 15.0  # Force d'impulsion des bâtons
        self.pole_cooldown = 0.8     # Délai minimum entre deux coups de bâton (secondes)
        self.last_pole_time = 0.0

    def apply_physics(self, player, ray_hit, keys):
        

        
        
        # 1. Orientation (Direction dans laquelle pointent les skis)
        turn = (keys['d'] - (keys['q'] or keys['a'])) * self.turn_speed * time.dt
        player.rotation_y += turn


        

        # 2. Accélération de la pente 
        forward_dir = player.forward
        if ray_hit.hit:
            ground_y = ray_hit.world_point.y
            self.current_height = player.y - ground_y
            self.suspension_compression = self.rest_height - self.current_height

            # On est en contact avec la suspension si on descend sous la hauteur de repos + marge
            if self.current_height <= self.rest_height + 0.2:
                #player.y = ground_y

                # Poussée des bâtons (si l'option est activée, au sol, et touche appuyée)
                if self.use_poles_mode and keys['space']:
                    current_time = time.time()
                    if current_time - self.last_pole_time >= self.pole_cooldown:
                        # Impulsion vers l'avant selon l'axe des skis
                        self.velocity += forward_on_slope * self.pole_push_force
                        self.last_pole_time = current_time

                
                normal = ray_hit.world_normal




                
                # 1. Direction avant projetée sur la pente
                forward_on_slope = (player.forward - normal * player.forward.dot(normal)).normalized()
                
                # 2. Construction d'un axe latéral STRICTEMENT orthogonal sur la pente (produit vectoriel)
                # Garantit que <forward_on_slope, right_on_slope> = 0 (pas d'injection d'énergie)
                right_on_slope = forward_on_slope.cross(normal).normalized()
                


                # 3. Projection de la pesanteur sur la pente
                gravity_vec = Vec3(0, -self.gravity, 0)
                slope_acc = gravity_vec - normal * gravity_vec.dot(normal)
                self.velocity += slope_acc * time.dt

                # 4. Décomposition dans la base orthogonale pure
                v_forward_mag = self.velocity.dot(forward_on_slope)
                v_right_mag = self.velocity.dot(right_on_slope)

                # 5. Amortissement pur du dérapage latéral sans altérer la vitesse avant
                v_right_mag = lerp(v_right_mag, 0.0, 3 * time.dt)

                # 6. Reconstruction exacte sans création d'énergie parasite
                self.velocity = (forward_on_slope * v_forward_mag) + (right_on_slope * v_right_mag)
                

                """# 7. Suspension (appliquée APRÈS la reconstruction pour ne pas contaminer la glisse)
                raw_displacement = self.current_height - self.rest_height

                # Bornage strict : [-0.2, +0.6] par rapport à rest_height
                # Hauteur bloquée entre 0.4m (compression max) et 1.2m (extension max)
                clamped_height = max(self.rest_height - 0.6, min(self.rest_height + 0.2, self.current_height))

                # Réajustement de la position du joueur si on dépasse les limites physiques des jambes
                if self.current_height != clamped_height:
                    player.y = ground_y + clamped_height
                    self.current_height = clamped_height

                displacement = self.current_height - self.rest_height
                self.suspension_compression = -displacement"""

                # 7. Suspension : calcul dynamique de la hauteur et compression
                displacement = self.current_height - self.rest_height  # négatif si enfoncé (< 1.0)

                # Force pure du ressort amorti (sans verrouiller player.y artificiellement)
                spring_force = -self.stiffness * displacement
                damping_force = -self.damping * self.velocity.y
                self.velocity.y += (spring_force + damping_force) * time.dt

                # Limitation stricte de la compression physique enregistrée [-0.2, 0.6]
                self.suspension_compression = max(-0.2, min(0.6, -displacement))

                # Force du ressort + compensation de la gravité statique pour équilibre à 1.0m
                spring_force = (-self.stiffness * displacement) + self.gravity
                damping_force = -self.damping * self.velocity.y
                
                self.velocity.y += (spring_force + damping_force) * time.dt

                # 8. Friction réelle de la neige (soustraction physique amortie par time.dt)

                drag_force = 0.5 # Ajuster la résistance de la neige
                if self.velocity.length() > 0:
                    self.velocity -= self.velocity.normalized() * drag_force * time.dt
            else:
                # En l'air (au-dessus du sol) : chute libre + détente lissée
                self.velocity.y -= self.gravity * time.dt
                self.suspension_compression = max(-0.2, min(0.6, lerp(self.suspension_compression, 0.0, 10.0 * time.dt)))
                self.current_height = self.rest_height - self.suspension_compression
        else:
            # En l'air (aucun sol détecté) : chute libre + détente lissée
            self.velocity.y -= self.gravity * time.dt
            self.suspension_compression = max(-0.2, min(0.6, lerp(self.suspension_compression, 0.0, 10.0 * time.dt)))
            self.current_height = self.rest_height - self.suspension_compression
        # Application du mouvement
        player.position += self.velocity * time.dt