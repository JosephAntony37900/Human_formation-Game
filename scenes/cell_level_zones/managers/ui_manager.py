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
        
        # Game Over menu settings
        self.game_over_selected = 0
        self.game_over_options = ["REINTENTAR", "SALIR AL MENÚ"]
        self.hover_alpha = 150
        self.hover_fade_out = False
        self.hover_speed = 3
        
        # Fonts
        try:
            self.kill_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 25)
            self.game_over_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 60)
            self.health_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 24)
            self.menu_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 40)
        except:
            print("Error cargando Pixelify Sans, usando fuente por defecto")
            self.kill_font = pygame.font.Font(None, 24)
            self.game_over_font = pygame.font.Font(None, 60)
            self.health_font = pygame.font.Font(None, 24)
            self.menu_font = pygame.font.Font(None, 40)

    def update_hover_animation(self):
        """Actualiza la animación de hover para el menú de game over"""
        if self.hover_fade_out:
            self.hover_alpha -= self.hover_speed
            if self.hover_alpha <= 100:
                self.hover_fade_out = False
        else:
            self.hover_alpha += self.hover_speed
            if self.hover_alpha >= 200:
                self.hover_fade_out = True

    def handle_game_over_input(self, event):
        """Maneja la entrada del teclado para el menú de game over"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.game_over_selected = (self.game_over_selected - 1) % len(self.game_over_options)
                return "navigation"
            elif event.key == pygame.K_DOWN:
                self.game_over_selected = (self.game_over_selected + 1) % len(self.game_over_options)
                return "navigation"
            elif event.key == pygame.K_RETURN:
                if self.game_over_selected == 0:
                    return "restart"
                elif self.game_over_selected == 1:
                    return "main_menu"
        return None

    def draw_health_bar(self, current_health, max_health):
        # Barra de fondo
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height))
        
        # Barra de vida
        health_percentage = max(0, current_health / max_health)
        current_health_width = self.health_bar_width * health_percentage
        
        # Color de la barra según el porcentaje de vida
        if health_percentage > 0.6:
            health_color = (0, 255, 0)  # Verde
        elif health_percentage > 0.3:
            health_color = (255, 255, 0)  # Amarillo
        else:
            health_color = (255, 0, 0)  # Rojo
            
        pygame.draw.rect(self.screen, health_color,
                         (self.health_bar_x, self.health_bar_y, current_health_width, self.health_bar_height))
        
        # Borde de la barra
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height), 2)
        
        # Texto de vida
        health_text = self.health_font.render(f"Vida: {max(0, int(current_health))}%", True, (255, 255, 255))
        self.screen.blit(health_text, (self.health_bar_x - health_text.get_width() - 10, self.health_bar_y))

    def draw_game_over(self):
        """Dibuja la pantalla de game over con menú de opciones"""
        # Overlay semi-transparente
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Título "Game Over"
        game_over_text = self.game_over_font.render("¡JUEGO TERMINADO!", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
        
        # Sombra del título
        shadow_text = self.game_over_font.render("¡JUEGO TERMINADO!", True, (100, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(game_over_rect.centerx + 3, game_over_rect.centery + 3))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(game_over_text, game_over_rect)
        
        # Menú de opciones
        self.draw_game_over_menu()

    def draw_game_over_menu(self):
        """Dibuja el menú de opciones del game over"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Configuración del menú
        menu_width = 400
        menu_height = 200
        menu_x = (screen_width - menu_width) // 2
        menu_y = (screen_height - menu_height) // 2 + 50
        
        # Fondo del menú
        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_surface.fill((30, 30, 30, 200))
        
        # Borde del menú
        pygame.draw.rect(menu_surface, (255, 100, 100), (0, 0, menu_width, menu_height), 3, border_radius=15)
        
        # Opciones del menú
        option_height = 60
        option_spacing = 20
        start_y = 30
        
        for i, option in enumerate(self.game_over_options):
            option_y = start_y + i * (option_height + option_spacing)
            option_rect = pygame.Rect(20, option_y, menu_width - 40, option_height)
            
            # Color de fondo de la opción
            if i == self.game_over_selected:
                # Opción seleccionada con animación
                alpha = min(255, self.hover_alpha)
                selected_surface = pygame.Surface((option_rect.width, option_rect.height), pygame.SRCALPHA)
                selected_surface.fill((255, 100, 100, alpha // 2))
                menu_surface.blit(selected_surface, option_rect.topleft)
                
                # Borde de la opción seleccionada
                pygame.draw.rect(menu_surface, (255, 255, 255), option_rect, 2, border_radius=10)
            else:
                # Opción no seleccionada
                pygame.draw.rect(menu_surface, (80, 80, 80, 100), option_rect, border_radius=10)
            
            # Texto de la opción
            text_color = (255, 255, 255) if i == self.game_over_selected else (200, 200, 200)
            option_text = self.menu_font.render(option, True, text_color)
            option_text_rect = option_text.get_rect(center=option_rect.center)
            menu_surface.blit(option_text, option_text_rect)
            
            # Flechas indicadoras para la opción seleccionada
            if i == self.game_over_selected:
                arrow_left = self.menu_font.render("<", True, (255, 255, 255))
                arrow_right = self.menu_font.render(">", True, (255, 255, 255))
                
                arrow_left_rect = arrow_left.get_rect(midright=(option_rect.left - 10, option_rect.centery))
                arrow_right_rect = arrow_right.get_rect(midleft=(option_rect.right + 10, option_rect.centery))
                
                menu_surface.blit(arrow_left, arrow_left_rect)
                menu_surface.blit(arrow_right, arrow_right_rect)
        
        # Instrucciones
        instruction_text = "Usa ↑/↓ para navegar, ENTER para seleccionar"
        instruction_font = pygame.font.Font(None, 24)
        instruction_surface = instruction_font.render(instruction_text, True, (180, 180, 180))
        instruction_rect = instruction_surface.get_rect(center=(menu_width // 2, menu_height - 20))
        menu_surface.blit(instruction_surface, instruction_rect)
        
        # Dibujar el menú en la pantalla
        self.screen.blit(menu_surface, (menu_x, menu_y))

    def draw_pause_overlay(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))