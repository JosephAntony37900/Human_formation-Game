#entities/Enemy_leucocito.py
import pygame
import random
import os

class EnemyLeucocito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # cargar las imagenes para la animacion del leucocito
        self.frames = self.load_frames("assets/enemies/leucocito/")
        print(f"Cargados {len(self.frames)} frames para el enemigo 'leucocito'")
        
        if len(self.frames) <= 1:
            print("Solo se carga 1 frame, no hay animacion revisa tu code chavo")
        
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (80, 80))  # se ajusta el tamaño si es necesario
        self.image = self.image.convert_alpha()
        
        # hacemos el fondo transparente (el fondo de la imagen que esta es negro)
        background_color = (0, 0, 0)  
        self.image.set_colorkey(background_color)
        print(f"Color clave para transparencia: {background_color}")
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, pygame.display.Info().current_w - 100)
        self.rect.y = -50
        self.speed = 3  # la velocidad de caida (mas lento que el gas, ajustable pero puede mejorar, vi un juego que nos puede inspirar)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150  # 150 ms entre frames (~6.67 FPS, ajustable, lo mismo pero mas perfecto)

    def load_frames(self, folder_path):
        """Carga todas las imágenes de una carpeta como frames."""
        frames = []
        try:
            for filename in sorted(os.listdir(folder_path)):  # ordenamos para mantener secuencia limpia
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    img_path = os.path.join(folder_path, filename)
                    frame = pygame.image.load(img_path).convert_alpha()
                    frames.append(frame)
            return frames if frames else [pygame.image.load("assets/enemies/leucocito/leucocito1.png").convert_alpha()]  # Fallback
        except Exception as e:
            print(f"Error cargando frames del leucocito: {e}")
            return [pygame.image.load("assets/enemies/leucocito/leucocito1.png").convert_alpha()]

    def update(self, player, bots):
        # movimiento del enemigo (caida)
        targets = [player] + list(bots)

        closets_target = min(
            targets,
            key = lambda t: (t.rect.centerx - self.rect.centerx) ** 2 + (t.rect.centery - self.rect.centery) ** 2
        )
        
        dx = closets_target.rect.centerx - self.rect.centerx
        dy = closets_target.rect.centery - self.rect.centery

        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)

        self.rect.x += int(self.speed * dx / distance)
        self.rect.y += int(self.speed * dy / distance)
        
        # animacion de los frames con flip horizontal si el objetivo esta a la izquierda
        if len(self.frames) > 1:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                
                frame = self.frames[self.current_frame]
                frame_scaled = pygame.transform.scale(frame, (80, 80))

                # Flip horizontal si el objetivo esta a la izquierda se pude variar pero esta bien optimizado
                if dx < 0:
                    frame_scaled = pygame.transform.flip(frame_scaled, True, False)

                self.image = frame_scaled.convert_alpha()
                self.image.set_colorkey((0, 0, 0))
                self.last_update = current_time
                print(f"Frame actual del leucocito: {self.current_frame}")
