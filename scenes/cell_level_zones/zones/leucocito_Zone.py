import random
import pygame
from entities.optimized_enemies import EnemyLeucocito

class LeucocitoZone:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.screen_width = pygame.display.Info().current_w
        self.spawn_enabled = False
        self.start_time = pygame.time.get_ticks()
        self.background_y_threshold = 100
        self.last_enemy_time = pygame.time.get_ticks()
        self.enemy_cooldown = 1000
        self.max_enemies = 8
    
    def spawn_enemy(self, level):
        now = pygame.time.get_ticks()
        if now - self.last_enemy_time > self.enemy_cooldown:
            if random.random() < 0.1:
                self.last_enemy_time = now
                
                enemy = EnemyLeucocito()
                self.entity_manager.add_entity(enemy, "enemy")
                
                # Añadir a grupos específicos del level si es necesario
                if hasattr(level, 'enemies'):
                    level.enemies.add(enemy)
    
    def update(self, background_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < 3000:
            return
        
        if not self.spawn_enabled and background_y >= self.background_y_threshold:
            self.spawn_enabled = True
        
        if self.spawn_enabled:
            current_enemies = len([e for e in self.entity_manager.enemies 
                                 if isinstance(e, EnemyLeucocito)])
            
            if current_enemies < self.max_enemies and random.random() < 0.04:
                middle_third_start = self.screen_width // 3
                middle_third_end = (self.screen_width * 2) // 3
                middle_third_width = middle_third_end - middle_third_start
                
                enemy = EnemyLeucocito()
                enemy.rect.x = middle_third_start + random.randint(
                    0, middle_third_width - enemy.rect.width
                )
                
                self.entity_manager.add_entity(enemy, "enemy")