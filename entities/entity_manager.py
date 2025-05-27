# entities/entity_manager.py
import pygame
from entities.base_entity import BaseEntity
from entities.optimized_enemies import EnemyLeucocito, EnemyLactobacilo, Spittle

class EntityManager:
    """Gestor centralizado de entidades para optimizar actualizaciones"""
    
    def __init__(self):
        self.all_entities = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
    def add_entity(self, entity: BaseEntity, entity_type: str = "general"):
        """Añade una entidad al gestor"""
        self.all_entities.add(entity)
        
        if entity_type == "obstacle":
            self.obstacles.add(entity)
        elif entity_type == "enemy":
            self.enemies.add(entity)
        elif entity_type == "projectile":
            self.projectiles.add(entity)
    
    def update_all(self, player, bots):
        """Actualiza todas las entidades y limpia las marcadas para eliminación"""
        # Actualizar entidades
        for entity in self.all_entities:
            if hasattr(entity, 'update'):
                if isinstance(entity, (EnemyLeucocito, EnemyLactobacilo, Spittle)):
                    entity.update(player, bots)
                else:
                    entity.update()
        
        # Limpiar entidades marcadas para eliminación
        to_remove = [entity for entity in self.all_entities if entity.should_be_deleted()]
        for entity in to_remove:
            entity.kill()  # Removes from all groups
    
    def draw_all(self, screen):
        """Dibuja todas las entidades"""
        self.all_entities.draw(screen)
    
    def get_collision_groups(self):
        """Retorna grupos para detección de colisiones"""
        return {
            'obstacles': self.obstacles,
            'enemies': self.enemies,
            'projectiles': self.projectiles
        }