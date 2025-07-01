import pygame
import os

class Castle (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [pygame.image.load("assets/characters/castle/castle.png").convert_alpha()]
        self.image = pygame.transform.scale(self.frames[0], (1300,1300))

        background_color = (0, 0, 0)  
        self.image.set_colorkey(background_color)

        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = -1560
        self.speed = 3
    
    def update(self):
        self.rect.y += self.speed