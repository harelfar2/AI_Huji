import pygame
import time
import random

SQUARE_SIZE = 40
EMPTY_VALUE = 11

# USER EVENTS ARE BETWEEN 24 AND 32
INSERT_EVENT = 24
DELETE_EVENT = 25


class GameBoard:

    def __init__(self, engine, grid_values):
        pygame.init()
        pygame.display.set_caption('Sudoku')
        self.__engine = engine
        self.grid_values = grid_values
        self.__screen = pygame.display.set_mode((400, 400))
        board = pygame.image.load('board.png')
        self.__screen.blit(board, (10, 10))
        self.tiles = self.create_tiles(10, 10)

        pygame.event.set_blocked(pygame.MOUSEMOTION)

    def create_tiles(self, init_x, init_y):
        tiles = list()
        x = y = 0
        for i in range(0, 9):
            row = list()
            for j in range(0, 9):
                if j in (0, 1, 2):
                    x = (j * 41) + (init_x + 2)
                if j in (3, 4, 5):
                    x = (j * 41) + (init_x + 6)
                if j in (6, 7, 8):
                    x = (j * 41) + (init_x + 10)
                if i in (0, 1, 2):
                    y = (i * 41) + (init_y + 2)
                if i in (3, 4, 5):
                    y = (i * 41) + (init_y + 6)
                if i in (6, 7, 8):
                    y = (i * 41) + (init_y + 10)

                tile = Tile(self.grid_values[i][j], x, y, j, i)
                row.append(tile)

            tiles.append(row)

        self.current_tile = tiles[0][0]
        return tiles

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == INSERT_EVENT:
                    self.grid_values[event.x][event.y] = event.value
                    self.tiles[event.x][event.y].update_value(event.value)
                elif event.type == DELETE_EVENT:
                    self.grid_values[event.x][event.y] = EMPTY_VALUE
                    self.tiles[event.x][event.y].update_value(EMPTY_VALUE)

            pygame.display.update()

            time.sleep(0.0005)

    def insert(self, x_pos, y_pos, new_value):
        pygame.event.post(pygame.event.Event(INSERT_EVENT, x=x_pos, y=y_pos, value=new_value))

    def delete(self, x_pos, y_pos):
        pygame.event.post(pygame.event.Event(DELETE_EVENT, x = x_pos, y = y_pos))

class Tile:
    def __init__(self, value, x, y, grid_x, grid_y):
        self.font_colr = pygame.color.THECOLORS["black"]
        self.value = value
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.read_only = self.value != EMPTY_VALUE

        self.screen  = pygame.display.get_surface()
        self.color_square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE)).convert()
        self.color_square.fill(pygame.color.THECOLORS['white'], None, pygame.BLEND_RGB_ADD)
        self.color_square_rect = self.color_square.get_rect()
        self.color_square_rect = self.color_square_rect.move(x + 1, y + 1)
        self.rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)

        self.draw()

    def draw(self):
        value = ''
        if self.value != EMPTY_VALUE:
            value = self.value

        font = pygame.font.Font('gunny.ttf', 30)
        text = font.render(str(value), 1, self.font_colr)
        textpos = text.get_rect()
        textpos.centerx = self.rect.centerx
        textpos.centery = self.rect.centery
        self.screen.blit(self.color_square, self.color_square_rect)
        self.screen.blit(text, textpos)

    def update_value(self, value):
        self.value = value
        self.draw()


