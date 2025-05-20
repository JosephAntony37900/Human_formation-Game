import pygame
from config.Display_settings import DisplaySettings
from entities.Player_model import Player
from entities.Narrador_model import Narrator
from entities.Obstacule_gas import Obstacle
from entities.Obstacule_velocity import ObstaculeVelocity
from entities.Enemy_leucocito import EnemyLeucocito
from .zones.lactobacilo_Zone import LactobaciloZone
from .zones.leucocito_Zone import LeucocitoZone
from entities.Bullet import Bullet
from inputs.keyboard import get_keys
from .zones.gas_Zone import GasZone
from .zones.waves_Zone import WavesZone
from entities.Bot_Espermanauta import BotEspermanauta
from .zones.moco_zone import MocoZone

import random

class CellLevel:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(DisplaySettings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_paused = True
        self.player = Player(100, 100)
        self.player.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 200)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.bots = pygame.sprite.Group()
        self.bots.add(
            BotEspermanauta(500, 800), 
            BotEspermanauta(600, 800), 
            BotEspermanauta(700, 800), 
            BotEspermanauta(800, 800),
            BotEspermanauta(900, 800),
            BotEspermanauta(1000, 800),
            BotEspermanauta(1100, 800),
            BotEspermanauta(1200, 800),
            BotEspermanauta(1300, 800),
            BotEspermanauta(1400, 800)
        )
        self.all_sprites.add(self.bots)
        self.boosts = pygame.sprite.Group()
        self.all_sprites.add(self.boosts)
        self.player_lives = 100.0
        self.max_lives = 100.0
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.health_bar_x = self.screen.get_width() - self.health_bar_width - 10
        self.health_bar_y = 10
        self.health_font = pygame.font.Font(None, 24)
        self.kill_count = 0
        self.enemies = pygame.sprite.Group()
        self.spittle_group = pygame.sprite.Group()
        self.time_to_change_zone = pygame.time.get_ticks()
        self.zone_name = ""


        try:
            self.kill_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 25)
            self.game_over_font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 60)
        except:
            print("Error cargando Pixelify Sans, usando fuente por defecto")
            self.kill_font = pygame.font.Font(None, 24)
            self.game_over_font = pygame.font.Font(None, 60)

        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.gas_zone = GasZone(self.screen, self.all_sprites)
        self.moco_zone = MocoZone(self.screen, self.all_sprites)# Zona de mocos
        self.wave_zone = WavesZone(self.screen, self.all_sprites)
        self.leucocito_zone = LeucocitoZone(self.screen, self.all_sprites, self.enemies)
        self.lactobacilo_zone = LactobaciloZone(self.screen, self.all_sprites, self.enemies, self.spittle_group)
        self.start_time = pygame.time.get_ticks()
        self.spawn_enabled = False
        self.spawn_background_y_threshold = 100
        self.narrator = Narrator()
        self.all_sprites.add(self.narrator)

        try:
            self.background = pygame.image.load("assets/backgrounds/background_1.png")
            info = pygame.display.Info()
            self.background = pygame.transform.scale(self.background, (info.current_w, info.current_h))
        except pygame.error as e:
            print(f"Error al cargar background image: {e}")
            self.background = None

        self.background_y = 0
        self.background_speed = 2
        self.original_background_speed = self.background_speed  
        self.texts = ["¡Prepárate para la batalla!", "¡El enemigo se acerca!", "¡Lucha valientemente, soldado!"]
        self.current_text_index = 0
        self.max_texts = len(self.texts) - 1
        self.text_switch_time = 3000
        self.last_text_switch = pygame.time.get_ticks()
        self.time_after_last_message = None
        self.fade_wait_time = 2000
        self.fade_started = False

        self.min_allowed_y = self.player.rect.y
        self.max_allowed_y = 800
        self.min_allowed_x = 40
        self.max_allowed_x = pygame.display.Info().current_w - 40

        self.game_over = False
        self.gases_avoided = 0
        self.zone = "gas"
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.enemy_spawn_interval = 2000
        self.music_start_time = pygame.time.get_ticks()
        self.music_started = False

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.check_collisions()
            self.draw()
            self.clock.tick(DisplaySettings.FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        if not self.game_over:
            keys = get_keys()
            if not self.game_paused:
                music_current_time = pygame.time.get_ticks()
                self.time_to_change_zone = pygame.time.get_ticks() - self.start_time
                background_is_moving = self.player.update(keys, self.min_allowed_x, self.max_allowed_x, 300, self.max_allowed_y, self)
                for bot in self.bots:
                    bot.update(self.min_allowed_x + 300, self.max_allowed_x - 300, 300, self.max_allowed_y, self, self.enemies, list(self.obstacles) + list(self.boosts), background_is_moving)
                self.player.bullets.update()

                self.update_obstacles()
                self.update_enemies()
                self.gas_zone.update_gases()
                player_x = self.player.rect.centerx
                player_y = self.player.rect.centery
                
                self.moco_zone.update_mocos(self.player, self.bots, background_is_moving)
                self.background_y += self.background_speed

                if self.time_to_change_zone >= 10000 and self.time_to_change_zone <= 50000: # 10 seg
                    self.zone_name = "GAS"
                    # self.gas_zone.spawn_gases(self.background_y, player_x, player_y, self.min_allowed_y, self.max_allowed_y)
                    self.gas_zone.spawn_gases_function(self)
                elif self.time_to_change_zone >= 50000 and self.time_to_change_zone <= 110000: # 50 seg
                    self.zone_name = "RAMPAS"
                    self.wave_zone.spawn_waves(self)
                elif self.time_to_change_zone >= 110000 and self.time_to_change_zone <= 140000: # 110 seg
                    self.zone_name = "MOCOS"
                    self.moco_zone.spawn_mocos(self.background_y, player_x, player_y, self.min_allowed_y, self.max_allowed_y)
                elif self.time_to_change_zone >= 140000 and self.time_to_change_zone <= 200000: # 140 seg
                    self.zone_name = "ENEMIGOS"
                    self.leucocito_zone.spawn_enemy(self)
                    self.lactobacilo_zone.spawn_enemy(self)
                elif self.time_to_change_zone >= 200000: # 200 seg
                    self.zone_name = "PRINCESS"
                
                if self.zone == "gas" and self.gases_avoided >= 20:
                  self.zone = "leucocito"
                  print("¡Has pasado a la zona de leucocitos!")

                # elif self.zone == "leucocito":
                #      self.handle_enemy_spawning()
                #      if self.kill_count >= 20:
                #         self.zone = "lactobacilo"
                #         print("¡Has llegado a la zona de lactobacilos!")

                elif self.zone == "lactobacilo":
                    self.lactobacilo_zone.update_lactobacilos(self.background_y)
                
                if not self.music_started and music_current_time - self.music_start_time >= 15000:
                    pygame.mixer.music.load("assets/music/Cosmicv1.mp3")
                    pygame.mixer.music.play(-1)
                    self.music_started = True


            current_time = pygame.time.get_ticks()
            if self.current_text_index <= self.max_texts:
                if current_time - self.last_text_switch >= self.text_switch_time:
                    self.narrator.update(self.texts[self.current_text_index])
                    self.current_text_index += 1
                    self.last_text_switch = current_time
            elif self.time_after_last_message is None:
                self.time_after_last_message = current_time

            if self.time_after_last_message is not None and current_time - self.time_after_last_message >= self.fade_wait_time:
                if not self.fade_started:
                    self.narrator.start_fade_out()
                    self.fade_started = True
                self.narrator.update_fade()
                if self.narrator.alpha <= 0:
                    self.game_paused = False

            self.narrator.update_speaking()
            self.apply_velocity_boosts()

    def update_obstacles(self):
        for gas in self.obstacles:
            gas.update()
            if gas.rect.y > self.screen.get_height():
                gas.kill()
                if self.zone == "gas":
                    self.gases_avoided += 1
                    print(f"Gases esquivados: {self.gases_avoided}/20")
        for boost in self.boosts:
            boost.update()
            if boost.rect.y > self.screen.get_height():
                boost.kill()

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update(self.player, self.bots)
            if enemy.rect.y > self.screen.get_height():
                enemy.kill()

    def check_collisions(self):
        if not self.game_paused and not self.game_over:
            for moco in self.moco_zone.mocos:
                if self.player.rect.colliderect(moco.rect):
                   self.player.slow_down(self) 

            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if hits:
                if self.player.take_damage(15.0):
                    self.player_lives -= 15.0
                    print(f"Vida restante (tras tocar gas): {self.player_lives}%")
                    if self.player_lives <= 0:
                        self.game_over = True

            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hits:
                if self.player.take_damage(25.0):
                    self.player_lives -= 25.0
                    print(f"Vida restante (tras tocar leucocito): {self.player_lives}%")
                    if self.player_lives <= 0:
                        self.game_over = True

            for bullet in self.player.bullets:
                hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
                if hits:
                    self.kill_count += len(hits)
                    print(f"Leucocitos eliminados: {self.kill_count}")
                    bullet.kill()
            for bot in self.bots:
                hits = pygame.sprite.spritecollide(bot, self.obstacles, False)
                if hits:
                    bot.take_damage(15.0)

            for bot in self.bots:
                hits = pygame.sprite.spritecollide(bot, self.enemies, False)
                if hits:
                    bot.take_damage(25.0)

    def draw(self):
        if self.background:
            bg_height = self.background.get_height()
            offset = self.background_y % bg_height
            self.screen.blit(self.background, (0, offset - bg_height))
            self.screen.blit(self.background, (0, offset))
        else:
            self.screen.fill((0, 0, 0))

        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.player.draw(self.screen)

        if self.game_paused and not self.game_over:
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))

        if self.narrator.alive():
            self.screen.blit(self.narrator.image, self.narrator.rect)

        pygame.draw.rect(self.screen, (100, 100, 100), (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height))
        health_percentage = self.player_lives / self.max_lives
        current_health_width = self.health_bar_width * health_percentage
        pygame.draw.rect(self.screen, (255, 0, 0), (self.health_bar_x, self.health_bar_y, current_health_width, self.health_bar_height))

        health_text = self.health_font.render(f"Vida: {int(self.player_lives)}%", True, (255, 255, 255))
        self.screen.blit(health_text, (self.health_bar_x - health_text.get_width() - 10, self.health_bar_y))

        if self.game_over:
            game_over_text = self.game_over_font.render("¡Juego Terminado!", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, self.screen.get_height() // 2))

        pygame.display.update()

    def apply_velocity_boosts(self):
        for boost in self.boosts:
            if self.player.rect.colliderect(boost.rect):
                self.player.rect = boost.impulse(self.player.rect)

        for bot in self.bots:
            for boost in self.boosts:
                if bot.rect.colliderect(boost.rect):
                    bot.rect = boost.impulse(bot.rect)

    def apply_moco_slowdown(self):
        for moco in self.moco_zone.mocos:
            if self.player.rect.colliderect(moco.rect):
                self.player.slow_down(self)

        for bot in self.bots:
            for moco in self.moco_zone.mocos:
                if bot.rect.colliderect(moco.rect):
                    bot.slow_down()
