# entities/optimized_obstacles.py
import pygame
from entities.base_entity import BaseEntity

class ObstacleVelocity(BaseEntity):
    """Obstáculo de velocidad optimizado"""
    
    DIRECTION_ROTATIONS = {
        "UP": 0,
        "RIGHT": -90,
        "DOWN": 180,
        "LEFT": 90
    }
    
    def __init__(self, x: int, y: int, direction: str, background_manager=None):
        super().__init__(x, y, (200, 200), "assets/obstacles/velocity/", 5, 150)
        
        self.direction = direction
        self.boost = 12
        self.background_manager = background_manager 
        # Rotar imagen según dirección
        if direction in self.DIRECTION_ROTATIONS:
            rotation = self.DIRECTION_ROTATIONS[direction]
            self.frames = [pygame.transform.rotate(frame, rotation) for frame in self.frames]
            self.image = self.frames[self.current_frame]

    
    def update(self):
        self.rect.y += self.speed
        self.update_animation()
        # Marcar para eliminación si está fuera de pantalla
        if self.is_off_screen():
            self.mark_for_deletion()
    
    def apply_impulse(self, target_rect: pygame.Rect) -> pygame.Rect:
        """Aplica impulso al objetivo según la dirección"""
        impulse_map = {
            "UP": (0, -self.boost),
            "DOWN": (0, self.boost),
            "LEFT": (-self.boost, 0),
            "RIGHT": (self.boost, 0)
        }
        
        if self.direction in impulse_map:
            dx, dy = impulse_map[self.direction]
            target_rect.x += dx
            target_rect.y += dy

        
        return target_rect
    
    def player_impulse(self):
        if self.direction == "UP" and self.background_manager:
           self.background_manager.establecer_velocidad(13)

    # FIXED: Mantener compatibilidad con el método antiguo impulse
    def impulse(self, target_rect: pygame.Rect) -> pygame.Rect:
        """Método de compatibilidad - llama a apply_impulse"""
        return self.apply_impulse(target_rect)

class ObstacleGas(BaseEntity):
    """Obstáculo de gas optimizado"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, (80, 80), "assets/obstacles/gas/", 5, 150)
    
    def update(self):
        self.rect.y += self.speed
        self.update_animation()
        if self.is_off_screen():
            self.mark_for_deletion()

class ObstacleMoco(BaseEntity):
    """Obstáculo de moco optimizado"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, (65, 65), "assets/obstacles/moco/", 7, 150)
    
    def update(self):
        self.rect.y += self.speed
        self.update_animation()
        if self.is_off_screen():
            self.mark_for_deletion()
            
    def apply_effect(self, player):
        player.w_blocked = True
        player.block_timer = pygame.time.get_ticks()
        player.rect.y += 6

            

