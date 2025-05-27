#entities/Obstacle_moco.py
import pygame
import random
import os

class Moco(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_frames("assets/obstacles/moco/") 
        print(f"Cargados {len(self.frames)} frames para el obstáculo 'moco'")

        if len(self.frames) <= 1:
            print("Advertencia: Solo se cargó 1 frame, no habrá animación")

        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (65, 65))
        self.image = self.image.convert_alpha()
        background_color = (255, 255, 255)  
        self.image.set_colorkey(background_color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150

    def load_frames(self, folder_path):
        frames = []
        try:
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(".png") or filename.endswith(".jpg"): 
                    img_path = os.path.join(folder_path, filename)
                    frame = pygame.image.load(img_path).convert_alpha()
                    frames.append(frame)
            return frames if frames else [pygame.image.load("assets/obstacles/moco/moco.png").convert_alpha()]
        except Exception as e:
            print(f"Error cargando frames del moco: {e}")
            return [pygame.image.load("assets/obstacles/moco/moco.png").convert_alpha()]

    def update(self):
        self.rect.y += self.speed
        if len(self.frames) > 1: 
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.current_frame], (65, 65))  
                self.image = self.image.convert_alpha()
                self.image.set_colorkey((255, 255, 255))
                self.last_update = current_time
