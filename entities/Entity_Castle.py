import pygame
import os

class Castle (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [pygame.image.load("assets/characters/castle/castle.png").convert_alpha()]
        self.image = pygame.transform.scale(self.frames[0], (500,500))

        background_color = (0, 0, 0)  
        self.image.set_colorkey(background_color)

        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = -25
        self.speed = 3
    
    def update(self):
        self.rect.y += self.speed