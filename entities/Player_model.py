#entities/Player_model.py
import pygame
import os
from entities.Bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_frames("assets/characters/cristobal/")
        self.rest_frames = self.load_frames("assets/characters/cristobal/rest/")
        self.shoot_frames = self.load_frames("assets/characters/cristobal/rest_shoot/")  
        self.w_blocked = False 
        self.block_timer = 0
        self.block_duration = 500  # milisegundos (2 segundos)
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (100, 100))
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
        self.is_resting = False
        self.invincible = False
        self.invincibility_timer = 0
        self.invincibility_duration = 1000
        self.original_speed = self.speed
        self.slowed = False
        self.slow_timer = 0
        self.slow_duration = 3000
        self.shooting = False
        self.shoot_frame_index = 0
        self.shoot_animation_timer = 0
        self.shoot_animation_speed = 40
        self.shoot_sound = pygame.mixer.Sound("assets/music/shot_sound.mp3")

        self.damage_effect = False
        self.damage_effect_timer = 0
        self.damage_effect_duration = 300


    def load_frames(self, folder_path):
        frames = []
        try:
            for filename in sorted(os.listdir(folder_path), key=lambda f: int(''.join(filter(str.isdigit, f))) if any(char.isdigit() for char in f) else 9999):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    img_path = os.path.join(folder_path, filename)
                    frame = pygame.image.load(img_path).convert_alpha()
                    frames.append(frame)
            if not frames:
                fallback = "assets/characters/cristobal/spermanauta (0).png" if "rest" not in folder_path else "assets/characters/cristobal/rest/rest(0).png"
                frames = [pygame.image.load(fallback).convert_alpha()]
        except Exception as e:
            fallback = "assets/characters/cristobal/spermanauta (0).png" if "rest" not in folder_path else "assets/characters/cristobal/rest/rest(0).png"
            frames = [pygame.image.load(fallback).convert_alpha()]
        return frames

    def update(self, keys, min_allowed_x, max_allowed_x, min_allowed_y, max_allowed_y, level):
        screen_width = pygame.display.Info().current_w
        middle_third_start = screen_width // 8
        middle_third_end = (screen_width * 7) // 8
        background_is_moving = False
        restricted_min_x = middle_third_start
        restricted_max_x = middle_third_end - self.rect.width
        moving = False

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.left < restricted_min_x:
                self.rect.left = restricted_min_x
            moving = True

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.rect.right > restricted_max_x + self.rect.width:
                self.rect.right = restricted_max_x + self.rect.width
            moving = True
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not self.w_blocked:
            if not self.w_blocked:
                if self.rect.top > min_allowed_y:
                   self.rect.y -= self.speed
                else:
                    background_is_moving = True
                    level.background_y += 4
                    self.rect.y -= self.speed
                    if self.rect.y < level.min_allowed_y:
                       level.min_allowed_y = self.rect.y
                if self.rect.top < min_allowed_y:
                   self.rect.top = min_allowed_y
                moving = True
        elif keys[pygame.K_w] and self.w_blocked:
            print("¡Tecla W bloqueada!")
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            if self.rect.bottom > max_allowed_y:
                self.rect.bottom = max_allowed_y
            moving = True
        if keys[pygame.K_e]:
            self.weapon_active = not self.weapon_active

        current_time = pygame.time.get_ticks()

        if self.weapon_active and keys[pygame.K_SPACE] and (current_time - self.last_shot >= self.shoot_cooldown):
            self.shoot_sound.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            level.all_sprites.add(bullet)
            self.last_shot = current_time
            self.shooting = True
            self.shoot_frame_index = 0
            self.shoot_animation_timer = current_time

        if self.invincible and current_time - self.invincibility_timer >= self.invincibility_duration:
            self.invincible = False

        if not moving:
            if not self.is_resting:
                self.current_frame = 0
                self.last_update = current_time
                self.is_resting = True

            if self.weapon_active and self.shooting:
                if current_time - self.shoot_animation_timer >= self.shoot_animation_speed:
                    self.shoot_frame_index += 1
                    self.shoot_animation_timer = current_time
                    if self.shoot_frame_index >= len(self.shoot_frames):
                        self.shoot_frame_index = 0
                        self.shooting = False

                self.image = pygame.transform.scale(self.shoot_frames[self.shoot_frame_index], (100, 100))
            elif self.weapon_active:
                self.image = pygame.transform.scale(self.shoot_frames[0], (100, 100))
            else:
                self.image = pygame.transform.scale(self.rest_frames[self.current_frame], (100, 100))

            self.image.set_colorkey((0, 0, 0))
        else:
            if self.is_resting:
                self.frames = self.load_frames("assets/characters/cristobal/")
                self.current_frame = 0
                self.last_update = current_time
                self.is_resting = False

            if len(self.frames) > 1 and current_time - self.last_update >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.current_frame], (100, 100))
                self.image = self.image.convert_alpha()
                self.image.set_colorkey((0, 0, 0))
                self.last_update = current_time
        
        self.check_slow_status(level)
        if self.w_blocked and pygame.time.get_ticks() - self.block_timer >= self.block_duration: 
            self.w_blocked = False

        return background_is_moving

    def take_damage(self, damage):
        if not self.invincible:
            self.invincible = True
            self.invincibility_timer = pygame.time.get_ticks()
            self.damage_effect = True
            self.damage_effect_timer = pygame.time.get_ticks()
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)

        if self.damage_effect:
            current_time = pygame.time.get_ticks()
            if current_time - self.damage_effect_timer < self.damage_effect_duration:
                red_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 100))
                screen.blit(red_overlay, (0,0))
            else:
                self.damage_effect = False

    def reset(self, x, y):
        self.rect.topleft = (x, y)
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.weapon_active = False
        self.last_shot = 0
        self.invincible = False
        self.invincibility_timer = 0
        self.bullets.empty()
        self.shooting = False

    def slow_down(self, level):
        if not self.slowed:
           self.speed = 1
           self.rect.y -= self.speed
        if level:
            level.background_speed = 1
        self.slowed = True
        self.slow_timer = pygame.time.get_ticks()

            
    def check_slow_status(self, level):
        if self.slowed:
           current_time = pygame.time.get_ticks()
           if current_time - self.slow_timer >= 2000:
              self.speed = self.original_speed
              if level:
                 level.background_speed = level.original_background_speed
              self.slowed = False

    def get_slowed(self):
        if not self.slowed:
            self.slowed = True
            self.speed *= 0.5

    def remove_slowed(self):
        if self.slowed:
            self.slowed = False
            self.speed *= 2
