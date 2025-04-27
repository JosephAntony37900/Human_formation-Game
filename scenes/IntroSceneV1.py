import pygame
import time
import scenes
from scenes.cell_level_zones.cell_level import CellLevel
from config.Display_settings import DisplaySettings

class IntroScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Menú de Inicio")
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = pygame.image.load("assets/backgrounds/Home.png")
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 55)


        self.button_rect = pygame.Rect(50, self.screen.get_height() // 4, 400, 90)
        self.hovered = False

        self.alpha = 255 
        self.fade_out = True
        self.last_fade_time = time.time()

    def run(self):
        while self.running:
            self.events()
            self.update_fade_effect()
            self.draw()
            self.clock.tick(DisplaySettings.FPS)

    def events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    self.start_game()

    def update_fade_effect(self):
        if not self.hovered:
            if time.time() - self.last_fade_time > 0.05:
                if self.fade_out:
                    self.alpha -= 15
                    if self.alpha <= 50:
                        self.fade_out = False
                else:
                    self.alpha += 15
                    if self.alpha >= 255:
                        self.fade_out = True
                self.last_fade_time = time.time()
        else:
            self.alpha = 255

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        self.screen.blit(overlay, (0, 0))
        self.draw_text_button()
        pygame.display.flip()

    def draw_text_button(self):
        text = self.font.render("Start New Game", True, (255, 255, 255))
        text.set_alpha(self.alpha)
        text_rect = text.get_rect(midleft=(self.button_rect.x, self.button_rect.centery))
        self.screen.blit(text, text_rect)

        if self.hovered:
            pygame.draw.line(self.screen, (255, 255, 255),
                             (self.button_rect.x, self.button_rect.bottom),
                             (self.button_rect.x + 430, self.button_rect.bottom), 3)
    
    
    def start_game(self):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))
    
        for alpha in range(0, 256, 10):
            fade_surface.set_alpha(alpha)
            self.screen.blit(self.background, (0, 0))
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 40))
            self.screen.blit(overlay, (0, 0))
            self.draw_text_button()
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30) 

        self.running = False
        game = CellLevel()
        game.run()

