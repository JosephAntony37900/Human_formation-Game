import pygame
import random
from entities.Obstacule_gas import Obstacle

class GasZone:
    def __init__(self, screen, all_sprites):
        self.screen = screen
        self.all_sprites = all_sprites
        self.obstacles = pygame.sprite.Group()

    def spawn_gases(self, background_y, spawn_threshold=100):
        if background_y < spawn_threshold:
            return

        middle_third_start = self.screen.get_width() // 3
        middle_third_end = (self.screen.get_width() * 2) // 3
        middle_third_width = middle_third_end - middle_third_start

        if len(self.obstacles) < 7 and random.random() < 0.03:
            obstacle = Obstacle()
            obstacle.rect.x = middle_third_start + random.randint(0, middle_third_width - obstacle.rect.width)
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)

    def update_gases(self):
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.rect.y > self.screen.get_height():
                obstacle.kill()

    def check_gas_collisions(self, player):
        hits = pygame.sprite.spritecollide(player, self.obstacles, False)
        if hits:
            if player.take_damage(15.0):
                return 15.0  # daño recibido
        return 0.0
