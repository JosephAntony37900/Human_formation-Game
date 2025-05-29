# scenes/cell_level_zones/managers/ui_manager.py
import pygame

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        
        # Health bar settings
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.health_bar_x = screen.get_width() - self.health_bar_width - 10
        self.health_bar_y = 10
        
        # Fonts
        try:
            self.kill_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 25)
            self.game_over_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 60)
            self.health_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 24)
        except:
            print("Error cargando Pixelify Sans, usando fuente por defecto")
            self.kill_font = pygame.font.Font(None, 24)
            self.game_over_font = pygame.font.Font(None, 60)
            self.health_font = pygame.font.Font(None, 24)
    
    def draw_health_bar(self, current_health, max_health):
        # Barra de fondo
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height))
        
        # Barra de vida
        health_percentage = current_health / max_health
        current_health_width = self.health_bar_width * health_percentage
        pygame.draw.rect(self.screen, (255, 0, 0), 
                        (self.health_bar_x, self.health_bar_y, current_health_width, self.health_bar_height))
        
        # Texto de vida
        health_text = self.health_font.render(f"Vida: {int(current_health)}%", True, (255, 255, 255))
        self.screen.blit(health_text, (self.health_bar_x - health_text.get_width() - 10, self.health_bar_y))
    
    def draw_game_over(self):
        game_over_text = self.game_over_font.render("¡Juego Terminado!", True, (255, 0, 0))
        self.screen.blit(game_over_text, 
                        (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 
                         self.screen.get_height() // 2))
    
    def draw_pause_overlay(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))