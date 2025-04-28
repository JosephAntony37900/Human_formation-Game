import pygame
import random
from entities.Obstacule_gas import Obstacle

class GasZone:
    def __init__(self, screen, all_sprites):
        self.screen = screen
        self.all_sprites = all_sprites
        self.gases = pygame.sprite.Group()
        self.max_obstacles = 10
        self.min_distance_between_gases = 50  
        self.spawn_delay = 10000  
        self.start_time = pygame.time.get_ticks()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 500  
        self.full_map_spawn_delay = 20000  
        self.full_map_spawn = False

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        self.playable_area = pygame.Rect(50, 50, screen_width - 100, screen_height - 100)

    def spawn_gases(self, background_y, player_x, player_y):
        current_time = pygame.time.get_ticks()

        if current_time - self.start_time < self.spawn_delay:
            return

        if not self.full_map_spawn and current_time - self.start_time > self.full_map_spawn_delay:
            self.full_map_spawn = True
            print("¡Modo gases en toda la zona jugable activado!")

        if len(self.gases) >= self.max_obstacles:
            return

        if current_time - self.last_spawn_time < self.spawn_interval:
            return

        if self.full_map_spawn:
            x = random.randint(self.playable_area.left, self.playable_area.right)
            y = random.randint(self.playable_area.top, self.playable_area.bottom)
        else:
            x = random.randint(player_x - 150, player_x + 150)
            y = random.randint(player_y - 150, player_y + 150)

            x = max(self.playable_area.left, min(x, self.playable_area.right))
            y = max(self.playable_area.top, min(y, self.playable_area.bottom))

        too_close = False
        for gas in self.gases:
            distance = ((gas.rect.centerx - x) ** 2 + (gas.rect.centery - y) ** 2) ** 0.5
            if distance < self.min_distance_between_gases:
                too_close = True
                break

        if not too_close:
            gas = Obstacle(x, y)
            self.all_sprites.add(gas)
            self.gases.add(gas)
            self.last_spawn_time = current_time

    def update_gases(self):
        for gas in self.gases:
            gas.update()
            if gas.rect.y > self.screen.get_height():
                gas.kill()
