# scenes/cell_level_zones/managers/sprite_manager.py
import pygame
from entities.Player_model import Player
from entities.Bot_Espermanauta import BotEspermanauta
from entities.Entity_princess import PrincessMononoke
from entities.Entity_Castle import Castle

class SpriteManager:
    def __init__(self, screen):
        self.screen = screen
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.bots = pygame.sprite.Group()
        self.boosts = pygame.sprite.Group()
        self.gases = pygame.sprite.Group()
        self.mocos = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.spittle_group = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.princess = pygame.sprite.Group()
        self.castles = pygame.sprite.Group()
        
        # Crear jugador
        self.player = Player(100, 100)
        self.player.rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 200)
        self.all_sprites.add(self.player)
        
        # Crear bots
        bot_positions = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400]
        for x in bot_positions:
            bot = BotEspermanauta(x, 800)
            self.bots.add(bot)
        
        self.all_sprites.add(self.bots)
        self.all_sprites.add(self.boosts)
        self.all_sprites.add(self.gases)
        self.all_sprites.add(self.mocos)
    
    def spawn_princess(self):
        princess = PrincessMononoke()
        self.princess.add(princess)
        castle = Castle()
        self.castles.add(castle)
        self.all_sprites.add(self.princess, self.castles)
        return True
    
    def update_sprites(self, keys, min_x, max_x, min_y, max_y, level_ref):
        background_is_moving = self.player.update(keys, min_x, max_x, min_y, max_y, level_ref)
        
        for bot in self.bots:
            bot.update(min_x + 300, max_x - 300, min_y, max_y, level_ref, 
                      self.enemies, list(self.obstacles) + list(self.boosts) + list(self.gases) + list(self.mocos), 
                      background_is_moving, self.princess)
        
        self.player.bullets.update()
        
        # Actualizar enemigos
        for enemy in self.enemies:
            enemy.update(self.player, self.bots)
            if enemy.rect.y > self.screen.get_height():
                enemy.kill()
        
        # Actualizar obstáculos
        for gas in self.obstacles:
            gas.update()
            if gas.rect.y > self.screen.get_height():
                gas.kill()
        
        for boost in self.boosts:
            boost.update()
            if boost.rect.y > self.screen.get_height():
                boost.kill()
        
        # Actualizar princesa
        for princess in self.princess:
            princess.update()
        
        for castle in self.castles:
            castle.update()
        
        return background_is_moving
    
    def draw_sprites(self, screen):
        self.all_sprites.draw(screen)
        self.player.bullets.draw(screen)
        self.player.draw(screen)