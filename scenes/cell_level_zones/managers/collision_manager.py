# scenes/cell_level_zones/managers/collision_manager.py
import pygame

class CollisionManager:
    def __init__(self):
        self.kill_count = 0
    
    def check_all_collisions(self, sprite_manager, moco_zone, game_manager):
        if game_manager.game_paused or game_manager.game_over:
            return 0, False
        
        damage_taken = 0
        level_won = False
        
        # Colisiones con mocos
        for moco in moco_zone.mocos:
            if sprite_manager.player.rect.colliderect(moco.rect):
                sprite_manager.player.slow_down(None)  # Pasar None ya que no se usa
        
        # Colisiones del jugador con obstáculos (gas)
        hits = pygame.sprite.spritecollide(sprite_manager.player, sprite_manager.obstacles, False)
        if hits:
            if sprite_manager.player.take_damage(15.0):
                damage_taken = 15.0
                print(f"Vida restante (tras tocar gas): {damage_taken}%")
        
        # Colisiones del jugador con enemigos
        hits = pygame.sprite.spritecollide(sprite_manager.player, sprite_manager.enemies, False)
        if hits:
            if sprite_manager.player.take_damage(25.0):
                damage_taken = 25.0
                print(f"Vida restante (tras tocar leucocito): {damage_taken}%")
        
        # Colisiones con princesa (victoria)
        if game_manager.princess_spawned:
            hits = pygame.sprite.spritecollide(sprite_manager.player, sprite_manager.princess, False)
            if hits:
                level_won = True
        
        # Colisiones de balas con enemigos
        for bullet in sprite_manager.player.bullets:
            hits = pygame.sprite.spritecollide(bullet, sprite_manager.enemies, True)
            if hits:
                self.kill_count += len(hits)
                print(f"Leucocitos eliminados: {self.kill_count}")
                bullet.kill()
        
        # Colisiones de bots con obstáculos
        for bot in sprite_manager.bots:
            hits = pygame.sprite.spritecollide(bot, sprite_manager.obstacles, False)
            if hits:
                bot.take_damage(15.0)
        
        # Colisiones de bots con enemigos
        for bot in sprite_manager.bots:
            hits = pygame.sprite.spritecollide(bot, sprite_manager.enemies, False)
            if hits:
                bot.take_damage(25.0)
        
        # Colisiones de bots con princesa (game over)
        for bot in sprite_manager.bots:
            if game_manager.princess_spawned:
                hits = pygame.sprite.spritecollide(bot, sprite_manager.princess, False)
                if hits:
                    game_manager.game_over = True
        
        return damage_taken, level_won
    
    def apply_velocity_boosts(self, sprite_manager):
        for boost in sprite_manager.boosts:
            if sprite_manager.player.rect.colliderect(boost.rect):
                sprite_manager.player.rect = boost.impulse(sprite_manager.player.rect)

        for bot in sprite_manager.bots:
            for boost in sprite_manager.boosts:
                if bot.rect.colliderect(boost.rect):
                    bot.rect = boost.impulse(bot.rect)