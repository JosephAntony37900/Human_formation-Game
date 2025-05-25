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
        self.direction_y = 1
        self.movement_timer = pygame.time.get_ticks()
        self.change_direction_interval = 2000
        self.max_health = 1000000
        self.health = self.max_health
        self.random_explore_dir = pgmath.Vector2(0, 0)
        self.last_random_time = pygame.time.get_ticks()
        self.random_direction_duration = 1500
        self.slowed = False
        self.slow_timer = 0
        self.slow_duration = 2000  # milisegundos
        self.original_speed = self.speed

    def update(self, min_x, max_x, min_y, max_y, level, enemies, obstacles, background_is_moving):
       
        self.detect_and_evade(list(obstacles) + list(enemies), background_is_moving, min_x, max_x)

        self.handle_animation_and_status()

        current_time = pygame.time.get_ticks()
        if self.slowed and current_time - self.slow_timer >= self.slow_duration:
            self.slowed = False
            self.speed = self.original_speed
            level.background_speed = level.original_background_speed


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
            if self.rect.colliderect(obj.rect.inflate(100, 100)):
                diff = pgmath.Vector2(self.rect.center) - pgmath.Vector2(obj.rect.center)
                distance = diff.length()
                if distance > 0:
                    avoidance_force += diff.normalize() / distance

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
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
    
    def slow_down(self, level, background_is_moving):
        if not self.slowed:
            self.rect.y -= self.speed
            level.background_speed = 1
            self.slowed = True
            self.slow_timer = pygame.time.get_ticks()