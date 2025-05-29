# scenes/cell_level_zones/managers/game_manager.py
import pygame
from config.Display_settings import DisplaySettings

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(DisplaySettings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_paused = True
        self.game_over = False
        
        # Tiempos
        self.start_time = pygame.time.get_ticks()
        self.time_to_change_zone = 0
        self.music_start_time = pygame.time.get_ticks()
        self.music_started = False
        
        # Límites de pantalla
        self.min_allowed_x = 40
        self.max_allowed_x = pygame.display.Info().current_w - 40
        self.min_allowed_y = 0
        self.max_allowed_y = 800
        
        # Victoria
        self.princess_spawned = False
        try:
            self.win_image = pygame.image.load("assets/backgrounds/final_escene_level1.png")
            info = pygame.display.Info()
            self.win_image = pygame.transform.scale(self.win_image, (info.current_w, info.current_h))
        except:
            print("Error cargando imagen de victoria")
            self.win_image = None
        
        self.win_font = pygame.font.Font(None, 48)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
    
    def update_game_state(self):
        if not self.game_over:
            music_current_time = pygame.time.get_ticks()
            self.time_to_change_zone = pygame.time.get_ticks() - self.start_time
            
            if not self.music_started and music_current_time - self.music_start_time >= 15000:
                pygame.mixer.music.load("assets/music/Cosmicv1.mp3")
                pygame.mixer.music.play(-1)
                self.music_started = True
    
    def win_level(self, screen):
        self.game_over = True
        pygame.mixer.music.stop()

        if self.win_image:
            screen.blit(self.win_image, (0, 0))

        victory_text = (
            "¡Victoria! Has logrado alcanzar a América y conquistar el planeta Gino-12034. "
            "Ahora, con la unión de ustedes dos, podrán terraformar el mundo, y de esto, "
            "surgirá algo nuevo..."
        )

        lines = self.wrap_text(victory_text, self.win_font, 580)
        line_height = self.win_font.get_height() + 5
        total_text_height = len(lines) * line_height

        overlay_height = total_text_height + 80
        overlay_rect = pygame.Rect(0, 0, 600, overlay_height)
        overlay_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

        overlay = pygame.Surface((overlay_rect.width, overlay_rect.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, overlay_rect.topleft)

        self.draw_wrapped_lines(
            lines=lines,
            font=self.win_font,
            color=(255, 255, 255),
            rect=overlay_rect,
            surface=screen,
            line_spacing=5
        )

        health_font = pygame.font.Font(None, 24)
        continue_text = health_font.render("Aprieta cualquier tecla para continuar", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(screen.get_width() // 2, overlay_rect.bottom - 30))
        screen.blit(continue_text, continue_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    waiting = False
                    self.running = False

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        line = ""

        for word in words:
            test_line = line + word + " "
            if font.render(test_line, True, (0, 0, 0)).get_width() > max_width:
                lines.append(line)
                line = word + " "
            else:
                line = test_line

        if line:
            lines.append(line)

        return lines

    def draw_wrapped_lines(self, lines, font, color, rect, surface, line_spacing=5):
        y = rect.top + 20
        for line in lines:
            line_surface = font.render(line.strip(), True, color)
            line_rect = line_surface.get_rect(centerx=rect.centerx)
            line_rect.top = y
            surface.blit(line_surface, line_rect)
            y += line_surface.get_height() + line_spacing