import pygame
import os

class ObstaculeVelocity(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.frames = self.load_frames("assets/obstacles/velocity/")
        print(f"Cargados {len(self.frames)} frames para las ondas del tracto reproductor")

        if len(self.frames) <= 1:
            print("Sin animación, objeto estático")

        self.direction = direction
        
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (200, 200))
        self.image = self.rotate_sprite(self.image, self.direction)
        self.image = self.image.convert_alpha()

        background_color = (255, 255, 255)
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.boost = 12

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150
    
    def load_frames(self, folder_path):
        frames = []
        try:
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith("png") or filename.endswith("jpg"):
                    img_path = os.path.join(folder_path, filename)
                    frame = pygame.image.load(img_path).convert_alpha()
                    frames.append(frame)
            return frames if frames else [pygame.image.load("assets/obstacles/velocity/onda (0).png")]
        except Exception as e:
            print("Error al cargar onda: {e}")
            return [pygame.image.load("assets/obstacles/velocity/onda (0).png")]
    
    def update(self):
        self.rect.y += 5

        if len(self.frames) > 1:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)

                frame = pygame.transform.scale(self.frames[self.current_frame], (200, 200))
                frame = self.rotate_sprite(frame, self.direction)
                frame.set_colorkey((255, 255, 255))
                self.image = frame

                self.last_update = current_time
                print(f"Frame actual del obstáculo: {self.current_frame}")
    
    def impulse(self, rect_obj):
        if self.direction == "UP":
            rect_obj.y -= self.boost
        elif self.direction == "LEFT":
            rect_obj.x -= self.boost
        elif self.direction == "RIGHT":
            rect_obj.x += self.boost
        elif self.direction == "DOWN":
            rect_obj.y += self.boost
        return rect_obj
    
    def rotate_sprite(self, image, direction):
        if direction == "UP":
            return image
        elif direction == "RIGHT":
            return pygame.transform.rotate(image, -90)
        elif direction == "DOWN":
            return pygame.transform.rotate(image, 180)
        elif direction == "LEFT":
            return pygame.transform.rotate(image, 90)
        return image