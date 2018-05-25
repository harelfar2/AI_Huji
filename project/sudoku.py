from board import Board
from functools import reduce
import numpy as np
import sys
from util import EMPTY_VALUE, Action
import time
from solvers import StupidSolver


class Sudoku:

    def __init__(self, filename, display_enabled = True, print = False, solver = StupidSolver()):
        grid, read_only_tiles = self.__parse_file(filename)
        self.__grid = grid
        self.__read_only_tiles = read_only_tiles

        for tile in read_only_tiles:
            solver.add_read_only_tile(tile)

        self.__solver = solver

        self.__print_enabled = print
        self.__display_enabled = display_enabled
        if display_enabled:
            self.__board = Board(grid)

    def insert(self, x, y, value):
        """
        puts value in the grid at tile (x,y)
        """
        self.__grid[y][x] = value
        if self.__display_enabled:
            self.__board.insert(x, y, value)

    def delete(self, x, y):
        """
        deletes the value in the grid at tile (x,y)
        """
        self.__grid[y][x] = EMPTY_VALUE
        if self.__display_enabled:
            self.__board.insert(x, y, EMPTY_VALUE)

    def get_row(self, x):
        """
        returns a list representing the row of tile (x,y) in the grid
        """
        row = self.__grid[x, :]
        return np.delete(row, np.where(row == EMPTY_VALUE))

    def get_column(self, y):
        """
        returns a list representing the column of tile (x,y) in the grid
        """
        col = self.__grid[:, y]
        return np.delete(col, np.where(col == EMPTY_VALUE))

    def get_block(self, x, y):
        """
        returns a list representing the 3x3 block of tile (x,y) in the grid
        """
        if 0 <= x < 3:
            s_x = slice(0, 3)
        elif 3 <= x < 6:
            s_x = slice(3, 6)
        else:
            s_x = slice(6, 9)

        if 0 <= y < 3:
            s_y = slice(0, 3)
        elif 3 <= y < 6:
            s_y = slice(3, 6)
        else:
            s_y = slice(6, 9)

        block = self.__grid[s_y, s_x].reshape(9)
        return np.delete(block, np.where(block == EMPTY_VALUE))


    def get_legal_values(self, x, y):
        """
        gets all possible legal values in the grid at tile (x,y)
        """
        all_values = [i for i in range(1,10)]

        row_values = self.get_row(x)
        col_values = self.get_column(x)
        block_values = self.get_block(x, y)

        curr_values = reduce(np.union1d, (row_values, col_values, block_values))
        return np.setdiff1d(all_values, curr_values)

    def get_grid(self):
        return self.__grid

    def play(self):
        while not self.is_complete():
            action = self.__solver.get_action(self)
            if action.id == Action.INSERT:
                self.insert(action.x, action.y, action.value)
            elif action.id == Action.DELETE:
                self.delete(action.x, action.y)
            elif action.id == Action.QUIT:
                self.quit()
                return

            if not self.__display_enabled:
                time.sleep(0.005)
                if(self.__print_enabled):
                    print("\n",self)


    def is_complete(self):
        return False

    def quit(self):
        print("STUCK")

    def __parse_file(self, filename):
        with open(filename) as f:
            line = f.readlines()[0]
        # you may also want to remove whitespace characters like `\n` at the end of each line

        values = []
        read_only = [(i, i) for i in range(9)]
        for index, char in enumerate(line):
            if char == '-':
                char = EMPTY_VALUE
            values += [int(char)]

        return np.array(values).reshape(9,9), read_only

    def __str__(self):
        string = ""
        for i in range(9):
            if i in [3, 6]:
                string += '------+-------+------\n'
            for j in range(9):
                if j in [3, 6]:
                    string += '|'
                string += str(self.__grid[i][j])
            string += "\n"

        return string


