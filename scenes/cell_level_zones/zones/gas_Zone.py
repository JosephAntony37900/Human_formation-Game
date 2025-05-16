import pygame
import random
from entities.Obstacule_gas import Obstacle

class GasZone:
    def __init__(self, screen, all_sprites):
        self.screen = screen
        self.all_sprites = all_sprites
        self.gases = pygame.sprite.Group()
        self.spawned_zones = set()
        self.spawn_interval_y = 400
        self.gas_radius = 100
        self.spawn_zone_height = 300
        self.max_obstacles_per_zone = 5
        self.full_map_spawn = False
        self.spawn_delay = 10000
        self.full_map_spawn_delay = 20000
        self.start_time = pygame.time.get_ticks()
        self.music_start_time = pygame.time.get_ticks()
        self.music_started = False

    def spawn_gases_function(self, level):
        if random.random() < 0.2:
            gas = Obstacle(0, random.random())
            level.obstacles.add(gas)
            level.all_sprites.add(level.obstacles)

    def spawn_gases(self, background_y, player_x, player_y, min_allowed_y, max_allowed_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < self.spawn_delay:
            return
        if not self.full_map_spawn and current_time - self.start_time > self.full_map_spawn_delay:
            self.full_map_spawn = True

        zone_y = (player_y + 300) // self.spawn_interval_y * self.spawn_interval_y
        if zone_y in self.spawned_zones:
            return

        self.spawned_zones.add(zone_y)

        for _ in range(self.max_obstacles_per_zone):
            if self.full_map_spawn:
                x = random.randint(50, self.screen.get_width() - 50)
                y = random.randint(zone_y, zone_y + self.spawn_zone_height)
            else:
                x = random.randint(player_x - self.gas_radius, player_x + self.gas_radius)
                y = random.randint(zone_y, zone_y + self.spawn_zone_height)

            x = max(50, min(x, self.screen.get_width() - 50))
            y = max(min_allowed_y, min(y, max_allowed_y))

            too_close = any(
                ((gas.rect.centerx - x) ** 2 + (gas.rect.centery - y) ** 2) ** 0.5 < self.gas_radius
                for gas in self.gases
            )

            if not too_close:
                gas = Obstacle(x, y)
                self.all_sprites.add(gas)
                self.gases.add(gas)

        if not self.music_started and current_time - self.music_start_time >= 15000:
            pygame.mixer.music.load("assets/music/Cosmicv1.mp3")
            pygame.mixer.music.play(-1)
            self.music_started = True

    def update_gases(self):
        for gas in self.gases:
            gas.update()
            if gas.rect.y > self.screen.get_height() + 200:
                gas.kill()
