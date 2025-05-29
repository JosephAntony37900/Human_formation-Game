# scenes/cell_level_zones/cell_level.py
import pygame
from config.Display_settings import DisplaySettings
from inputs.keyboard import get_keys

# Importar managers
from .managers.game_manager import GameManager
from .managers.sprite_manager import SpriteManager
from .managers.ui_manager import UIManager
from .managers.collision_manager import CollisionManager
from .managers.zone_manager import ZoneManager
from .managers.background_manager import BackgroundManager
from .managers.narrator_manager import NarratorManager

class CellLevel:
    def __init__(self):
        # Inicializar managers
        self.game_manager = GameManager()
        self.sprite_manager = SpriteManager(self.game_manager.screen)
        self.ui_manager = UIManager(self.game_manager.screen)
        self.collision_manager = CollisionManager()
        
        # ZoneManager ahora maneja internamente el EntityManager
        self.zone_manager = ZoneManager(
            self.game_manager.screen, 
            self.sprite_manager.all_sprites, 
            self.sprite_manager.enemies, 
            self.sprite_manager.spittle_group
        )
        
        self.background_manager = BackgroundManager(self.game_manager.screen)
        self.narrator_manager = NarratorManager()
        
        # Agregar narrador a los sprites
        self.narrator_manager.add_to_sprites(self.sprite_manager.all_sprites)
        
        # Variables de estado del juego
        self.player_lives = 100.0
        self.max_lives = 100.0
                
        # Propiedad para compatibilidad con zonas
        self.background_y = 0

        self.background_was_changed = False
    
    @property
    def screen(self):
        return self.game_manager.screen
    
    @property
    def obstacles(self):
        # Ahora los obstáculos vienen del EntityManager del ZoneManager
        return self.zone_manager.entity_manager.obstacles
    
    @property
    def boosts(self):
        return self.sprite_manager.boosts
    
    @property
    def enemies(self):
        # Los enemigos ahora vienen del EntityManager del ZoneManager
        return self.zone_manager.entity_manager.enemies
    
    @property
    def all_sprites(self):
        return self.sprite_manager.all_sprites

    def run(self):
        while self.game_manager.running:
            self.events()
            self.update()
            self.check_collisions()
            self.draw()
            self.game_manager.clock.tick(DisplaySettings.FPS)

    def events(self):
        self.game_manager.handle_events()

    def update(self):
        if not self.game_manager.game_over:
            keys = get_keys()
            
            if not self.game_manager.game_paused:
                self.game_manager.update_game_state()
                
                # Actualizar sprites (jugador y bots principalmente)
                background_is_moving = self.sprite_manager.update_sprites(
                    keys, 
                    self.game_manager.min_allowed_x, 
                    self.game_manager.max_allowed_x,
                    300,  # min_y
                    self.game_manager.max_allowed_y, 
                    self
                )
                
                # Actualizar fondo
                self.background_manager.update_background()
                self.background_y = self.background_manager.background_y
                
                # Actualizar zonas - ahora maneja internamente las entidades optimizadas
                should_spawn_princess = self.zone_manager.update_zones(
                    self.game_manager.time_to_change_zone, 
                    self, 
                    self.sprite_manager.player, 
                    self.sprite_manager.bots, 
                    background_is_moving
                )
                
                # Spawnar princesa si es necesario
                if should_spawn_princess and not self.game_manager.princess_spawned:
                    print("Princess spawned")
                    self.background_manager.change_end_background()
                    self.sprite_manager.spawn_princess()
                    self.game_manager.princess_spawned = True
                
                #self.zone_manager.update_gas_zone()
                self.collision_manager.apply_velocity_boosts(self.sprite_manager)

        # Actualizar narrador (siempre se ejecuta)
        narrator_finished = self.narrator_manager.update_narrator()
        if narrator_finished and self.game_manager.game_paused:
            self.game_manager.game_paused = False
            
    @property
    def min_allowed_y(self):
        return getattr(self.game_manager, 'min_allowed_y', 300)

    @min_allowed_y.setter
    def min_allowed_y(self, value):
        self.game_manager.min_allowed_y = value

    def check_collisions(self):
        damage_taken, level_won = self.collision_manager.check_all_collisions(
            self.sprite_manager, 
            self.zone_manager,  
            self.game_manager,
            
        )
        
        if damage_taken > 0:
            self.player_lives -= damage_taken
            if self.player_lives <= 0:
                self.game_manager.game_over = True
        
        if level_won:
            self.game_manager.win_level(self.game_manager.screen)
        
        # Actualizar contador de gases evitados - ahora usando el EntityManager
        for gas in self.zone_manager.entity_manager.obstacles:
            if hasattr(gas, 'rect') and gas.rect.y > self.game_manager.screen.get_height():
                if self.zone_manager.zone == "gas":
                    self.zone_manager.count_gas_avoided()
     
    @property
    def background_speed(self):
        return getattr(self.background_manager, 'background_speed', 2)

    @background_speed.setter
    def background_speed(self, value):
        if hasattr(self.background_manager, 'background_speed'):
            self.background_manager.background_speed = value
        else:
            # Si no existe, crearlo
            self.background_manager.background_speed = value

    @property
    def original_background_speed(self):
        return getattr(self.background_manager, 'original_background_speed', 2)

    @original_background_speed.setter
    def original_background_speed(self, value):
        if hasattr(self.background_manager, 'original_background_speed'):
            self.background_manager.original_background_speed = value
        else:
            # Si no existe, crearlo
            self.background_manager.original_background_speed = value     
     
    def draw(self):
        # Dibujar fondo
        self.background_manager.draw_background()
        
        # Dibujar sprites (jugador, bots, etc.)
        self.sprite_manager.draw_sprites(self.game_manager.screen)
        
        # Dibujar todas las entidades gestionadas por ZoneManager
        self.zone_manager.draw_all_entities(self.game_manager.screen)
        
        # Dibujar UI
        self.ui_manager.draw_health_bar(self.player_lives, self.max_lives)
        
        # Overlay de pausa
        if self.game_manager.game_paused and not self.game_manager.game_over:
            self.ui_manager.draw_pause_overlay()
        
        # Dibujar narrador
        self.narrator_manager.draw_narrator(self.game_manager.screen)
        
        # Game Over
        if self.game_manager.game_over:
            self.ui_manager.draw_game_over()
        
        pygame.display.update()