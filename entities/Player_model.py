import pygame
import os
from entities.Bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_frames("assets/characters/cristobal/")
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (80, 80))
        self.image = self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 8
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.bullets = pygame.sprite.Group()
        self.weapon_active = False
        self.last_shot = 0
        self.shoot_cooldown = 300

        try:
            self.weapon_image = pygame.image.load("assets/weapons/Bullet.png").convert_alpha()
            self.weapon_image = pygame.transform.scale(self.weapon_image, (20, 40))
            self.weapon_image.set_colorkey((0, 0, 0))
        except pygame.error:
            self.weapon_image = pygame.Surface((20, 40))
            self.weapon_image.fill((255, 0, 0))
        self.weapon_rect = self.weapon_image.get_rect()

        self.invincible = False
        self.invincibility_timer = 0
        self.invincibility_duration = 1000

    def load_frames(self, folder_path):
        frames = []
        try:
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    img_path = os.path.join(folder_path, filename)
                    frame = pygame.image.load(img_path).convert_alpha()
                    frames.append(frame)
            return frames if frames else [pygame.image.load("assets/characters/cristobal/cristobal1.png").convert_alpha()]
        except Exception:
            return [pygame.image.load("assets/characters/cristobal/cristobal1.png").convert_alpha()]

    def update(self, keys, min_allowed_x, max_allowed_x, min_allowed_y, max_allowed_y, level):
        screen_width = pygame.display.Info().current_w
        middle_third_start = screen_width // 8  #aqui ya funcionan los limites del player
        middle_third_end = (screen_width * 7) // 8 #,,
        
        restricted_min_x = middle_third_start
        restricted_max_x = middle_third_end - self.rect.width
        
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.left < restricted_min_x:
                self.rect.left = restricted_min_x

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.rect.right > restricted_max_x + self.rect.width:
                self.rect.right = restricted_max_x + self.rect.width

        if keys[pygame.K_w]:
            if self.rect.top > min_allowed_y:
                self.rect.y -= self.speed
            else:
                level.background_y += self.speed * 0.5
                if self.rect.y < level.min_allowed_y:
                    level.min_allowed_y = self.rect.y
            if self.rect.top < min_allowed_y:
                self.rect.top = min_allowed_y

        if keys[pygame.K_s]:
            self.rect.y += self.speed
            if self.rect.bottom > max_allowed_y:
                self.rect.bottom = max_allowed_y

        if keys[pygame.K_e]:
            self.weapon_active = not self.weapon_active

        current_time = pygame.time.get_ticks()
        if self.weapon_active and keys[pygame.K_SPACE] and (current_time - self.last_shot >= self.shoot_cooldown):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            level.all_sprites.add(bullet)
            self.last_shot = current_time

        if self.weapon_active:
            self.weapon_rect.bottomleft = (self.rect.right, self.rect.centery)

        if self.invincible:
            if current_time - self.invincibility_timer >= self.invincibility_duration:
                self.invincible = False

        if len(self.frames) > 1:
            if current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.current_frame], (80, 80))
                self.image = self.image.convert_alpha()
                self.image.set_colorkey((0, 0, 0))
                self.last_update = current_time

    def draw_weapon(self, screen):
        if self.weapon_active:
            screen.blit(self.weapon_image, self.weapon_rect)

    def take_damage(self, damage):
        if not self.invincible:
            self.invincible = True
            self.invincibility_timer = pygame.time.get_ticks()
            return True
        return False