import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/obstacles/Gas.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(100, pygame.display.Info().current_w - 100)
        self.rect.y = random.randint(100, pygame.display.Info().current_h - 100)

    def update(self):
        pass
