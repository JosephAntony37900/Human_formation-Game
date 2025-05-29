import pygame
from entities.Narrador_model import Narrator

class NarratorManager:
    def __init__(self):
        self.narrator = Narrator()
        self.texts = [
            "¡Prepárate para la batalla!",
            "¡El enemigo se acerca!",
            "¡Lucha valientemente, soldado!"
        ]
        self.current_text_index = 0
        self.max_texts = len(self.texts) - 1
        self.text_switch_time = 1000
        self.last_text_switch = pygame.time.get_ticks()
        self.time_after_last_message = None
        self.fade_wait_time = 2000
        self.fade_started = False
        self.finished = False
        self.gameplay_enabled = False

    def add_to_sprites(self, group):
        group.add(self.narrator)

    def handle_event(self, event):
        # Detecta evento que el narrador terminó el fade out
        if event.type == pygame.USEREVENT and event.dict.get("narrator_done"):
            self.finished = True
            self.gameplay_enabled = True

    def update_narrator(self):
        current_time = pygame.time.get_ticks()
        self.narrator.update_fade()

        if self.current_text_index <= self.max_texts:
            if self.narrator.display_text != self.texts[self.current_text_index]:
                self.narrator.update(self.texts[self.current_text_index])
            elif not self.narrator.speaking and current_time - self.last_text_switch >= self.text_switch_time:
                self.current_text_index += 1
                self.last_text_switch = current_time
        elif self.time_after_last_message is None:
            self.time_after_last_message = current_time

        if self.time_after_last_message is not None and current_time - self.time_after_last_message >= self.fade_wait_time:
            if not self.fade_started:
                self.narrator.start_fade_out()
                self.fade_started = True

        self.narrator.update_speaking()

        # Ya no seteamos finished ni gameplay_enabled aquí
        return self.finished

    def draw_narrator(self, screen):
        if self.narrator.alive():
            screen.blit(self.narrator.image, self.narrator.rect)

    def can_play(self):
        return self.gameplay_enabled
