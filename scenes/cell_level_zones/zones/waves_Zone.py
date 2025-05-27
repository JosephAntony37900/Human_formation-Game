import pygame
import random
from entities.optimized_obstacles import ObstacleVelocity

class WavesZone:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.last_wave_time = pygame.time.get_ticks()
        self.waves_cooldown = 1000
        self.screen_width = pygame.display.Info().current_w
    
    def spawn_waves(self, level):
        now = pygame.time.get_ticks()
        if now - self.last_wave_time > self.waves_cooldown:
            if random.random() < 0.1:
                self.last_wave_time = now
                
                x = random.randint(50, self.screen_width - 50)
                y = -50
                
                # Selección de dirección optimizada
                directions = ["UP", "LEFT", "RIGHT", "DOWN"]
                direction = random.choice(directions)
                
                wave = ObstacleVelocity(x, y, direction)
                self.entity_manager.add_entity(wave, "obstacle")
                
                # Añadir a grupos específicos del level si es necesario
                if hasattr(level, 'boosts'):
                    level.boosts.add(wave)