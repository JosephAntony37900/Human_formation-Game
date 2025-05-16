import pygame
import random
from entities.Obstacule_velocity import ObstaculeVelocity

class WavesZone:
    def __init__(self, screen, all_sprites):
        self.screen = screen
        self.all_sprites = all_sprites
        self.last_wave_time = pygame.time.get_ticks()
        self.waves_coldown = 1000
    
    def spawn_waves(self, level):
        now = pygame.time.get_ticks()
        if now - self.last_wave_time > self.waves_coldown:
            if random.random() < 0.1:
                self.last_wave_time = now
                screen_width = self.screen.get_width()

                x = random.randint(50, screen_width - 50)
                y = -50

                direction = "ANY"
                select_direction = random.randint(1,4)
                if select_direction == 1:
                    direction = "UP"
                elif select_direction == 2:
                    direction = "LEFT"
                elif select_direction == 3:
                    direction = "RIGHT"
                elif select_direction == 4:
                    direction = "DOWN"
                else:
                    direction = "UP"
                wave = ObstaculeVelocity(x, y, direction)
                level.boosts.add(wave)
                level.all_sprites.add(wave)