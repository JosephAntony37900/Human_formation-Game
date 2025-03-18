import pygame
from config.Display_settings import DisplaySettings
from entities.Player_model import Player
from entities.Narrador_model import Narrator
from entities.Obstacule_gas import Obstacle  
from inputs.keyboard import get_keys
import random

class Level1:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(DisplaySettings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, 100)
        self.player.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 200)  
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        self.obstacles = pygame.sprite.Group()
        for _ in range(5): 
            obstacle = Obstacle()
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)

        self.narrator = Narrator()
        self.all_sprites.add(self.narrator)

        try:
            self.background = pygame.image.load("assets/backgrounds/scene_base_HD.png")
            info = pygame.display.Info()
            self.background = pygame.transform.scale(self.background, (info.current_w, info.current_h))
        except pygame.error as e:
            print(f"Error cargando la imagen de fondo: {e}")
            self.background = None

        self.background_y = 0
        self.texts = ["¡Prepárate para la batalla!", "¡El enemigo se acerca!", "¡Lucha valientemente, soldado!"]
        self.current_text_index = 0
        self.max_texts = 2
        self.click_count = 0
        self.time_after_last_message = None
        self.fade_wait_time = 3000
        self.fade_started = False
        self.min_allowed_y = self.player.rect.y
        self.max_allowed_y = 800
        self.min_allowed_x = 40
        self.max_allowed_x = pygame.display.Info().current_w - 40

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.check_collisions()  
            self.draw()
            self.clock.tick(DisplaySettings.FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.click_count < self.max_texts:
                    self.change_text()
                    self.click_count += 1

    def update(self):
        keys = get_keys()
        if keys[pygame.K_LEFT]:
            if self.player.rect.left > self.min_allowed_x:
                self.player.rect.x -= self.player.speed
        if keys[pygame.K_RIGHT]:
            if self.player.rect.right < self.max_allowed_x:
                self.player.rect.x += self.player.speed
        min_player_y = 300
        max_player_y = self.max_allowed_y
        if keys[pygame.K_UP]:
            if self.player.rect.top > min_player_y:
                self.player.rect.y -= self.player.speed
            else:
                self.background_y += self.player.speed * 0.5
                if self.player.rect.y < self.min_allowed_y:
                    self.min_allowed_y = self.player.rect.y
        if keys[pygame.K_DOWN]:
            if self.player.rect.bottom + self.player.speed <= max_player_y:
                self.player.rect.y += self.player.speed
            else:
                self.player.rect.bottom = max_player_y

        if self.click_count <= self.max_texts:
            self.narrator.update(self.texts[self.current_text_index])
        if self.click_count >= self.max_texts and self.time_after_last_message is None:
            self.time_after_last_message = pygame.time.get_ticks()
        if self.time_after_last_message is not None and pygame.time.get_ticks() - self.time_after_last_message >= self.fade_wait_time:
            if not self.fade_started:
                self.narrator.start_fade_out()
                self.fade_started = True
        if self.fade_started:
            self.narrator.update_fade()

        self.move_obstacles()

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.rect.y += 5
            if obstacle.rect.y > self.screen.get_height():
                obstacle.rect.y = -50
                obstacle.rect.x = random.randint(100, pygame.display.Info().current_w - 100)

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over()

    def game_over(self):
        print("Game Over!")
        self.running = False

    def draw(self):
        if self.background:
            bg_height = self.background.get_height()
            offset = self.background_y % bg_height
            self.screen.blit(self.background, (0, offset - bg_height))
            self.screen.blit(self.background, (0, offset))
        else:
            self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def change_text(self):
        if self.current_text_index < len(self.texts) - 1:
            self.current_text_index += 1
            self.narrator.update(self.texts[self.current_text_index])
        else:
            self.time_after_last_message = pygame.time.get_ticks()
