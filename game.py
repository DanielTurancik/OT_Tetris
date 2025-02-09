import sys
from blocks import *
from grid import Grid
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False
        self.rotate_sound = pygame.mixer.Sound('assets/audio/se_game_rotate.wav')
        self.sound1 = pygame.mixer.Sound('assets/audio/me_game_start2.wav')
        self.landing_sound = pygame.mixer.Sound('assets/audio/se_game_landing.wav')

    def display_score(self, screen):
        font = pygame.font.Font('assets/fonts/font2.TTF', 20)
        score_text = font.render(f'Score: {int(self.score/10)}', True, (255, 255, 255))
        screen.blit(score_text, (427, 10))


    def show_intro_screen(self, screen):
        intro = True
        background = pygame.image.load('assets/background/background2.jpg')
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        font_title = pygame.font.Font('assets/fonts/font2.TTF', 70)
        font_start = pygame.font.Font('assets/fonts/font2.TTF', 18)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        intro = False
                        self.sound1.play()

            screen.blit(background, (0, 0))
            title_text = font_title.render('TETRIS', True, (255, 255, 255))
            screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2,180))

            start_text = font_start.render('Press ENTER to Start', True, (255, 255, 255))
            screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 330))

            pygame.display.update()

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.reset_score()

    def death_info(self, screen):
        game_over_font = pygame.font.Font('assets/fonts/font2.TTF', 30)
        restart_font = pygame.font.Font('assets/fonts/font2.TTF', 13)

        background_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        pygame.draw.rect(screen, (0, 0, 0), background_rect)

        game_over_text = game_over_font.render('GAME OVER', True, (255, 0,0))
        restart_text = restart_font.render('PRESS ENTER TO RESTART', True, (255, 0,0))

        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(restart_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 300))

    def get_random_block(self):
        if len(self.blocks) < 1:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen)
        self.display_score(screen)
        self.draw_next_block(screen)

    def move_left(self):
        self.current_block.move(0,-1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,1)
    def move_right(self):
        self.current_block.move(0,1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,-1)

    def move_down(self):
        self.current_block.move(1,0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1,0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        cleared_rows = self.grid.clear_full_rows()
        self.score += cleared_rows * 1000
        if not self.block_fits():
            self.game_over = True
        self.landing_sound.play()

    def update_score(self, value):
        self.score +=  value

    def reset_score(self):
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.col) == False:
                return False
        return True

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.col) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def draw_next_block(self, screen):
        font = pygame.font.Font('assets/fonts/font2.TTF', 16)
        next_text = font.render('NEXT BLOCK:', True, (255, 255, 255))
        screen.blit(next_text, (430, 250))

        for tile in self.next_block.get_cell_positions():
            tile_rect = pygame.Rect(
                365 + tile.col * self.grid.cell_size,
                300 + tile.row * self.grid.cell_size,
                self.grid.cell_size - 1,
                self.grid.cell_size - 1
            )
            pygame.draw.rect(screen, self.grid.colors[self.next_block.id], tile_rect)