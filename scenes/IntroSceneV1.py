import pygame
from config.Display_settings import DisplaySettings
from entities.Player_model import Player
from inputs.keyboard import get_keys
class IntroScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(DisplaySettings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, 100)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(DisplaySettings.FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = get_keys()
        self.player.update(keys)

    def draw(self):
        self.screen.fill((0, 0, 0)) 
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               self.running = False  
