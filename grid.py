import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 14
        self.cell_size = 30
        self.grid = [[0] * self.num_cols for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end=" ")
            print()

    def is_inside(self, row, col):
        if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
            return True
        return False

    def is_empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        return False

    def is_row_full(self, row):
        for col in range(self.num_cols):
            if self.grid[row][col] == 0:
                return False
        return True

    def clear_row(self, row):
        for col in range(self.num_cols):
            self.grid[row][col] = 0


    def move_row_down(self, row, num_rows):
        for col in range(self.num_cols):
            self.grid[row + num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def play_sound(self):
        cleared_row_sound = pygame.mixer.Sound('assets/audio/se_game_tetris.wav')
        cleared_row_sound.play()

    def animate_row_clear(self, screen, row):
        for _ in range(5):
            for col in range(self.num_cols):
                cell_rect = pygame.Rect(col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, (255, 255, 255), cell_rect)
            pygame.display.update()
            pygame.time.delay(50)
            for col in range(self.num_cols):
                cell_rect = pygame.Rect(col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[0], cell_rect)
            pygame.display.update()
            pygame.time.delay(50)

    def animate_column_clear(self, screen, col):
        for _ in range(5):
            for row in range(self.num_rows):
                cell_rect = pygame.Rect(col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1,
                                        self.cell_size - 1)
                pygame.draw.rect(screen, (255, 255, 255), cell_rect)
            pygame.display.update()
            pygame.time.delay(50)
            for row in range(self.num_rows):
                cell_rect = pygame.Rect(col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1,
                                        self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[0], cell_rect)
            pygame.display.update()
            pygame.time.delay(50)

    def clear_full_rows(self, screen):
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.animate_row_clear(screen, row)
                self.clear_row(row)
                completed += 1
                self.play_sound()
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def count_full_rows(self):
        completed = 0
        for row in range(self.num_rows):
            if self.is_row_full(row):
                completed += 1
        return completed

    def draw(self, screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

    def reset(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grid[row][col] = 0