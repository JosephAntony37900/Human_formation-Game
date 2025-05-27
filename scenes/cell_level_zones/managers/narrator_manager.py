# scenes/cell_level_zones/managers/narrator_manager.py
import pygame
from entities.Narrador_model import Narrator

class NarratorManager:
    def __init__(self):
        self.narrator = Narrator()
        
        # Configuración de textos
        self.texts = ["¡Prepárate para la batalla!", "¡El enemigo se acerca!", "¡Lucha valientemente, soldado!"]
        self.current_text_index = 0
        self.max_texts = len(self.texts) - 1
        self.text_switch_time = 3000
        self.last_text_switch = pygame.time.get_ticks()
        self.time_after_last_message = None
        self.fade_wait_time = 2000
        self.fade_started = False
    
    def update_narrator(self):
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
                return True  # Indica que el juego puede empezar
        
        self.narrator.update_speaking()
        return False
    
    def draw_narrator(self, screen):
        if self.narrator.alive():
            screen.blit(self.narrator.image, self.narrator.rect)
    
    def add_to_sprites(self, sprite_group):
        sprite_group.add(self.narrator)