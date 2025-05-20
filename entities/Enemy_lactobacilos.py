import pygame
import random
import os

class Spittle(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.frames = self.load_frames("assets/enemies/lactobacilo/spittle")
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 5
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def load_frames(self, path):
        frames = []
        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):
                img_path = os.path.join(path, filename)
                image = pygame.image.load(img_path).convert_alpha()
                frames.append(pygame.transform.scale(image, (30, 30)))
        return frames

    def update(self, player, bots):
        # Movimiento
        self.rect.x += int(self.speed * self.direction[0])
        self.rect.y += int(self.speed * self.direction[1])

        # Animación
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

        # Si sale de pantalla, elimínalo
        if (self.rect.right < 0 or self.rect.left > pygame.display.Info().current_w or
                self.rect.bottom < 0 or self.rect.top > pygame.display.Info().current_h):
            self.kill()


class EnemyLactobacilo(pygame.sprite.Sprite):
    def __init__(self, spittle_group):
        super().__init__()
        self.moving_frames = self.load_frames("assets/enemies/lactobacilo/moving", (80, 80))
        self.attack_frames = self.load_frames("assets/enemies/lactobacilo/attack", (80, 80))
        self.current_frame = 0
        self.image = self.moving_frames[self.current_frame]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, pygame.display.Info().current_w - 100)
        self.rect.y = -60
        self.speed = 2.5
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150
        self.last_spit = pygame.time.get_ticks()
        self.spit_cooldown = 2000
        self.state = "moving"
        self.spittle_group = spittle_group

    def load_frames(self, folder_path, size):
        frames = []
        try:
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(".png"):
                    img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                    img = pygame.transform.scale(img, size)
                    frames.append(img)
        except Exception as e:
            print(f"Error cargando frames de {folder_path}: {e}")
        return frames or [pygame.Surface((80, 80))]

    def update(self, player, bots):
        # Buscar objetivo
        targets = [player] + list(bots)
        target = min(targets, key=lambda t: (t.rect.centerx - self.rect.centerx) ** 2 + (t.rect.centery - self.rect.centery) ** 2)
        dx, dy = target.rect.centerx - self.rect.centerx, target.rect.centery - self.rect.centery
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        direction = (dx / distance, dy / distance)

        # Movimiento
        self.rect.x += int(self.speed * direction[0])
        self.rect.y += int(self.speed * direction[1])

        # Ataque cada X tiempo
        now = pygame.time.get_ticks()
        if now - self.last_spit > self.spit_cooldown:
            spit = Spittle(self.rect.centerx, self.rect.centery, direction)
            self.spittle_group.add(spit)
            self.last_spit = now
            self.state = "attack"
        else:
            self.state = "moving"

        # Animación
        frames = self.attack_frames if self.state == "attack" else self.moving_frames
        if len(frames) > 1:
            if now - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]
                self.image.set_colorkey((0, 0, 0))
                self.last_update = now
