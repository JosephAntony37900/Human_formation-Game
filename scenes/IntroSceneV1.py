import pygame
import time
import os
import scenes
from scenes.cell_level_zones.cell_level import CellLevel
from config.Display_settings import DisplaySettings

class IntroScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Human Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.animation_path = "assets/backgrounds/home"
        self.background_frames = self.load_animation_frames(self.animation_path, "menu_frame", total_frames=6)
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_rate = 15 

        self.arcade_font = pygame.font.Font("assets/Fonts/ka1.ttf", 120)
        self.font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 55)
        self.options = ["Start New Game", "Configuration", "Salir del Juego"]
        self.selected = 0
        self.state = 'menu'
        self.config_options = ["Sound: Yes", "Sound: No"]
        self.config_selected = 0
        self.sound_enabled = True
        self.hover_alpha = 50
        self.hover_fade_out = False
        self.hover_speed = 5

    def load_animation_frames(self, path, base_filename, total_frames):
        frames = []
        for i in range(total_frames):
            filename = f"{base_filename}({i}).png"
            full_path = os.path.join(path, filename)
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.scale(image, self.screen.get_size())
            frames.append(image)
        return frames

    def run(self):
        while self.running:
            self.handle_events()
            self.update_hover_animation()
            self.draw()
            self.clock.tick(DisplaySettings.FPS)

        pygame.quit()
        exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'config':
                        self.state = 'menu'
                    else:
                        self.running = False
                elif event.key == pygame.K_UP:
                    if self.state == 'menu':
                        self.selected = (self.selected - 1) % len(self.options)
                    else:
                        self.config_selected = (self.config_selected - 1) % len(self.config_options)
                elif event.key == pygame.K_DOWN:
                    if self.state == 'menu':
                        self.selected = (self.selected + 1) % len(self.options)
                    else:
                        self.config_selected = (self.config_selected + 1) % len(self.config_options)
                elif event.key == pygame.K_RETURN:
                    if self.state == 'menu':
                        if self.selected == 0:
                            self.start_game()
                        elif self.selected == 1:
                            self.state = 'config'
                        elif self.selected == 2:
                            self.running = False
                    else:
                        self.sound_enabled = (self.config_selected == 0)
                        self.state = 'menu'

    def update_hover_animation(self):
        if self.hover_fade_out:
            self.hover_alpha -= self.hover_speed
            if self.hover_alpha <= 80:
                self.hover_fade_out = False
        else:
            self.hover_alpha += self.hover_speed
            if self.hover_alpha >= 200:
                self.hover_fade_out = True

    def draw(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.background_frames)
            self.frame_counter = 0

        self.screen.blit(self.background_frames[self.current_frame], (0, 0))

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        self.screen.blit(overlay, (0, 0))

        if self.state == 'menu':
            self.draw_menu()
        else:
            self.draw_config()

        pygame.display.flip()

    def draw_title(self):
        w, h = self.screen.get_size()
        text = "Human Game"
        border_surf = self.arcade_font.render(text, True, (255, 255, 255))
        border_pos = border_surf.get_rect(center=(w // 2, h // 3))
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
            self.screen.blit(border_surf, (border_pos.x + dx, border_pos.y + dy))
        fill_surf = self.arcade_font.render(text, True, (49, 15, 129))
        self.screen.blit(fill_surf, border_pos)

    def draw_menu(self):
        w, h = self.screen.get_size()
        self.draw_title()
        padding_x, padding_y = 20, 20
        max_w = max(self.font.size(opt)[0] for opt in self.options) + padding_x * 2
        max_h = self.font.get_height() + padding_y * 2
        total_h = len(self.options) * (max_h + 20) - 20
        start_y = h // 2 - total_h // 2 + 150

        for idx, text in enumerate(self.options):
            x = w // 2 - max_w // 2
            y = start_y + idx * (max_h + 20)
            rect = pygame.Rect(x, y, max_w, max_h)
            pygame.draw.rect(self.screen, (59, 19, 165), rect, border_radius=40)
            if idx == self.selected and self.hover_alpha > 125:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, width=2, border_radius=40)
            label = self.font.render(text, True, (255, 255, 255))
            label_pos = label.get_rect(center=rect.center)
            self.screen.blit(label, label_pos)

    def draw_config(self):
        w, h = self.screen.get_size()
        self.draw_title()
        padding_x, padding_y = 20, 20
        max_w = max(self.font.size(opt)[0] for opt in self.config_options) + padding_x * 2
        max_h = self.font.get_height() + padding_y * 2
        total_h = len(self.config_options) * (max_h + 20) - 20
        start_y = h // 2 - total_h // 2 + 90

        for idx, text in enumerate(self.config_options):
            x = w // 2 - max_w // 2
            y = start_y + idx * (max_h + 20)
            rect = pygame.Rect(x, y, max_w, max_h)
            pygame.draw.rect(self.screen, (59, 19, 165), rect, border_radius=40)
            if idx == self.config_selected and self.hover_alpha > 125:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 rect, width=2, border_radius=40)
            label = self.font.render(text, True, (255, 255, 255))
            label_pos = label.get_rect(center=rect.center)
            self.screen.blit(label, label_pos)

    def start_game(self):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 256, 10):
            fade_surface.set_alpha(alpha)
            self.screen.blit(self.background_frames[self.current_frame], (0, 0))
            self.draw_menu()
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)
        self.running = False
        game = CellLevel()
        game.run()
