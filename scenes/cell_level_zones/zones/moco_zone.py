import pygame
import random
from entities.Obstacle_moco import Moco

class MocoZone:
    def __init__(self, screen, all_sprites):
        self.screen = screen
        self.all_sprites = all_sprites
        self.mocos = pygame.sprite.Group()
        self.last_generation_time = pygame.time.get_ticks()
        self.spawn_delay = 400 

    def spawn_mocos(self, background_y, player_x, player_y, min_allowed_y, max_allowed_y):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_generation_time

        if elapsed_time < self.spawn_delay:
            return

        self.last_generation_time = current_time
        x = random.randint(250, self.screen.get_width() - 250)
        y = player_y - random.randint(self.screen.get_height(), self.screen.get_height() + 300)
        moco = Moco(x, y)
        self.all_sprites.add(moco)
        self.mocos.add(moco)

    def update_mocos(self, player):
        for moco in self.mocos:
            moco.update()
            self.check_collision_with_player(moco, player)
            if moco.rect.top > self.screen.get_height() + 100:
                moco.kill()

    def check_collision_with_player(self, moco, player):
        if moco.rect.colliderect(player.rect):
            player.slow_down(self)
