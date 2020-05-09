import sys

import pygame

from destroy_the_blocks.game import Game
from destroy_the_blocks.game import Menu
from destroy_the_blocks.settings import *

pressed_left = False
pressed_right = False

while True:
    # initializing menu object with settings
    menu = Menu(bg_size, bg_color)

    # initializing game object with settings
    game = Game(bg_size, bg_color, pl_rect, pl_color, pl_speed,
                ball_size, ball_color, ball_speed, block_size,
                block_color, number_of_cols)

    # array of blocks
    blocks = Game.block(game, block_size)

    while Game.menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                Menu.click(menu)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game.menu = False

        Menu.background(menu)
        Menu.button(menu, "rect")
        Menu.button(menu, "text")

        Menu.result(menu)
        Game.lose = False
        Game.win = False
        Game.finish = False

        pygame.display.flip()

        pressed_left = False
        pressed_right = False

    while not Game.finish:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pressed_left = True
                elif event.key == pygame.K_RIGHT:
                    pressed_right = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pressed_left = False
                elif event.key == pygame.K_RIGHT:
                    pressed_right = False

        if pressed_left:
            Game.platform_move(game, False)

        if pressed_right:
            Game.platform_move(game, True)

        Game.background(game)
        Game.platform(game)
        Game.ball(game)
        Game.ball_move(game)
        Game.blocks_logic(game, blocks, block_size, block_color)

        pygame.display.flip()

    Game.menu = True
