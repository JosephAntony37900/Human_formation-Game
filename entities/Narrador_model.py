import pygame
import numpy as np

class Narrator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        w, h = self.screen.get_size()

        try:
            self.image_closed = pygame.image.load("assets/characters/narrador/narrador_lentes.png").convert_alpha()
            self.image_open = pygame.image.load("assets/characters/narrador/narrador_sonrisa.png").convert_alpha()
        except pygame.error as e:
            print(f"Error cargando imágenes: {e}")
            self.image_closed = pygame.Surface((100, 100))
            self.image_open = pygame.Surface((100, 100))
            self.image_closed.fill((255, 0, 0))
            self.image_open.fill((255, 0, 0))

        sprite_w = w // 3
        sprite_h = int(sprite_w * (self.image_closed.get_height() / self.image_closed.get_width()))
        self.base_closed = pygame.transform.scale(self.image_closed, (sprite_w, sprite_h))
        self.base_open = pygame.transform.scale(self.image_open, (sprite_w, sprite_h))
        self.character_image = self.base_closed

        try:
            self.font = pygame.font.Font("assets/fonts/ka1.ttf", 36)
        except pygame.error:
            self.font = pygame.font.Font(None, 36)

        self.full_text = ""
        self.display_text = ""
        self.text_index = 0
        self.text_speed = 100  # Texto más lento
        self.last_char_time = pygame.time.get_ticks()
        self.image = pygame.Surface((w // 2, sprite_h + 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomright=(w - 20, h - 20))
        self.alpha = 0
        self.fading_in = True
        self.fading_out = False
        self.fade_time = pygame.time.get_ticks()
        self.fade_duration = 1000
        self.speaking = False
        self.last_switch = pygame.time.get_ticks()
        self.switch_interval = 300
        self.border_color_index = 0
        self.border_colors = [(255, 255, 255), (150, 150, 150)]
        self.border_switch_time = 500
        self.last_border_switch = pygame.time.get_ticks()
        self.scale_factor = 1.0
        self.scale_speed = 0.002
        self.blink = False
        self.blink_start = 0
        self.blink_duration = 200

        try:
            self.pixel_bg = pygame.image.load("assets/ui/pixel_bg.png").convert_alpha()
        except Exception as e:
            print("No se pudo cargar 'pixel_bg.png':", e)
            self.pixel_bg = None

        pygame.mixer.init()
        sample_rate = 44100
        duration = 0.05
        freq = 440
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * freq * t) * 0.2
        stereo_wave = np.column_stack((wave, wave)).astype(np.int16)
        self.dialogue_sound = pygame.sndarray.make_sound(stereo_wave)

    def update_image(self):
        text_surface = self.font.render(self.display_text, True, (0, 0, 0))
        text_w, text_h = text_surface.get_size()

        scaled_w = int(self.base_closed.get_width() * self.scale_factor)
        scaled_h = int(self.base_closed.get_height() * self.scale_factor)
        char_image = pygame.transform.scale(self.character_image, (scaled_w, scaled_h))

        if self.blink and pygame.time.get_ticks() - self.blink_start < self.blink_duration:
            char_image.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)

        char_w, char_h = char_image.get_size()
        text_box_w = text_w + 40
        text_box_h = text_h + 20
        w = text_box_w + char_w + 20
        h = max(text_box_h, char_h + 20)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)

        if self.pixel_bg:
            pattern = pygame.transform.scale(self.pixel_bg, (4, 4))
            for x in range(0, text_box_w, pattern.get_width()):
                for y in range(10, 10 + text_box_h, pattern.get_height()):
                    self.image.blit(pattern, (x, y))
        else:
            pygame.draw.rect(self.image, (255, 255, 255, self.alpha), (0, 10, text_box_w, text_box_h))

        pygame.draw.rect(
            self.image,
            (*self.border_colors[self.border_color_index], self.alpha),
            (0, 10, text_box_w, text_box_h),
            width=3
        )

        self.image.blit(text_surface, (20, 20))
        self.image.blit(char_image, (text_box_w, (h - char_h) // 2))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(bottomright=self.rect.bottomright)

    def update(self, new_text):
        if new_text != self.full_text:
            self.full_text = new_text
            self.display_text = ""
            self.text_index = 0
            self.speaking = True
            self.last_switch = pygame.time.get_ticks()
            self.blink = True
            self.blink_start = pygame.time.get_ticks()
            self.update_image()

    def update_speaking(self):
        if self.speaking:
            current_time = pygame.time.get_ticks()
            if self.text_index < len(self.full_text) and current_time - self.last_char_time >= self.text_speed:
                self.display_text += self.full_text[self.text_index]
                self.text_index += 1
                self.last_char_time = current_time
                self.dialogue_sound.play()

            if current_time - self.last_switch >= self.switch_interval:
                self.character_image = self.base_open if self.character_image == self.base_closed else self.base_closed
                self.last_switch = current_time

            if current_time - self.last_border_switch >= self.border_switch_time:
                self.border_color_index = (self.border_color_index + 1) % len(self.border_colors)
                self.last_border_switch = current_time

            self.scale_factor = 1.0 + 0.01 * np.sin(current_time * self.scale_speed)  # Menos movimiento
            self.update_image()
            if self.text_index >= len(self.full_text):
                self.speaking = False

    def start_fade_out(self):
        self.fading_out = True
        self.fading_in = False
        self.fade_time = pygame.time.get_ticks()
        self.speaking = False
        self.character_image = self.base_closed
        self.update_image()

    def update_fade(self):
        t = pygame.time.get_ticks() - self.fade_time
        progress = min(t / self.fade_duration, 1)
        if self.fading_in:
            self.alpha = int(255 * progress)
            if progress >= 1:
                self.fading_in = False
        elif self.fading_out:
            self.alpha = int(255 * (1 - progress))
            if self.alpha <= 0:
                # Cambiado: el evento ahora usa "narrator_done": True para evitar conflictos
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"narrator_done": True}))
                self.kill()
        self.update_image()
