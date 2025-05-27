# scenes/cell_level_zones/managers/zone_manager.py
from ..zones.lactobacilo_Zone import LactobaciloZone
from ..zones.leucocito_Zone import LeucocitoZone
from ..zones.gas_Zone import GasZone
from ..zones.waves_Zone import WavesZone
from ..zones.moco_zone import MocoZone

class ZoneManager:
    def __init__(self, screen, all_sprites, enemies, spittle_group):
        self.screen = screen
        self.zone_name = ""
        self.zone = "gas"
        self.gases_avoided = 0
        
        # Inicializar zonas
        self.gas_zone = GasZone(screen, all_sprites)
        self.moco_zone = MocoZone(screen, all_sprites)
        self.wave_zone = WavesZone(screen, all_sprites)
        self.leucocito_zone = LeucocitoZone(screen, all_sprites, enemies)
        self.lactobacilo_zone = LactobaciloZone(screen, all_sprites, enemies, spittle_group)
    
    def update_zones(self, time_to_change_zone, level_ref, player, bots, background_is_moving):
        player_x = player.rect.centerx
        player_y = player.rect.centery
        
        self.moco_zone.update_mocos(player, bots, background_is_moving)
        
        if time_to_change_zone >= 10000 and time_to_change_zone <= 20000:  # 10 seg
            self.zone_name = "GAS"
            self.gas_zone.spawn_gases_function(level_ref)
        elif time_to_change_zone >= 20000 and time_to_change_zone <= 30000:  # 20 seg
            self.zone_name = "RAMPAS"
            self.wave_zone.spawn_waves(level_ref)
        elif time_to_change_zone >= 30000 and time_to_change_zone <= 40000:  # 30 seg
            self.zone_name = "MOCOS"
            self.moco_zone.spawn_mocos(level_ref.background_y, player_x, player_y, 
                                     level_ref.game_manager.min_allowed_y, 
                                     level_ref.game_manager.max_allowed_y)
        elif time_to_change_zone >= 40000 and time_to_change_zone <= 50000:  # 40 seg
            self.zone_name = "ENEMIGOS"
            self.leucocito_zone.spawn_enemy(level_ref)
            self.lactobacilo_zone.spawn_enemy(level_ref)
        elif time_to_change_zone >= 50000:  # 50 seg
            self.zone_name = "PRINCESS"
            return True  # Indica que es momento de la princesa
        
        # Lógica de cambio de zona por gas
        if self.zone == "gas" and self.gases_avoided >= 20:
            self.zone = "leucocito"
            print("¡Has pasado a la zona de leucocitos!")
        elif self.zone == "lactobacilo":
            self.lactobacilo_zone.update_lactobacilos(level_ref.background_y)
        
        return False
    
    def update_gas_zone(self):
        self.gas_zone.update_gases()
    
    def count_gas_avoided(self):
        self.gases_avoided += 1
        print(f"Gases esquivados: {self.gases_avoided}/20")