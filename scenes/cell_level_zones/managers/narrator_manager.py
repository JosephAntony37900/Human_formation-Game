import pygame
from entities.Narrador_model import Narrator

class NarratorManager:
    def __init__(self):
        self.narrator = Narrator()
        self.texts = [
            "¡Preparate para la batalla!",
            "¡El enemigo se acerca!",
            "¡Lucha valientemente, soldado!"
        ]
        self.current_text_index = 0
        self.max_texts = len(self.texts) - 1
        self.text_switch_time = 3000  # milisegundos entre textos
        self.last_text_switch = pygame.time.get_ticks()
        self.time_after_last_message = None
        self.fade_wait_time = 2000
        self.fade_started = False
        self.finished = False
        self.gameplay_enabled = False
        self.narrator_started = False

    def add_to_sprites(self, group):
        group.add(self.narrator)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT and event.dict.get("narrator_done"):
            self.finished = True
            self.gameplay_enabled = True

    def update_narrator(self):
        current_time = pygame.time.get_ticks()
        self.narrator.update_fade()

        if self.current_text_index <= self.max_texts:
            if self.narrator.display_text != self.texts[self.current_text_index]:
                self.narrator.update(self.texts[self.current_text_index])
                self.narrator_started = True
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
        return self.finished

    def draw_narrator(self, screen):
        if self.narrator.alive():
            screen.blit(self.narrator.image, self.narrator.rect)

    def can_play(self):
        if not self.narrator_started:
            self.gameplay_enabled = True
            self.finished = True
        return self.gameplay_enabled

    def is_active(self):
        return self.narrator.alive() and not self.finished

    def is_speaking(self):
        return self.narrator.speaking if self.narrator.alive() else False

    def skip_to_end(self):
        self.current_text_index = self.max_texts + 1
        self.time_after_last_message = pygame.time.get_ticks()
        self.narrator.speaking = False

    def reset(self):
        self.current_text_index = 0
        self.time_after_last_message = None
        self.fade_started = False
        self.finished = False
        self.gameplay_enabled = False
        self.narrator_started = False
        self.last_text_switch = pygame.time.get_ticks()
        old_narrator = self.narrator
        self.narrator = Narrator()
        for group in old_narrator.groups():
            group.remove(old_narrator)
            group.add(self.narrator)

    def get_progress(self):
        if not self.narrator_started:
            return 0.0
        if self.finished:
            return 1.0
        progress = self.current_text_index / (len(self.texts))
        return min(progress, 1.0)
