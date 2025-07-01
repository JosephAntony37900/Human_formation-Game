class Button:
    def __init__(self, text, pos, size=(100, 40), font_size=24):
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.image = self.font.render(text, True, (0, 0, 0))
        self.rect = pygame.Rect(pos, size)
        self.bg_color = (255, 255, 255)
        self.hover_color = (200, 200, 200)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
