# scenes/cell_level_zones/managers/collision_manager.py
import pygame
from entities.optimized_obstacles import ObstacleMoco, ObstacleGas, ObstacleVelocity



class CollisionManager:
    def __init__(self):
        self.kill_count = 0
    
    def check_all_collisions(self, sprite_manager, zone_manager, game_manager):
        if game_manager.game_paused or game_manager.game_over:
            return 0, False
        
        damage_taken = 0
        level_won = False
        
        # Obtener grupos de colisión del entity manager
        collision_groups = zone_manager.entity_manager.get_collision_groups()
        # Colisiones con obstáculos (incluyendo mocos y gas)
        for obstacle in collision_groups['obstacles']:
            if sprite_manager.player.rect.colliderect(obstacle.rect):
                if isinstance(obstacle, ObstacleMoco):
                    obstacle.apply_effect(sprite_manager.player)
                elif isinstance(obstacle, ObstacleGas):
                    if sprite_manager.player.take_damage(15.0):
                        damage_taken = 15.0
                        print(f"Vida restante (tras tocar gas): {damage_taken}%")
        
        # Colisiones del jugador con obstáculos del sprite_manager (compatibilidad)
        if hasattr(sprite_manager, 'obstacles'):
            hits = pygame.sprite.spritecollide(sprite_manager.player, sprite_manager.obstacles, False)
            if hits:
                if sprite_manager.player.take_damage(15.0):
                    damage_taken = 15.0
                    print(f"Vida restante (tras tocar obstáculo): {damage_taken}%")
                    
        # Colisiones del jugador con enemigos del entity_manager
        for enemy in collision_groups['enemies']:
            if sprite_manager.player.rect.colliderect(enemy.rect):
                if sprite_manager.player.take_damage(25.0):
                    damage_taken = 25.0
                    print(f"Vida restante (tras tocar enemigo): {damage_taken}%")
        
        # Colisiones del jugador con enemigos del sprite_manager (compatibilidad)
        if hasattr(sprite_manager, 'enemies'):
            hits = pygame.sprite.spritecollide(sprite_manager.player, sprite_manager.enemies, False)
            if hits:
                if sprite_manager.player.take_damage(25.0):
                    damage_taken = 25.0
                    print(f"Vida restante (tras tocar leucocito): {damage_taken}%")
        
        # Colisiones con princesa (victoria)
        if game_manager.princess_spawned and hasattr(sprite_manager, 'princess'):
            hits = pygame.sprite.spritecollide(sprite_manager.player, sprite_manager.princess, False)
            if hits:
                level_won = True
        
        # Colisiones de balas con enemigos del entity_manager
        if hasattr(sprite_manager.player, 'bullets'):
            for bullet in sprite_manager.player.bullets:
                for enemy in collision_groups['enemies']:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.kill()  # Eliminar enemigo
                        bullet.kill()  # Eliminar bala
                        self.kill_count += 1
                        print(f"Enemigos eliminados: {self.kill_count}")
                        break  # Una bala solo puede golpear un enemigo
        
        # Colisiones de balas con enemigos del sprite_manager (compatibilidad)
        if hasattr(sprite_manager.player, 'bullets') and hasattr(sprite_manager, 'enemies'):
            for bullet in sprite_manager.player.bullets:
                hits = pygame.sprite.spritecollide(bullet, sprite_manager.enemies, True)
                if hits:
                    self.kill_count += len(hits)
                    print(f"Leucocitos eliminados: {self.kill_count}")
                    bullet.kill()
        
        # Colisiones de bots con obstáculos
        if hasattr(sprite_manager, 'boosts'):
            for boost in sprite_manager.boosts:
                if sprite_manager.player.rect.colliderect(boost.rect):
                   if isinstance(boost, ObstacleVelocity):
                        boost.player_impulse() 
                        if hasattr(sprite_manager, 'bots'):
                            for bot in sprite_manager.bots:
                                bot.freeze_due_to_player_boost()
                if hasattr(sprite_manager, 'bots'):
                   for bot in sprite_manager.bots:
                       if bot.rect.colliderect(boost.rect):
                          if isinstance(boost, ObstacleVelocity):
                             bot.rect = boost.apply_impulse(bot.rect)
                
                                
                for enemy in collision_groups['enemies']:
                    if bot.rect.colliderect(enemy.rect):
                        bot.take_damage(25.0)
                
                # Enemigos del sprite_manager (compatibilidad)
                if hasattr(sprite_manager, 'enemies'):
                    hits = pygame.sprite.spritecollide(bot, sprite_manager.enemies, False)
                    if hits:
                        bot.take_damage(25.0)
                
                # Colisiones de bots con princesa (game over)
                if game_manager.princess_spawned and hasattr(sprite_manager, 'princess'):
                    hits = pygame.sprite.spritecollide(bot, sprite_manager.princess, False)
                    if hits:
                        game_manager.game_over = True
        
        return damage_taken, level_won
    
    def apply_velocity_boosts(self, sprite_manager):
        if hasattr(sprite_manager, 'boosts'):
            for boost in sprite_manager.boosts:
                if sprite_manager.player.rect.colliderect(boost.rect):
                    sprite_manager.player.rect = boost.apply_impulse(sprite_manager.player.rect)
                    sprite_manager.player.impulsed = True
                    sprite_manager.player.impulse_timer = pygame.time.get_ticks()

                if hasattr(sprite_manager, 'bots'):
                    for bot in sprite_manager.bots:
                        if bot.rect.colliderect(boost.rect):
                            bot.rect = boost.apply_impulse(bot.rect)