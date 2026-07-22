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
                
                # 1. Direction avant projetée sur la pente
                forward_on_slope = (player.forward - normal * player.forward.dot(normal)).normalized()
                
                # 2. Construction d'un axe latéral STRICTEMENT orthogonal sur la pente (produit vectoriel)
                # Garantit que <forward_on_slope, right_on_slope> = 0 (pas d'injection d'énergie)
                right_on_slope = forward_on_slope.cross(normal).normalized()
                
                """# 2. Projection de la GRAVITÉ sur l'axe longitudinal et latéral des skis
                gravity_vec = Vec3(0, -self.gravity, 0)
                slope_acc = gravity_vec - normal * gravity_vec.dot(normal)

                acc_forward = slope_acc.dot(forward_on_slope)
                acc_right = slope_acc.dot(right_on_slope)

                # 3. La gravité latérale subit la résistance des carres (seule une fraction passe)
                edge_grip = 0.1  # 0.0 = pas de glisse latérale par la pente, 1.0 = patinoire
                acc_right *= edge_grip

                # Reconstitution de l'accélération nette sur la pente
                net_acceleration = (forward_on_slope * acc_forward) + (right_on_slope * acc_right)
                self.velocity += net_acceleration * time.dt"""

                # 3. Projection de la pesanteur sur la pente
                gravity_vec = Vec3(0, -self.gravity, 0)
                slope_acc = gravity_vec - normal * gravity_vec.dot(normal)
                self.velocity += slope_acc * time.dt

                # 4. Décomposition dans la base orthogonale pure
                v_forward_mag = self.velocity.dot(forward_on_slope)
                v_right_mag = self.velocity.dot(right_on_slope)

                # 5. Amortissement pur du dérapage latéral sans altérer la vitesse avant
                v_right_mag = lerp(v_right_mag, 0.0, 4 * time.dt)

                # 6. Reconstruction exacte sans création d'énergie parasite
                self.velocity = (forward_on_slope * v_forward_mag) + (right_on_slope * v_right_mag)
                



                # 4. Friction réelle de la neige (soustraction physique amortie par time.dt)
                # Remplace le multiplicateur brut 0.99
                drag_force = 0.5 # Ajuster la résistance de la neige
                if self.velocity.length() > 0:
                    self.velocity -= self.velocity.normalized() * drag_force * time.dt
            else:
                # En l'air : gravite standard
                self.velocity.y -= self.gravity * time.dt
        else:
            # En l'air : gravite standard
            self.velocity.y -= self.gravity * time.dt

        # Application du mouvement
        player.position += self.velocity * time.dt