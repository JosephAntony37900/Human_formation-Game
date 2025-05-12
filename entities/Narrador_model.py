import pygame

class Narrator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # cargar ambas imágenes del narrador
        self.image_closed = pygame.image.load("assets/characters/narrador/narrador_lentes.png").convert_alpha()
        self.image_open = pygame.image.load("assets/characters/narrador/narrador_sonrisa.png").convert_alpha()
        
        # escalamos las imagenes a un tamaño mas pequeño (un cuarto de la pantalla)
        display_surface = pygame.display.get_surface()
        screen_width, screen_height = display_surface.get_width(), display_surface.get_height()
        self.image_closed = pygame.transform.scale(self.image_closed, (screen_width // 4, screen_height // 4))
        self.image_open = pygame.transform.scale(self.image_open, (screen_width // 4, screen_height // 4))
        
        self.character_image = self.image_closed  
        self.font = pygame.font.Font("assets/Pixelify_Sans/pixelfont.ttf", 25)  
        self.text = ""
        self.image = pygame.Surface((screen_width // 3, screen_height // 3), pygame.SRCALPHA)  
        self.rect = self.image.get_rect()
        self.rect.bottomright = (screen_width - 20, screen_height - 20)  
        self.alpha = 255
        self.fading = False
        self.fade_start_time = 0
        self.fade_duration = 2000
        self.speaking = False
        self.last_switch_time = pygame.time.get_ticks()
        self.switch_interval = 400  #
        self.update_image()

    def update_image(self):
        rendered_text = self.font.render(self.text, True, (0, 0, 0))
        text_width, text_height = rendered_text.get_size()
        char_width, char_height = self.character_image.get_size()
        offset_x = 10

        new_width = text_width + char_width + 40 
        new_height = max(text_height + 20, char_height + 20)  
        old_bottomright = self.rect.bottomright
        self.image = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
        
        pygame.draw.rect(self.image, (255, 255, 255, self.alpha), (5, 5, text_width + 20, text_height + 10), border_radius=10)
        pygame.draw.rect(self.image, (139, 69, 19, self.alpha), (5, 5, text_width + 20, text_height + 10), border_radius=10, width=3)
        

        text_y = 5 + (text_height + 10 - text_height) // 2  
        self.image.blit(rendered_text, (15, text_y))  
        x_img = text_width + 25  
        y_img = (new_height - char_height) // 2 
        character_surface = self.character_image.copy()
        character_surface.set_alpha(self.alpha)
        self.image.blit(character_surface, (x_img, y_img))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.bottomright = old_bottomright

    def update(self, new_text):
        self.text = new_text
        self.speaking = True
        self.last_switch_time = pygame.time.get_ticks() 
        self.update_image()

    def update_speaking(self):
        if self.speaking:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_switch_time >= self.switch_interval:
                if self.character_image == self.image_closed:
                    self.character_image = self.image_open
                else:
                    self.character_image = self.image_closed
                self.last_switch_time = current_time
                self.update_image()

    def start_fade_out(self):
        self.fading = True
        self.fade_start_time = pygame.time.get_ticks()
        self.speaking = False
        self.character_image = self.image_closed  
        self.update_image()

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