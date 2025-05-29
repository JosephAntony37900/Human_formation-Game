# scenes/cell_level_zones/managers/zone_manager.py
from entities.entity_manager import EntityManager
from ..zones.lactobacilo_Zone import LactobaciloZone
from ..zones.leucocito_Zone import LeucocitoZone
from ..zones.gas_Zone import GasZone
from ..zones.waves_Zone import WavesZone
from ..zones.moco_zone import MocoZone

class ZoneManager:
    def __init__(self, screen, sprite_manager, spittle_group):
        self.screen = screen
        self.zone_name = ""
        self.zone = "gas"
        self.gases_avoided = 0
        self.sprite_manager = sprite_manager
        
        # Crear el gestor de entidades
        self.entity_manager = EntityManager()
        
        # Inicializar zonas con el entity manager
        self.gas_zone = GasZone(self.entity_manager)
        self.moco_zone = MocoZone(self.entity_manager)
        self.wave_zone = WavesZone(self.entity_manager)
        self.leucocito_zone = LeucocitoZone(self.entity_manager)
        self.lactobacilo_zone = LactobaciloZone(self.entity_manager, spittle_group)

        self.background_was_changed = False
    
    def update_zones(self, time_to_change_zone, level_ref, player, bots, background_is_moving, background_manager):
        # Actualizar todas las entidades
        self.entity_manager.update_all(player, bots)
        
        # Verificar colisiones de moco
        self.moco_zone.check_collision_with_player(player)
        self.moco_zone.check_collision_with_bots(bots, background_is_moving)
        
        player_x = player.rect.centerx
        player_y = player.rect.centery
        
        # Lógica de zonas por tiempo
        if time_to_change_zone >= 10000 and time_to_change_zone <= 20000:  # 10 seg
            self.zone_name = "GAS"
            self.gas_zone.spawn_gases_function(level_ref, self.sprite_manager)
        elif time_to_change_zone >= 20000 and time_to_change_zone <= 30000:  # 20 seg
            self.zone_name = "RAMPAS"
            self.wave_zone.spawn_waves(level_ref)
        elif time_to_change_zone >= 30000 and time_to_change_zone <= 40000:  # 30 seg
            self.zone_name = "MOCOS"
            self.moco_zone.spawn_mocos(level_ref.background_y, player_x, player_y, 
                                     level_ref.game_manager.min_allowed_y, 
                                     level_ref.game_manager.max_allowed_y,
                                     self.sprite_manager)
        elif time_to_change_zone >= 40000 and time_to_change_zone <= 50000:  # 40 seg
            self.zone_name = "ENEMIGOS"
            self.leucocito_zone.spawn_enemy(level_ref, self.sprite_manager)
            self.lactobacilo_zone.spawn_enemy(level_ref, self.sprite_manager)
        elif time_to_change_zone >= 55000 and not self.background_was_changed:
            print("Cambiando fondo")
            background_manager.change_end_background()
            self.background_was_changed = True
        elif time_to_change_zone >= 60000:  # 50 seg
            self.zone_name = "PRINCESS"
            return True  # Indica que es momento de la princesa
        
        # Lógica de cambio de zona por gas
        if self.zone == "gas" and self.gases_avoided >= 20:
            self.zone = "leucocito"
            print("¡Has pasado a la zona de leucocitos!")
        elif self.zone == "lactobacilo":
            self.lactobacilo_zone.update(level_ref.background_y)
        
        return False
    
    def draw_all_entities(self, screen):
        """Dibuja todas las entidades gestionadas"""
        self.entity_manager.draw_all(screen)
    
    def get_collision_groups(self):
        """Retorna grupos para detección de colisiones"""
        return self.entity_manager.get_collision_groups()
    
    def count_gas_avoided(self):
        self.gases_avoided += 1
        print(f"Gases esquivados: {self.gases_avoided}/20")