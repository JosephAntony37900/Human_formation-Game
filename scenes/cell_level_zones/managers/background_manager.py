# scenes/cell_level_zones/managers/background_manager.py
import pygame

class BackgroundManager:
    def __init__(self, screen):
        self.screen = screen
        self.background_y = 0
        self.background_speed = 2
        self.original_background_speed = self.background_speed
        
        # Cargar imagen de fondo
        try:
            self.background = pygame.image.load("assets/backgrounds/background_1.png")
            info = pygame.display.Info()
            self.background = pygame.transform.scale(self.background, (info.current_w, info.current_h))
        except pygame.error as e:
            print(f"Error al cargar background image: {e}")
            self.background = None
    
    def update_background(self):
        self.background_y += self.background_speed
    
    def draw_background(self):
        if self.background:
            bg_height = self.background.get_height()
            offset = self.background_y % bg_height
            self.screen.blit(self.background, (0, offset - bg_height))
            self.screen.blit(self.background, (0, offset))
        else:
            self.screen.fill((0, 0, 0))