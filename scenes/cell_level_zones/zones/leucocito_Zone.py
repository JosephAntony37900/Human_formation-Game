import random
import pygame
from entities.Enemy_leucocito import EnemyLeucocito

class LeucocitoZone:
    def __init__(self, screen, all_sprites, enemies):
        self.screen = screen
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.spawn_enabled = False
        self.start_time = pygame.time.get_ticks()
        self.background_y_threshold = 100  # Puedes ajustar esto
        self.last_enemy_time = pygame.time.get_ticks()
        self.enemy_coldown = 1000
    
    def spawn_enemy(self, level):
        now = pygame.time.get_ticks()
        if now - self.last_enemy_time > self.enemy_coldown:
            if random.random() < 0.1:
                self.last_enemy_time = now
                screen_width = self.screen.get_width()

                x = random.randint(50, screen_width - 50)
                y = -50

                enemy = EnemyLeucocito()
                level.enemies.add(enemy)
                level.all_sprites.add(enemy)

    def update(self, background_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < 3000:
            return

        if not self.spawn_enabled and background_y >= self.background_y_threshold:
            self.spawn_enabled = True

        if self.spawn_enabled:
            middle_third_start = self.screen.get_width() // 3
            middle_third_end = (self.screen.get_width() * 2) // 3
            middle_third_width = middle_third_end - middle_third_start

            if len(self.enemies) < 8 and random.random() < 0.04:
                enemy = EnemyLeucocito()
                enemy.rect.x = middle_third_start + random.randint(0, middle_third_width - enemy.rect.width)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
