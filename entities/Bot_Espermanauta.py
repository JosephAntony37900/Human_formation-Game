#entities/Bot_Espermanauta.py
import pygame
import pygame.math as pgmath
from entities.Player_model import Player
import random

class BotEspermanauta(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.frames[self.current_frame], (100, 100))
        self.speed = 4
        self.direction = 1
        self.frozen_by_boost = False

        self.direction_y = 1
        self.movement_timer = pygame.time.get_ticks()
        self.change_direction_interval = 2000
        self.max_health = 150000
        self.health = self.max_health
        self.random_explore_dir = pgmath.Vector2(0, 0)
        self.last_random_time = pygame.time.get_ticks()
        self.random_direction_duration = 1500
        self.slowed = False
        self.slow_timer = 0
        self.slow_duration = 2000  # milisegundos
        self.original_speed = self.speed

    def update(self, min_x, max_x, min_y, max_y, level, enemies, obstacles, background_is_moving, princesses):
        # Detectar y aplicar efectos de obstáculos
        self.handle_obstacle_collisions(obstacles, level)
        
        # Detectar colisiones con enemigos y recibir daño
        self.handle_enemy_collisions(enemies)
        
        self.detect_and_evade(list(obstacles) + list(enemies), background_is_moving, min_x, max_x)

        if len(princesses) > 0:
            closets_target = min(
                princesses,
                key = lambda t: (t.rect.centerx - self.rect.centerx) ** 2 + (t.rect.centery - self.rect.centery) ** 2
            )
        
            dx = closets_target.rect.centerx - self.rect.centerx
            dy = closets_target.rect.centery - self.rect.centery

            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)

            self.rect.x += int((self.speed * dx / distance) * 0.75)
            self.rect.y += int((self.speed * dy / distance) * 0.75)

        self.handle_animation_and_status()

        current_time = pygame.time.get_ticks()
        if self.slowed and current_time - self.slow_timer >= self.slow_duration:
            self.slowed = False
            self.speed = self.original_speed
            
        if self.frozen_by_boost:
            self.handle_animation_and_status()
            return


    def handle_enemy_collisions(self, enemies):
        """Detecta colisiones con enemigos y aplica daño"""
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if not self.invincible:  # Solo recibe daño si no es invencible
                    # Diferentes tipos de enemigos causan diferente daño
                    damage = 25  # Daño base
                    if hasattr(enemy, '__class__'):
                        if enemy.__class__.__name__ == 'EnemyLeucocito':
                            damage = 30
                        elif enemy.__class__.__name__ == 'EnemyLactobacilo':
                            damage = 35
                        elif enemy.__class__.__name__ == 'Spittle':
                            damage = 15
                    
                    self.take_damage(damage)
                    
                    # Aplicar un pequeño empujón para separar del enemigo
                    push_force = 20
                    dx = self.rect.centerx - enemy.rect.centerx
                    dy = self.rect.centery - enemy.rect.centery
                    distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                    
                    self.rect.x += int((push_force * dx / distance))
                    self.rect.y += int((push_force * dy / distance))

    def handle_obstacle_collisions(self, obstacles, level):
        """Detecta colisiones con obstáculos y aplica sus efectos igual que al jugador"""
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # Efecto de obstáculo de velocidad
                if hasattr(obstacle, 'apply_impulse'):
                    self.rect = obstacle.apply_impulse(self.rect)
                elif hasattr(obstacle, 'impulse'):
                    self.rect = obstacle.impulse(self.rect)
                
                elif obstacle.__class__.__name__ == 'ObstacleMoco':
                    self.slow_down(level, False)
                    self.rect.y += 12 
                    
                    print(f"Bot {self} empujado por ObstacleMoco")

                
                # Efecto de gas (daño)
                elif obstacle.__class__.__name__ == 'ObstacleGas':
                    self.take_damage(20)  # Mismo daño que recibe el jugador

    def handle_animation_and_status(self):
        current_time = pygame.time.get_ticks()

        if self.invincible and current_time - self.invincibility_timer >= self.invincibility_duration:
            self.invincible = False

        if len(self.frames) > 1:
            if current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.current_frame], (100, 100))
                self.image.set_colorkey((0, 0, 0))
                self.last_update = current_time

    def detect_and_evade(self, objects, background_is_moving, min_x, max_x):
        avoidance_force = pgmath.Vector2(0, 0)
        border_avoidance = pgmath.Vector2(0, 0)
        margin = 50

        if self.rect.left < min_x + margin:
            border_avoidance.x += 3
        if self.rect.right > max_x - margin:
            border_avoidance.x -= 3

        for obj in objects:
            # Aumentar la distancia de detección para enemigos específicamente
            detection_inflate = 120
            
            # Mayor distancia de evasión para enemigos
            if hasattr(obj, '__class__') and obj.__class__.__name__ in ['EnemyLeucocito', 'EnemyLactobacilo', 'Spittle']:
                detection_inflate = 150  # Mayor distancia para enemigos
            
            if self.rect.colliderect(obj.rect.inflate(detection_inflate, detection_inflate)):
                diff = pgmath.Vector2(self.rect.center) - pgmath.Vector2(obj.rect.center)
                distance = diff.length()
                if distance > 0:
                    # Mayor fuerza de evasión para enemigos
                    force_multiplier = 2.0 if hasattr(obj, '__class__') and obj.__class__.__name__ in ['EnemyLeucocito', 'EnemyLactobacilo', 'Spittle'] else 1.0
                    avoidance_force += (diff.normalize() / distance) * force_multiplier

        total_force = avoidance_force + border_avoidance

        if total_force.length() > 0:
            total_force = total_force.normalize() * self.speed
            new_x = self.rect.x + total_force.x

            if min_x <= new_x <= max_x - self.rect.width:
                self.rect.x = new_x
            else:
                total_force.x *= -1
                new_x = self.rect.x + total_force.x
                if min_x <= new_x <= max_x - self.rect.width:
                    self.rect.x = new_x
                else:
                    self.rect.y += self.speed * 2

            self.rect.y += total_force.y

            above_rect = self.rect.copy()
            above_rect.y -= self.speed * 2
            if any(above_rect.colliderect(obj.rect) for obj in objects):
                self.rect.y += self.speed * 2
            else:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_random_time > self.random_direction_duration:
                    rand_x = random.uniform(-1, 1)
                    rand_y = random.choice([-1, 1])
                    self.random_explore_dir = pgmath.Vector2(rand_x, rand_y).normalize()
                    self.last_random_time = current_time

                self.rect.x += self.random_explore_dir.x * self.speed
                self.rect.y += self.random_explore_dir.y * self.speed

        else:
            if not background_is_moving:
                if self.slowed:
                    self.rect.y += self.speed
                else:
                    self.rect.y -= self.speed

        if self.rect.left < min_x:
            self.rect.left = min_x
        if self.rect.right > max_x:
            self.rect.right = max_x

    def avoid_obstacles(self, obstacles):
        anticipation_distance = 25

        next_rect = self.rect.copy()
        next_rect.x += (self.speed + anticipation_distance) * self.direction

        will_collide = any(next_rect.colliderect(ob.rect) for ob in obstacles)

        if will_collide:
            test_direction = -self.direction
            test_rect = self.rect.copy()
            test_rect.x += (self.speed + anticipation_distance) * test_direction

            can_evade = not any(test_rect.colliderect(ob.rect) for ob in obstacles)

            if can_evade:
                self.direction = test_direction
                self.rect.x += self.speed * self.direction
            else:
                down_rect = self.rect.copy()
                down_rect.y += self.speed * 10

                if not any(down_rect.colliderect(ob.rect) for ob in obstacles):
                    self.rect.y += self.speed * 10
        else:
            self.rect.x += self.speed * self.direction
    
    def shoot_and_avoid_enemies(self, enemies, level):
        anticipation_distance = 25

        next_rect = self.rect.copy()
        next_rect.x += (self.speed + anticipation_distance) * self.direction

        will_collide = any(next_rect.colliderect(ob.rect) for ob in enemies)

        if will_collide:
            test_direction = -self.direction
            test_rect = self.rect.copy()
            test_rect.x += (self.speed + anticipation_distance) * test_direction
            can_evade = not any(test_rect.colliderect(ob.rect) for ob in enemies)
            if can_evade:
                self.direction = test_direction
                self.rect.x += self.speed * self.direction
            else:
                down_rect = self.rect.copy()
                down_rect.y += self.speed * 10
                if not any(down_rect.colliderect(ob.rect) for ob in enemies):
                    self.rect.y += self.speed * 10
        else:
            self.rect.x += self.speed * self.direction
            
    def freeze_due_to_player_boost(self):
        self.frozen_by_boost = True
    def unfreeze(self):
        self.frozen_by_boost = False  #Metodos para que no se muevan los bots cuando se mueva el player en rampa
    
    def take_damage(self, damage):
        if not self.invincible:
            self.health -= damage
            # Activar invencibilidad temporal después de recibir daño
            self.invincible = True
            self.invincibility_timer = pygame.time.get_ticks()
            
            if self.health <= 0:
                self.kill()
    
    def slow_down(self, level, background_is_moving):
        if not self.slowed: 
           self.w_blocked = True
           self.block_timer = pygame.time.get_ticks()
           self.rect.y += 7

