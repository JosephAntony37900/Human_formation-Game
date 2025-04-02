import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/weapons/bullet.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (10, 20))
            self.image.set_colorkey((0, 0, 0))
        except pygame.error as e:
            print(f"Error cargando imagen del proyectil: {e}")
            # aqui se usa un rectangulo rojo como marcador temporal
            self.image = pygame.Surface((10, 20))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()