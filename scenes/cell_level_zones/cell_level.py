import os
import pygame
from config.Display_settings import DisplaySettings
from inputs.keyboard import get_keys
from .managers.game_manager import GameManager
from .managers.sprite_manager import SpriteManager
from .managers.ui_manager import UIManager
from .managers.collision_manager import CollisionManager
from .managers.zone_manager import ZoneManager
from .managers.background_manager import BackgroundManager
from .managers.narrator_manager import NarratorManager

class CellLevel:
    def __init__(self):
        self.game_manager = GameManager()
        self.sprite_manager = SpriteManager(self.game_manager.screen)
        self.ui_manager = UIManager(self.game_manager.screen)
        self.collision_manager = CollisionManager()
        self.zone_manager = ZoneManager(
            self.game_manager.screen, 
            self.sprite_manager,
            self.sprite_manager.spittle_group
        )
        self.background_manager = BackgroundManager(self.game_manager.screen)
        self.narrator_manager = NarratorManager()
        self.narrator_manager.add_to_sprites(self.sprite_manager.all_sprites)
        self.player_lives = 100.0
        self.max_lives = 100.0
        self.background_y = 0

        self.show_menu = False
        font_path = os.path.join("assets/fonts/ka1.ttf")
        self.menu_font = pygame.font.Font(font_path, 30)
        self.menu_options = ["CONTINUAR", "SALIR"]
        self.menu_color = (215, 126, 210)  
        self.border_color = (255, 192, 203)  
        self.shadow_color = (0, 0, 0)
        self.frame_count = 0
        self.menu_selected = 0

    @property
    def screen(self):
        return self.game_manager.screen

    @property
    def obstacles(self):
        return self.zone_manager.entity_manager.obstacles

    @property
    def boosts(self):
        return self.sprite_manager.boosts

    @property
    def enemies(self):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_manager.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = not self.show_menu
                    self.game_manager.game_paused = self.show_menu

                elif self.show_menu:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        self.handle_menu_selection()
                    elif event.key == pygame.K_c:
                        self.show_menu = False
                        self.game_manager.game_paused = False
                    elif event.key == pygame.K_x:
                        pygame.quit()
                        exit()
            else:
                if not self.show_menu:
                    self.game_manager.handle_events()
                    self.narrator_manager.handle_event(event)

    def handle_menu_selection(self):
        sel = self.menu_selected
        if sel == 0:
            self.show_menu = False
            self.game_manager.game_paused = False
        elif sel == 1:
            self.game_manager.running = False
            from scenes.IntroSceneV1 import IntroScene
            intro = IntroScene()
            intro.run()

    def update(self):
        self.frame_count += 1

        if not self.game_manager.game_over:
            keys = get_keys()

            if not self.show_menu:
                narrator_finished = self.narrator_manager.update_narrator()
            else:
                narrator_finished = False

            if narrator_finished:
                self.game_manager.game_paused = False

            if not self.game_manager.game_paused:
                self.game_manager.update_game_state()
                background_is_moving = self.sprite_manager.update_sprites(
                    keys,
                    self.game_manager.min_allowed_x,
                    self.game_manager.max_allowed_x,
                    300,
                    self.game_manager.max_allowed_y,
                    self
                )
                if not self.show_menu:
                    self.background_manager.update_background()
                self.background_y = self.background_manager.background_y
                should_spawn_princess = self.zone_manager.update_zones(
                    self.game_manager.time_to_change_zone, 
                    self, 
                    self.sprite_manager.player, 
                    self.sprite_manager.bots, 
                    background_is_moving,
                    self.background_manager
                )
                if should_spawn_princess and not self.game_manager.princess_spawned:
                    self.sprite_manager.spawn_princess()
                    self.game_manager.princess_spawned = True
                self.collision_manager.apply_velocity_boosts(self.sprite_manager)

    def check_collisions(self):
        damage_taken, level_won = self.collision_manager.check_all_collisions(
            self.sprite_manager,
            self.zone_manager,
            self.game_manager
        )
        if damage_taken > 0:
            self.player_lives -= damage_taken
            if self.player_lives <= 0:
                self.game_manager.game_over = True
        if level_won:
            self.game_manager.win_level(self.game_manager.screen)
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
            self.background_manager.background_speed = value

    @property
    def original_background_speed(self):
        return getattr(self.background_manager, 'original_background_speed', 2)

    @original_background_speed.setter
    def original_background_speed(self, value):
        if hasattr(self.background_manager, 'original_background_speed'):
            self.background_manager.original_background_speed = value
        else:
            self.background_manager.original_background_speed = value

    def draw(self):
        self.background_manager.draw_background()
        self.sprite_manager.draw_sprites(self.game_manager.screen)
        self.zone_manager.draw_all_entities(self.game_manager.screen)
        self.ui_manager.draw_health_bar(self.player_lives, self.max_lives)
        self.narrator_manager.draw_narrator(self.game_manager.screen)

        if self.game_manager.game_paused and not self.game_manager.game_over:
            self.ui_manager.draw_pause_overlay()
            if self.show_menu:
                self.draw_menu()

        if self.game_manager.game_over:
            self.ui_manager.draw_game_over()

        pygame.display.update()

    def draw_menu(self):
        width, height = 500, 200
        screen_center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        menu_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        menu_surface.fill((20, 20, 20, 220))

        border_rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(menu_surface, self.border_color, border_rect, 4, border_radius=20)

        arrow_left = "<"
        arrow_right = ">"

        option_spacing = 60
        start_y = 40

        for i, option in enumerate(self.menu_options):
            rect = pygame.Rect(50, start_y + i * option_spacing, width - 100, 50)
            pygame.draw.rect(menu_surface, self.menu_color, rect, border_radius=15)
            if i == self.menu_selected:
                pygame.draw.rect(menu_surface, self.border_color, rect, 4, border_radius=15)

            label = self.menu_font.render(option, True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            menu_surface.blit(label, label_rect)

            if i == self.menu_selected:
                arrow_l = self.menu_font.render(arrow_left, True, (255, 192, 203))
                arrow_r = self.menu_font.render(arrow_right, True, (255, 192, 203))
                arrow_l_rect = arrow_l.get_rect(midright=(rect.left - 15, rect.centery))
                arrow_r_rect = arrow_r.get_rect(midleft=(rect.right + 15, rect.centery))
                menu_surface.blit(arrow_l, arrow_l_rect)
                menu_surface.blit(arrow_r, arrow_r_rect)

        self.screen.blit(menu_surface, (screen_center[0] - width // 2, screen_center[1] - height // 2))
