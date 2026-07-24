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
        self.rest_height = 0.8       # Hauteur cible au-dessus du sol (mètres)
        self.stiffness = 0.0005       # Raideur du ressort (k) : plus élevé = plus ferme
        self.damping = 0.01          # Amortissement (c) : évite le comportement "trampoline"

        # Attributs d'état exposés pour l'UI et la télémétrie
        self.current_height = self.rest_height
        self.suspension_compression = 0.0  # 0 = repos, >0 = comprimé, <0 = détendu

        #Pour le mode bâtons
        self.use_poles_mode = False
        self.pole_push_force = 40.0  # Force d'impulsion des bâtons
        self.pole_duration = 0.4        # Durée de poussée active (s)
        self.pole_cooldown = 0.6        # Intervalle total entre 2 coups (s)
        self.pole_active_time = 0.0     # Compteur restant de poussée
        self.pole_cooldown_timer = 0.0  # Compteur restant de recharge

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

                

                
                normal = ray_hit.world_normal




                
                # 1. Direction avant projetée sur la pente
                forward_on_slope = (player.forward - normal * player.forward.dot(normal)).normalized()
                
                # 2. Construction d'un axe latéral STRICTEMENT orthogonal sur la pente (produit vectoriel)
                # Garantit que <forward_on_slope, right_on_slope> = 0 (pas d'injection d'énergie)
                right_on_slope = forward_on_slope.cross(normal).normalized()
                
                # Poussée des bâtons (si l'option est activée, au sol, et touche appuyée)
                # 1. Décrémentation des timers globaux (en dehors des conditions de touche)
                if self.pole_active_time > 0:
                    self.pole_active_time -= time.dt
                if self.pole_cooldown_timer > 0:
                    self.pole_cooldown_timer -= time.dt

                # 2. Déclenchement d'un nouveau cycle (si espace appuyé, au sol, et hors cooldown/poussée)
                if self.use_poles_mode and keys['space'] and self.pole_active_time <= 0 and self.pole_cooldown_timer <= 0:
                    self.pole_active_time = self.pole_duration
                    self.pole_cooldown_timer = self.pole_cooldown  # Durée totale du cycle (ex: 0.6s)

                # 3. Application de la force (se termine naturellement même si espace est relâché)
                if self.pole_active_time > 0:
                    self.velocity += forward_on_slope * self.pole_push_force * time.dt

                # 3. Projection de la pesanteur sur la pente
                gravity_vec = Vec3(0, -self.gravity, 0)
                slope_acc = gravity_vec - normal * gravity_vec.dot(normal)
                self.velocity += slope_acc * time.dt

                # 4. Décomposition dans la base orthogonale pure
                v_forward_mag = self.velocity.dot(forward_on_slope)
                v_right_mag = self.velocity.dot(right_on_slope)

                # 5. Amortissement pur du dérapage latéral sans altérer la vitesse avant
                v_right_mag = lerp(v_right_mag, 0.0, 5 * time.dt)

                # 6. Reconstruction exacte sans création d'énergie parasite
                self.velocity = (forward_on_slope * v_forward_mag) + (right_on_slope * v_right_mag)
                

                # 7. Suspension : calcul dynamique de la hauteur et compression
                displacement = self.current_height - self.rest_height  # négatif si enfoncé (< 1.0)

                # Force pure du ressort amorti (sans verrouiller player.y artificiellement)
                spring_force = -self.stiffness * displacement
                damping_force = -self.damping * self.velocity.y
                self.velocity.y += (spring_force + damping_force) * time.dt

                # Limitation stricte de la compression physique enregistrée [-0.2, 0.6]
                self.suspension_compression = max(-0.6, min(0.6, -displacement))

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