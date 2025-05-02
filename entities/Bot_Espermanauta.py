import pygame
import os
from entities.Bullet import Bullet
from entities.Player_model import Player

class BotEspermanauta(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 4
        self.direction = 1
        self.movement_timer = pygame.time.get_ticks()
        self.change_direction_interval = 2000
        self.health = 25

    def update(self, min_x, max_x, min_y, max_y, level, enemies, obstacles, background_is_moving):
        screen_width = pygame.display.Info().current_w
        middle_third_start = screen_width // 5  #aqui ya funcionan los limites del player
        middle_third_end = (screen_width * 4) // 5 #,,
        current_time = pygame.time.get_ticks()

        restricted_min_x = middle_third_start
        restricted_max_x = middle_third_end - self.rect.width

        # Cambia dirección cada X segundos
        # if current_time - self.movement_timer > self.change_direction_interval:
        #     self.direction *= -1
        #     self.movement_timer = current_time

        # Mover horizontalmente en su dirección actual
        # self.rect.x += self.speed * self.direction

        # Restringe a los límites del nivel
        # if self.rect.left < min_x or self.rect.right > max_x:
        #     self.direction *= -1  # Cambia dirección si choca con bordes

        self.rect.x += self.speed * self.direction

        # Rebotar al llegar a los límites horizontales
        if self.rect.left <= min_x or self.rect.right >= max_x:
            self.direction *= -1
            self.rect.x += self.speed * self.direction

        # Simula disparos aleatorios o cada cierto tiempo
#        if self.weapon_active and current_time - self.last_shot >= self.shoot_cooldown:
#            bullet = Bullet(self.rect.centerx, self.rect.top)
#            self.bullets.add(bullet)
#            level.all_sprites.add(bullet)
#            self.last_shot = current_time

        self.avoid_obstacles(obstacles, min_x, max_x)
        self.shoot_enemies(enemies, level)

        # Actualiza animaciones, invencibilidad, etc.
        self.handle_animation_and_status()

        if not background_is_moving:
            self.rect.y -= self.speed
    
    def handle_animation_and_status(self):
        current_time = pygame.time.get_ticks()

        if self.invincible and current_time - self.invincibility_timer >= self.invincibility_duration:
            self.invincible = False

        if len(self.frames) > 1:
            if current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.current_frame], (80, 80))
                self.image.set_colorkey((0, 0, 0))
                self.last_update = current_time

    def avoid_obstacles(self, obstacles, min_x, max_x):

        anticipation_distance = 20  # distancia para prever obstáculos

        # Simula movimiento en la dirección actual
        next_rect = self.rect.copy()
        next_rect.x += (self.speed + anticipation_distance) * self.direction

        will_collide = any(next_rect.colliderect(ob.rect) for ob in obstacles)

        if will_collide:
            # Intenta mover al lado contrario (como prueba)
            test_direction = -self.direction
            test_rect = self.rect.copy()
            test_rect.x += (self.speed + anticipation_distance) * test_direction

            can_evade = not any(test_rect.colliderect(ob.rect) for ob in obstacles)

            if can_evade:
                self.direction = test_direction
                self.rect.x += self.speed * self.direction
            else:
                # Si no hay escape horizontal, intenta moverse hacia abajo (evadir vertical)
                down_rect = self.rect.copy()
                down_rect.y += self.speed

                if not any(down_rect.colliderect(ob.rect) for ob in obstacles):
                    self.rect.y += self.speed * 3
                    # Si no puede ir a ningún lado, se queda quieto
        else:
            # Si no habrá colisión, se mueve normalmente
            self.rect.x += self.speed * self.direction
    
    def shoot_enemies(self, enemies, level):
        self.weapon_active = True
        for enemy in enemies:
            if abs(enemy.rect.centery - self.rect.centery) < 30:
                distance = enemy.rect.centerx - self.rect.centerx

                if abs(distance) < 300:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_shot >= self.shoot_cooldown:
                        bullet = Bullet(self.rect.centerx, self.rect.top)
                        self.bullets.add(bullet)
                        level.all_sprites.add(bullet)
                        self.last_shot = current_time
        self.weapon_active = False