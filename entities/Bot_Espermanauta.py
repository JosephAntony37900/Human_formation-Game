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
        self.max_health = 75
        self.health = self.max_health

    def update(self, min_x, max_x, min_y, max_y, level, enemies, obstacles, background_is_moving):
        # if current_time - self.movement_timer > self.change_direction_interval:
        #     self.direction *= -1
        #     self.movement_timer = current_time

        # self.rect.x += self.speed * self.direction

        # if self.rect.left < min_x or self.rect.right > max_x:
        #     self.direction *= -1  # Cambia dirección si choca con bordes

        self.rect.x += self.speed * self.direction

        if self.rect.left <= min_x or self.rect.right >= max_x:
            self.direction *= -1
            self.rect.x += self.speed * self.direction

        # Simula disparos aleatorios o cada cierto tiempo
#        if self.weapon_active and current_time - self.last_shot >= self.shoot_cooldown:
#            bullet = Bullet(self.rect.centerx, self.rect.top)
#            self.bullets.add(bullet)
#            level.all_sprites.add(bullet)
#            self.last_shot = current_time

        self.avoid_obstacles(obstacles)
        self.shoot_and_avoid_enemies(enemies, level)

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
        #self.weapon_active = True
        #for enemy in enemies:
        #    if abs(enemy.rect.centery - self.rect.centery) < 30:
        #        distance = enemy.rect.centerx - self.rect.centerx

        #        if abs(distance) < 300:
        #            current_time = pygame.time.get_ticks()
        #            if current_time - self.last_shot >= self.shoot_cooldown:
        #                bullet = Bullet(self.rect.centerx, self.rect.top)
        #                self.bullets.add(bullet)
        #                level.all_sprites.add(bullet)
        #                self.last_shot = current_time
        #self.weapon_active = False
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()