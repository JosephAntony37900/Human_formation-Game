import pygame

class Narrator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.character_image = pygame.image.load("assets/characters/narrador_lentes.png").convert_alpha()
        self.character_image = pygame.transform.scale(self.character_image, (250, 250))
        self.font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 25)
        self.text = ""
        self.image = pygame.Surface((400, 120), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        display_surface = pygame.display.get_surface()
        if display_surface:
            self.rect.bottomright = (display_surface.get_width() - 20, display_surface.get_height() - 20)
        else:
            self.rect.bottomright = (800, 600)
        self.alpha = 255
        self.fading = False
        self.fade_start_time = 0
        self.fade_duration = 2000
        self.update_image()
    def update_image(self):
        rendered_text = self.font.render(self.text, True, (0, 0, 0))
        text_width, text_height = rendered_text.get_size()
        char_width, char_height = self.character_image.get_size()
        offset_x = 30
        new_width = 5 + text_width + 10 + char_width + 10
        new_height = max(text_height, char_height) + 30
        old_bottomright = self.rect.bottomright
        self.image = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255, self.alpha), (5 + offset_x, 5, text_width + 20, text_height + 20), border_radius=15)
        pygame.draw.rect(self.image, (139, 69, 19, self.alpha), (5 + offset_x, 5, text_width + 20, text_height + 20), border_radius=15, width=3)
        text_y = (new_height - text_height) // 18
        self.image.blit(rendered_text, (15 + offset_x, text_y + 10))
        x_img = new_width - char_width - 10
        y_img = (new_height - char_height) // 2
        character_surface = self.character_image.copy()
        character_surface.set_alpha(self.alpha)
        self.image.blit(character_surface, (x_img + offset_x, y_img))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.bottomright = old_bottomright
    def update(self, new_text):
        self.text = new_text
        self.update_image()
    def start_fade_out(self):
        self.fading = True
        self.fade_start_time = pygame.time.get_ticks()
    def update_fade(self):
        if self.fading:
            t = pygame.time.get_ticks() - self.fade_start_time
            progress = min(t / self.fade_duration, 1)
            eased = 1 - (1 - progress) ** 3
            self.alpha = int(255 * (1 - eased))
            if self.alpha <= 0:
                self.alpha = 0
                self.kill()
        self.update_image()
