import pygame
import random
from entities.optimized_obstacles import ObstacleMoco

class MocoZone:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.last_generation_time = pygame.time.get_ticks()
        self.spawn_delay = 400
    
    def spawn_mocos(self, background_y, player_x, player_y, min_allowed_y, max_allowed_y):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_generation_time
        
        if elapsed_time < self.spawn_delay:
            return
        
        self.last_generation_time = current_time
        x = random.randint(250, self.screen_width - 250)
        y = player_y - random.randint(self.screen_height, self.screen_height + 300)
        
        moco = ObstacleMoco(x, y)
        self.entity_manager.add_entity(moco, "obstacle")
    
    def check_collision_with_player(self, player):
        """Verifica colisiones con el jugador usando el entity manager"""
        obstacles = self.entity_manager.obstacles
        for moco in obstacles:
            if isinstance(moco, ObstacleMoco) and moco.rect.colliderect(player.rect):
                player.slow_down(self)
    
    def check_collision_with_bots(self, bots, background_is_moving):
        """Verifica colisiones con bots"""
        obstacles = self.entity_manager.obstacles
        for moco in obstacles:
            if isinstance(moco, ObstacleMoco):
                for bot in bots:
                    if moco.rect.colliderect(bot.rect):
                        bot.slow_down(self, background_is_moving)