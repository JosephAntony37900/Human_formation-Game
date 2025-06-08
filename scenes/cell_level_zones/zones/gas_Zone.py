import pygame
import random
from entities.optimized_obstacles import ObstacleGas

class GasZone:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.spawned_zones = set()
        self.spawn_interval_y = 200
        self.gas_radius = 50
        self.spawn_zone_height = 300
        self.max_obstacles_per_zone = 10
        self.full_map_spawn = False
        self.spawn_delay = 3000
        self.full_map_spawn_delay = 6000
        self.start_time = pygame.time.get_ticks()
        self.music_start_time = pygame.time.get_ticks()
        self.music_started = False
        self.last_gas_time = pygame.time.get_ticks()
        self.gas_cooldown = 1000
    
    def spawn_gases_function(self, level, sprite_manager):
        now = pygame.time.get_ticks()
        
        if now - self.last_gas_time > self.gas_cooldown:
            if random.random() < 0.1:
                self.last_gas_time = now
                
                x = random.randint(50, self.screen_width - 50)
                y = -50
                
                gas = ObstacleGas(x, y)
                self.entity_manager.add_entity(gas, "obstacle")
                sprite_manager.gases.add(gas)
                
                # Añadir a grupos específicos del level si es necesario
                if hasattr(level, 'obstacles'):
                    level.obstacles.add(gas)
    
    def spawn_gases(self, background_y, player_x, player_y, min_allowed_y, max_allowed_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < self.spawn_delay:
            return
            
        if not self.full_map_spawn and current_time - self.start_time > self.full_map_spawn_delay:
            self.full_map_spawn = True
        
        zone_y = (player_y - 300) // self.spawn_interval_y * self.spawn_interval_y
        if zone_y in self.spawned_zones:
            return
        
        self.spawned_zones.add(zone_y)
        
        # Obtener gases actuales para verificar distancia
        current_gases = [e for e in self.entity_manager.obstacles 
                        if isinstance(e, ObstacleGas)]
        
        for _ in range(self.max_obstacles_per_zone):
            x = random.randint(50, self.screen_width - 50)
            y = random.randint(zone_y, zone_y + self.spawn_zone_height)
            
            x = max(50, min(x, self.screen_width - 50))
            y = max(min_allowed_y, min(y, max_allowed_y))
            
            # Verificar distancia con gases existentes
            too_close = any(
                ((gas.rect.centerx - x) ** 2 + (gas.rect.centery - y) ** 2) ** 0.5 < self.gas_radius
                for gas in current_gases
            )
            
            if not too_close:
                gas = ObstacleGas(x, y)
                self.entity_manager.add_entity(gas, "obstacle")
        
        # Manejar música
        if not self.music_started and current_time - self.music_start_time >= 15000:
            try:
                pygame.mixer.music.load("assets/music/Cosmicv1.mp3")
                pygame.mixer.music.play(-1)
                self.music_started = True
            except pygame.error as e:
                print(f"Error cargando música: {e}")