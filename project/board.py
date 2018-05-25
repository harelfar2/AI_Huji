import pygame
import time
import util


class Board:


    def __init__(self, grid_values):
        self.__graphic_grid = grid_values
        pygame.init()
        pygame.display.set_caption('Sudoku')
        self.__screen = pygame.display.set_mode((400, 400))
        board = pygame.image.load('board.png')
        self.__screen.blit(board, (10, 10))

        self.__tiles = self.__create_tiles(10, 10)
        pygame.event.set_blocked(pygame.MOUSEMOTION)

    def __create_tiles(self, init_x, init_y):
        tiles = list()
        x = y = 0
        for row in range(0, 9):
            board_row = list()
            for col in range(0, 9):
                if col in (0, 1, 2):
                    x = (col * 41) + (init_x + 2)
                if col in (3, 4, 5):
                    x = (col * 41) + (init_x + 6)
                if col in (6, 7, 8):
                    x = (col * 41) + (init_x + 10)
                if row in (0, 1, 2):
                    y = (row * 41) + (init_y + 2)
                if row in (3, 4, 5):
                    y = (row * 41) + (init_y + 6)
                if row in (6, 7, 8):
                    y = (row * 41) + (init_y + 10)

                tile = Tile(self.__graphic_grid[row][col], x, y, col, row)
                board_row.append(tile)

            tiles.append(board_row)

        return tiles

    def insert(self, x_pos, y_pos, new_value):
        self.__graphic_grid[y_pos][x_pos] = new_value
        self.__tiles[x_pos][y_pos].update_value(new_value)
        pygame.display.update()
        time.sleep(0.5)



class Tile:

    SQUARE_SIZE = 40
    def __init__(self, value, graphic_x, graphic_y, grid_x, grid_y):
        self.__value = value
        self.__grid_x = grid_x
        self.__grid_y = grid_y
        self.__read_only = self.__value != util.EMPTY_VALUE

        if self.__read_only:
            self.__font_color = pygame.color.THECOLORS["red"]
        else:
            self.__font_color = pygame.color.THECOLORS["black"]

        self.__screen  = pygame.display.get_surface()
        self.__color_square = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE)).convert()
        self.__color_square.fill(pygame.color.THECOLORS['white'], None, pygame.BLEND_RGB_ADD)
        self.__color_square_rect = self.__color_square.get_rect()
        self.__color_square_rect = self.__color_square_rect.move(graphic_x + 1, graphic_y + 1)
        self.__rect = pygame.Rect(graphic_x, graphic_y, self.SQUARE_SIZE, self.SQUARE_SIZE)

        self.__draw()

    def __draw(self):
        value = ''
        if self.__value != util.EMPTY_VALUE:
            value = self.__value

        font = pygame.font.Font('comic_sans.ttf', 30)
        text = font.render(str(value), 1, self.__font_color)
        textpos = text.get_rect()
        textpos.centerx = self.__rect.centerx
        textpos.centery = self.__rect.centery
        self.__screen.blit(self.__color_square, self.__color_square_rect)
        self.__screen.blit(text, textpos)

    def update_value(self, value):
        self.__value = value
        self.__draw()

    def is_read_only(self):
        return self.__read_only

