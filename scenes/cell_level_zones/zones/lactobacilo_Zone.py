import pygame
import random
from entities.Enemy_lactobacilos import EnemyLactobacilo

class LactobaciloZone:
    def __init__(self, screen, all_sprites, enemies, spittle_group):
        self.screen = screen
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.spittle_group = spittle_group
        self.spawn_enabled = False
        self.start_time = pygame.time.get_ticks()
        self.background_y_threshold = 150  # Ajustable

    def update(self, background_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < 3000:
            return

        if not self.spawn_enabled and background_y >= self.background_y_threshold:
            self.spawn_enabled = True

        if self.spawn_enabled and len(self.enemies) < 6 and random.random() < 0.03:
            enemy = EnemyLactobacilo(self.spittle_group)
            middle_start = self.screen.get_width() // 3
            middle_width = self.screen.get_width() // 3
            enemy.rect.x = middle_start + random.randint(0, middle_width - enemy.rect.width)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
