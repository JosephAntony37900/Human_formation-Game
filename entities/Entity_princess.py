import pygame
import os

class PrincessMononoke(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = self.load_frames("assets/characters/america/")
        print(f"Cargados {len(self.frames)} frames para el enemigo 'leucocito'")
        
        if len(self.frames) <= 1:
            print("Solo se carga 1 frame, no hay animacion revisa tu code chavo")
        
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (150, 150))
        self.image = self.image.convert_alpha()
        
        # hacemos el fondo transparente (el fondo de la imagen que esta es negro)
        background_color = (0, 0, 0)  
        self.image.set_colorkey(background_color)
        print(f"Color clave para transparencia: {background_color}")

        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = -50
        self.speed = 3
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150
    
    def load_frames(self, folder_path):
        frames = []
        try:
            for filename in sorted(os.listdir(folder_path), key=lambda f: int(''.join(filter(str.isdigit, f))) if any(char.isdigit() for char in f) else 9999):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    img_path = os.path.join(folder_path, filename)
                    frame = pygame.image.load(img_path).convert_alpha()
                    frames.append(frame)
            if not frames:
                fallback = "assets/characters/america/america (1).png" if "rest" not in folder_path else "assets/characters/america/america (1).png"
                frames = [pygame.image.load(fallback).convert_alpha()]
        except Exception as e:
            fallback = "assets/characters/america/america (1).png" if "rest" not in folder_path else "assets/characters/america/america (1).png"
            frames = [pygame.image.load(fallback).convert_alpha()]
        return frames
    
    def update(self):
        self.rect.y += self.speed
        if len(self.frames) > 1:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.current_frame], (150, 150))
                self.image = self.image.convert_alpha()
                self.image.set_colorkey((0, 0, 0))
                self.last_update = current_time
                print(f"Frame actual del leucocito: {self.current_frame}")