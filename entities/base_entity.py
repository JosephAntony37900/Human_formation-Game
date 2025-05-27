# entities/base_entity.py
import pygame
import os
import math
from typing import List, Tuple, Optional

class ResourceManager:
    """Gestor centralizado de recursos para evitar cargas duplicadas"""
    _instance = None
    _loaded_animations = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_animation(self, path: str, size: Tuple[int, int]) -> List[pygame.Surface]:
        """Carga y cachea animaciones para evitar cargas repetidas"""
        cache_key = f"{path}_{size[0]}x{size[1]}"
        
        if cache_key not in self._loaded_animations:
            frames = []
            try:
                for filename in sorted(os.listdir(path)):
                    if filename.endswith(('.png', '.jpg')):
                        img_path = os.path.join(path, filename)
                        frame = pygame.image.load(img_path).convert_alpha()
                        frame = pygame.transform.scale(frame, size)
                        frames.append(frame)
                
                if not frames:
                    # Crear frame por defecto si no se encuentra ninguno
                    default_frame = pygame.Surface(size, pygame.SRCALPHA)
                    default_frame.fill((255, 0, 255))  # Magenta para debug
                    frames.append(default_frame)
                    
            except Exception as e:
                print(f"Error cargando animación de {path}: {e}")
                default_frame = pygame.Surface(size, pygame.SRCALPHA)
                default_frame.fill((255, 0, 255))
                frames = [default_frame]
            
            self._loaded_animations[cache_key] = frames
        
        return self._loaded_animations[cache_key]

class BaseEntity(pygame.sprite.Sprite):
    """Clase base optimizada para todas las entidades del juego"""
    
    def __init__(self, x: int, y: int, size: Tuple[int, int], animation_path: str, 
                 speed: int = 5, frame_rate: int = 150):
        super().__init__()
        
        self.resource_manager = ResourceManager()
        self.frames = self.resource_manager.load_animation(animation_path, size)
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = speed
        self.frame_rate = frame_rate
        self.last_update = pygame.time.get_ticks()
        
        # Para eliminación diferida
        self.marked_for_deletion = False
        self.deletion_time = 0
        self.deletion_delay = 6000  # 6 segundos
        
        # Cache para cálculos costosos
        self._screen_bounds = None
        self._last_bounds_check = 0
        
    def update_animation(self):
        """Actualiza la animación solo si es necesario"""
        if len(self.frames) <= 1:
            return
            
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now
    
    def get_screen_bounds(self) -> Tuple[int, int]:
        """Cache de los límites de pantalla para evitar llamadas repetidas"""
        now = pygame.time.get_ticks()
        if self._screen_bounds is None or now - self._last_bounds_check > 1000:
            display_info = pygame.display.Info()
            self._screen_bounds = (display_info.current_w, display_info.current_h)
            self._last_bounds_check = now
        return self._screen_bounds
    
    def is_off_screen(self, margin: int = 100) -> bool:
        """Verifica si la entidad está fuera de pantalla con margen"""
        screen_w, screen_h = self.get_screen_bounds()
        return (self.rect.right < -margin or self.rect.left > screen_w + margin or
                self.rect.bottom < -margin or self.rect.top > screen_h + margin)
    
    def mark_for_deletion(self):
        """Marca la entidad para eliminación diferida"""
        if not self.marked_for_deletion:
            self.marked_for_deletion = True
            self.deletion_time = pygame.time.get_ticks()
    
    def should_be_deleted(self) -> bool:
        """Verifica si la entidad debe ser eliminada"""
        if not self.marked_for_deletion:
            return False
        return pygame.time.get_ticks() - self.deletion_time >= self.deletion_delay
    
    def calculate_direction_to_target(self, target_pos: Tuple[int, int]) -> Tuple[float, float]:
        """Calcula dirección normalizada hacia un objetivo"""
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        distance = max(1, math.sqrt(dx * dx + dy * dy))
        return dx / distance, dy / distance