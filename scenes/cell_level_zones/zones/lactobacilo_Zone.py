# scenes/cell_level_zones/zones/lactobacilo_Zone.py
import pygame
import random
from entities.optimized_enemies import EnemyLactobacilo

class LactobaciloZone:
    def __init__(self, entity_manager, spittle_group):
        self.entity_manager = entity_manager
        self.spittle_group = spittle_group
        self.screen_width = pygame.display.Info().current_w
        self.spawn_enabled = False
        self.start_time = pygame.time.get_ticks()
        self.background_y_threshold = 150
        self.last_enemy_time = pygame.time.get_ticks()
        self.enemy_cooldown = 1000
        self.max_enemies = 6
    
    def spawn_enemy(self, level, sprite_manager):
        now = pygame.time.get_ticks()
        if now - self.last_enemy_time > self.enemy_cooldown:
            if random.random() < 0.3:
                self.last_enemy_time = now
                
                enemy = EnemyLactobacilo(self.spittle_group)
                self.entity_manager.add_entity(enemy, "enemy")
                sprite_manager.enemies.add(enemy)
                
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
                                 if isinstance(e, EnemyLactobacilo)])
            
            if current_enemies < self.max_enemies and random.random() < 0.03:
                middle_start = self.screen_width // 3
                middle_width = self.screen_width // 3
                
                enemy = EnemyLactobacilo(self.spittle_group)
                enemy.rect.x = middle_start + random.randint(
                    0, middle_width - enemy.rect.width
                )
                
                self.entity_manager.add_entity(enemy, "enemy")