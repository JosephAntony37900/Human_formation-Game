# entities/optimized_enemies.py
import pygame
from typing import List, Tuple, Optional
from entities.base_entity import BaseEntity


class EnemyLeucocito(BaseEntity):
    
    def __init__(self):
        import random
        screen_w = pygame.display.Info().current_w
        x = random.randint(100, screen_w - 100)
        
        super().__init__(x, -50, (80, 80), "assets/enemies/leucocito/", 3, 150)
        
        # Cache para optimizar búsqueda de objetivos
        self._target_cache = None
        self._last_target_search = 0
        self._target_search_interval = 100  # ms entre búsquedas
        
    def find_closest_target(self, targets: List) -> Optional[pygame.sprite.Sprite]:
        """Encuentra el objetivo más cercano con cache"""
        now = pygame.time.get_ticks()
        
        if (self._target_cache is None or 
            now - self._last_target_search >= self._target_search_interval):
            
            if targets:
                self._target_cache = min(
                    targets,
                    key=lambda t: (t.rect.centerx - self.rect.centerx) ** 2 + 
                                  (t.rect.centery - self.rect.centery) ** 2
                )
            self._last_target_search = now
        
        return self._target_cache
    
    def update(self, player, bots):
        targets = [player] + list(bots)
        target = self.find_closest_target(targets)
        
        if target:
            dx, dy = self.calculate_direction_to_target(target.rect.center)
            
            # Movimiento suavizado
            self.rect.x += int(self.speed * dx)
            self.rect.y += int(self.speed * dy)
            
            # Flip horizontal basado en dirección
            if len(self.frames) > 1:
                now = pygame.time.get_ticks()
                if now - self.last_update >= self.frame_rate:
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    
                    frame = self.frames[self.current_frame]
                    if dx < 0:  # Objetivo a la izquierda
                        frame = pygame.transform.flip(frame, True, False)
                    
                    self.image = frame
                    self.last_update = now
        
        # Marcar para eliminación si está muy lejos
        if self.is_off_screen(200):
            self.mark_for_deletion()

class Spittle(BaseEntity):
    """Proyectil optimizado"""
    
    def __init__(self, x: int, y: int, direction: Tuple[float, float]):
        super().__init__(x, y, (30, 30), "assets/enemies/lactobacilo/spittle", 5, 100)
        self.direction = direction
    
    def update(self, player=None, bots=None):
        self.rect.x += int(self.speed * self.direction[0])
        self.rect.y += int(self.speed * self.direction[1])
        
        self.update_animation()
        
        if self.is_off_screen():
            self.mark_for_deletion()

class EnemyLactobacilo(BaseEntity):
    def __init__(self, spittle_group):
        import random
        screen_w = pygame.display.Info().current_w
        x = random.randint(100, screen_w - 100)
        
        super().__init__(x, -60, (80, 80), "assets/enemies/lactobacilo/moving", 20, 150)
        # Cargar frames de ataque
        self.attack_frames = self.resource_manager.load_animation(
            "assets/enemies/lactobacilo/attack", (80, 80)
        )
        # Rotar frames
        self.frames = [pygame.transform.rotate(frame, 90) for frame in self.frames]
        self.attack_frames = [pygame.transform.rotate(frame, 90) for frame in self.attack_frames]
        self.image = self.frames[self.current_frame]
        
        self.spittle_group = spittle_group
        self.last_spit = pygame.time.get_ticks()
        self.spit_cooldown = 2000
        self.state = "moving"
    
    def update(self, player, bots):
        self.rect.y += self.speed
        
        # now = pygame.time.get_ticks()
        # if now - self.last_spit > self.spit_cooldown:
        #     targets = [player] + list(bots)
        #     if targets:
        #         target = min(targets, key=lambda t: 
        #                     (t.rect.centerx - self.rect.centerx) ** 2 + 
        #                     (t.rect.centery - self.rect.centery) ** 2)
        #         direction = self.calculate_direction_to_target(target.rect.center)
        #         spit = Spittle(self.rect.centerx, self.rect.centery, direction)
        #         self.spittle_group.add(spit)
        #         self.last_spit = now
        #         self.state = "attack"
        # else:
        #     self.state = "moving"
        
        # Animación
        frames = self.attack_frames if self.state == "attack" else self.frames
        if len(frames) > 1:
            now = pygame.time.get_ticks()
            if now - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]
                self.last_update = now
        
        if self.is_off_screen():
            self.mark_for_deletion()