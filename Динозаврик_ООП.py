
import pygame
from pygame.locals import *
import random as rand

pygame.init()
pygame.font.init()

global size
size = 1280, 720
w,h = size

class player(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = 0 + self.rect.size[0]/2, size[1] // 2
        self.dead_timer = 0
        self.speed = [10,6]

class enemy(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.image = pygame.transform.scale(self.image, (100,200))
        self.rect = self.image.get_rect()
        self.rect.left = size[0]
        self.rect.bottom = size[1] - 100
        self.speed = [-10, 0]

    def update(self):
        if self.rect.left < 0:
            self.rect.right = size[0]

class health(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()

class win_object(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.rotozoom(self.image, 0 ,0.5)
        self.image = pygame.transform.scale(self.image, (50,60))
        self.rect = self.image.get_rect()
        self.rect.left = rand.randint(280, 1000)
        self.rect.bottom = rand.randint(220, size[1] - 100)

player_sprite = player('resources/Динозавр_right.png')
cactus_sprite = enemy('resources/Кактус.png')
h1 = health("resources/Сердце.png")
h1.rect.left = 1150
h1.rect.top = 20
h2 = health("resources/Сердце.png")
h2.rect.left = 1070
h2.rect.top = 20
h3 = health("resources/Сердце.png")
h3.rect.left = 990
h3.rect.top = 20
bonus = win_object("resources/Изумруд.png")

screen = pygame.display.set_mode(size)
background = pygame.image.load("resources/Пустыня.jpg")
background = pygame.transform.scale(background, size)
pygame.display.set_caption("Динозавры")

running = True
is_jump = False
score = 0
health_point = 3
win_point = 0

font = pygame.font.SysFont("times new roman", 36)
score_text = font.render(f'Счёт: {score}', True, (180, 0, 0))
win_score_text = font.render(f'Очки: {win_point}', True, (180, 0, 0))
lose_text = font.render("", True, (180, 0, 0))
win_text = font.render("", True, (180, 0, 0))
timer = pygame.time.Clock()

while running:
    timer.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                is_jump = True

    keys = pygame.key.get_pressed()
    if keys[K_SPACE] and is_jump is False:
        player_sprite.rect.y -= 20
        if player_sprite.rect.top < 0:
            is_jump = True
        if keys[K_d] and player_sprite.rect.right < w:
            rect = player_sprite.rect
            player_sprite.rect.x += player_sprite.speed[0]
            player_sprite = player("resources/Динозавр_right.png")
            player_sprite.rect = rect
        elif keys[K_a] and player_sprite.rect.left > 0:
            rect = player_sprite.rect
            player_sprite.rect.x -= player_sprite.speed[0]
            player_sprite = player("resources/Динозавр_left.png")
            player_sprite.rect = rect
    elif keys[K_d] and player_sprite.rect.right < w:
        rect = player_sprite.rect
        player_sprite.rect.x += player_sprite.speed[0]
        player_sprite = player("resources/Динозавр_right.png")
        player_sprite.rect = rect
    elif keys[K_a] and player_sprite.rect.left > 0:
        rect = player_sprite.rect
        player_sprite.rect.x -= player_sprite.speed[0]
        player_sprite = player("resources/Динозавр_left.png")
        player_sprite.rect = rect

    screen.blit(background, (0, 0))
    screen.blit(player_sprite.image, player_sprite.rect)
    screen.blit(cactus_sprite.image, cactus_sprite.rect)
    screen.blit(bonus.image, bonus.rect)
    screen.blit(h1.image, h1.rect)
    if health_point > 1:
        screen.blit(h2.image, h2.rect)
        if health_point > 2:
            screen.blit(h3.image, h3.rect)

    player_sprite.rect = player_sprite.rect.move(0, player_sprite.speed[1])
    cactus_sprite.rect = cactus_sprite.rect.move(cactus_sprite.speed)

    if player_sprite.rect.bottom > size[1] - 100:
        player_sprite.rect.bottom = size[1] - 100
        is_jump = False
    if cactus_sprite.rect.left < 0:
        score += 1
        score_text = font.render(f'Счёт {score}', True, (180,0,0))

    if player_sprite.rect.colliderect(bonus.rect):
        bonus.kill()
        bonus.rect.left = rand.randint(280, 1000)
        bonus.rect.bottom = rand.randint(220, size[1] - 100)
        win_point += 1
        win_score_text = font.render(f'Очки: {win_point}', True, (180, 0, 0))

    if player_sprite.rect.colliderect(cactus_sprite.rect):
        cactus_sprite.kill()
        cactus_sprite.rect.left = size[0]
        cactus_sprite.rect.bottom = size[1] - 100
        if health_point == 3:
            h3.kill()
        elif health_point == 2:
            h2.kill()
        elif health_point == 1:
            h1.kill()
        health_point -= 1

    if win_point == 100:
        screen.blit(background, (0,0))
        win_text = font.render("ПОБЕДА!!!", True, (180, 0, 0))
        running = False
    if health_point == 0:
        screen.blit(background, (0,0))
        lose_text = font.render("ТЫ ПРОИГРАЛ!!!", True, (180, 0, 0))
        running = False

    screen.blit(score_text, (10,20))
    screen.blit(win_score_text, (600,20))
    screen.blit(lose_text, (size[0] / 2 - 150, size[1] / 2))
    screen.blit(win_text, (size[0] / 2 - 80, size[1] / 2))
    pygame.display.update()

    cactus_sprite.update()

pygame.time.delay(2000)
pygame.quit()