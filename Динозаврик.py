import pygame
from pygame.locals import *
import random as rand

size = 1280, 720
w,h = size

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(size)
background = pygame.image.load("resources/Пустыня.jpg ")
background = pygame.transform.scale(background, size)
pygame.display.set_caption("Динозавры")
running = True

player_sprite = pygame.image.load("resources/Динозавр_right.png")
player_sprite = pygame.transform.rotozoom(player_sprite, 0, 0.5)
player_rect = player_sprite.get_rect()
player_rect.center = 0 + player_rect.size[0] / 2, size[1] // 2

speed = [0,6]

cactus_size = (100,200)
cactus = pygame.image.load("resources/Кактус.png")
cactus = pygame.transform.rotozoom(cactus, 0, 0.5)
cactus = pygame.transform.scale(cactus, cactus_size )
cactus_rect = cactus.get_rect()
cactus_rect.left = size[0]
cactus_rect.bottom = size[1] - 100
cactus_speed = [-10, 0]

bonus_size = (50,60)
bonus = pygame.image.load("resources/Изумруд.png")
bonus = pygame.transform.rotozoom(bonus, 0, 0.5)
bonus = pygame.transform.scale(bonus, bonus_size)
bonus_rect = bonus.get_rect()
bonus_rect.left = rand.randint(280, 1000)
bonus_rect.bottom = rand.randint(220, size[1] - 100)

health_size = (80, 80)
health = pygame.image.load('resources/Сердце.png')
health = pygame.transform.rotozoom(health, 0, 0.5)
health = pygame.transform.scale(health, health_size)
health_rect = health.get_rect()
health_rect.left = 1150
health_rect.top = 20

health1 = pygame.image.load('resources/Сердце.png')
health1 = pygame.transform.rotozoom(health, 0, 0.5)
health1 = pygame.transform.scale(health1, health_size)
health1_rect = health.get_rect()
health1_rect.left = 1070
health1_rect.top = 20

health2 = pygame.image.load('resources/Сердце.png')
health2 = pygame.transform.rotozoom(health, 0, 0.5)
health2 = pygame.transform.scale(health2, health_size)
health2_rect = health.get_rect()
health2_rect.left = 990
health2_rect.top = 20


timer = pygame.time.Clock()

is_jump = False
is_cactus_alive = True
score = 0
bonus_score = 0
health_point = 3
score_font = pygame.font.SysFont("arial", 36)
score_text = score_font.render(f'Счёт {score}', True, (180, 0, 0))
lose_text = score_font.render('', True,(180,0,0))
bonus_text = score_font.render(f'Очки {bonus_score}',True,(180,0,0))
win_text = score_font.render('', True, (180,0,0))

while running:
    timer.tick(60)

    if is_cactus_alive is False:
        cactus = pygame.image.load("resources/Кактус.png")
        cactus = pygame.transform.rotozoom(cactus, 0, 0.5)
        cactus = pygame.transform.scale(cactus, cactus_size)
        cactus_rect = cactus.get_rect()
        cactus_rect.left = size[0]
        cactus_rect.bottom = size[1] - 100
        is_cactus_alive = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                is_jump = True

    keys = pygame.key.get_pressed()
    if keys[K_SPACE] and is_jump is False:
        player_rect.y -= 20
        if player_rect.top < 0:
            is_jump = True
        if keys[K_d] and player_rect.right < w:
            player_rect.x += 10
            player_sprite = pygame.image.load("resources/Динозавр_right.png")
            player_sprite = pygame.transform.rotozoom(player_sprite, 0, 0.5)
        elif keys[K_a] and player_rect.left > 0:
            player_rect.x -= 10
            player_sprite = pygame.image.load("resources/Динозавр_left.png")
            player_sprite = pygame.transform.rotozoom(player_sprite, 0, 0.5)

    elif keys[K_d] and player_rect.right < w:
        player_rect.x += 10
        player_sprite = pygame.image.load("resources/Динозавр_right.png")
        player_sprite = pygame.transform.rotozoom(player_sprite, 0, 0.5)
    elif keys[K_a] and player_rect.left > 0:
        player_rect.x -= 10
        player_sprite = pygame.image.load("resources/Динозавр_left.png")
        player_sprite = pygame.transform.rotozoom(player_sprite, 0, 0.5)

    screen.blit(background, (0,0))
    screen.blit(player_sprite, player_rect)
    screen.blit(cactus, cactus_rect)
    screen.blit(bonus, bonus_rect)
    screen.blit(health, health_rect)
    if health_point > 1:
        screen.blit(health1, health1_rect)
        if health_point > 2:
            screen.blit(health2, health2_rect)

    cactus_rect = cactus_rect.move(cactus_speed)
    player_rect = player_rect.move(speed)

    if player_rect.bottom > size[1] - 100:
        player_rect.bottom = size[1] - 100
        is_jump = False
    if cactus_rect.left < 0:
        cactus_rect.right = size[0]
        score += 1
        score_text = score_font.render(f'Счёт {score}', True, (180,0,0))

    if player_rect.colliderect(cactus_rect):
        del cactus
        is_cactus_alive = False
        if health_point == 3:
            del health2
        elif health_point == 2:
            del health1
        elif health_point == 1:
            del health
        health_point -= 1

    if player_rect.colliderect(bonus_rect):
        del bonus
        bonus_score +=1
        bonus_text = score_font.render(f'Очки {bonus_score}', True, (180, 0, 0))
        bonus = pygame.image.load("resources/Изумруд.png")
        bonus = pygame.transform.rotozoom(bonus, 0, 0.5)
        bonus = pygame.transform.scale(bonus, bonus_size)
        bonus_rect = bonus.get_rect()
        bonus_rect.left = rand.randint(280, 1000)
        bonus_rect.bottom = rand.randint(220, size[1] - 100)

    if bonus_score == 15:
        screen.blit(background, (0, 0))
        win_text = score_font.render("ПОБЕДА!!!", True, (180, 0, 0))
        running = False
    if health_point == 0:
        screen.blit(background, (0,0))
        lose_text = score_font.render("ТЫ ПРОИГРАЛ!!!", True, (180, 0, 0))
        running = False

    screen.blit(lose_text, (size[0]/2 - 125, size[1]/2))
    screen.blit(score_text, (10,20))
    screen.blit(bonus_text, (600,20))
    screen.blit(win_text,(size[0]/2 - 80, size[1]/2))
    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()