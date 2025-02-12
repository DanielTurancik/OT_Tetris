import sys
import pygame
from game import Game
from block import *
pygame.init()

background_color =  [0, 0, 0]


screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Tetris")
game = Game(screen)
clock = pygame.time.Clock()
temp = 0
game.show_intro_screen(screen)


initial_speed = 500
min_speed = 160
speed_reduction = 20
speedup_interval = 5000 # 5 sekúnd

GAME_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_UPDATE, initial_speed)

SPEED_UP = pygame.USEREVENT + 2
pygame.time.set_timer(SPEED_UP, speedup_interval)

current_speed = initial_speed


while True:
    if int(temp) % 2 == 1:
        game.update_score(1)
    else:
        temp += 0.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True and event.key == pygame.K_RETURN:
                game.game_over = False
                game.reset()
                current_speed = initial_speed
                pygame.time.set_timer(GAME_UPDATE, current_speed)
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
        if event.type == SPEED_UP and not game.game_over:
            if current_speed > min_speed:
                current_speed -= speed_reduction
                pygame.time.set_timer(GAME_UPDATE, current_speed)
                print(current_speed)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not game.game_over:
        game.move_down_continuous()

    screen.fill(background_color)
    game.draw(screen)
    if game.game_over:
        game.death_info(screen)


    pygame.display.update()
    clock.tick(60)
