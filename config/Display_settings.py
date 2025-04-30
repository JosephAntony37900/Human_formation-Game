import pygame

class DisplaySettings:
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    TITLE = "Human Formation Game"
    FPS = 60
