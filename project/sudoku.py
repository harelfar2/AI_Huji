from board import Board
from functools import reduce
import numpy as np

from util import EMPTY_VALUE, Action, grid_to_string
import time
from datetime import datetime
from solvers import StupidSolver, BackTrackingSolver


class Sudoku:

    def __init__(self, filename, solver_type = 'stupid', display_enabled = True, print = False):
        self.__grid, self.__read_only_tiles = self.__parse_file(filename)
        if solver_type == 'stupid':
            self.__solver = StupidSolver(self)
        if solver_type == 'backtracking':
            self.__solver = BackTrackingSolver(self)

        self.__print_enabled = print
        self.__display_enabled = display_enabled
        if display_enabled:
            self.__board = Board(self.__grid)

    def play(self):
        start = time.time()
        actions_queue = self.__solver.solve()
        end = time.time()

        total = end - start
        print("got solution after", total, "seconds", flush=True)

        if self.__display_enabled:

            action_counter = 0
            quit_game = False

            while actions_queue:
                action = actions_queue.popleft()
                if action.id == Action.INSERT:
                    self.__insert(action.x, action.y, action.value)
                elif action.id == Action.DELETE:
                    self.__delete(action.x, action.y)
                elif action.id == Action.QUIT:
                    quit_game = True
                    break

                if not self.__display_enabled and self.__print_enabled:
                    print("\n", self)
                action_counter += 1
        else:
            action_counter = len(actions_queue)
            quit_game = not self.__solver.is_solved
            print(grid_to_string(self.__solver.grid))

        if not quit_game:
            print("solved with", action_counter, "action" + ["s", ""][action_counter == 1])
        else:
            print("quit after", action_counter, "action" + ["s", ""][action_counter == 1])

        time.sleep(5)

    def __insert(self, x, y, value):
        """
        puts value in the grid at tile (x,y)
        """
        self.__grid[y][x] = value
        if self.__display_enabled:
            self.__board.insert(y, x, value)

    def __delete(self, x, y):
        """
        deletes the value in the grid at tile (x,y)
        """
        self.__grid[y][x] = EMPTY_VALUE
        if self.__display_enabled:
            self.__board.insert(y, x, EMPTY_VALUE)

    @staticmethod
    def get_row(grid, x):
        """
        returns a list representing the row of tile (x,y) in the grid
        """
        row = grid[x, :]
        return np.delete(row, np.where(row == EMPTY_VALUE))

    @staticmethod
    def get_column(grid, y):
        """
        returns a list representing the column of tile (x,y) in the grid
        """
        col = grid[:, y]
        return np.delete(col, np.where(col == EMPTY_VALUE))

    @staticmethod
    def get_block(grid, x, y):
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

        block = grid[s_y, s_x].reshape(9)
        return np.delete(block, np.where(block == EMPTY_VALUE))

    @staticmethod
    def get_first_empty_cell(grid, read_only, x_start = 0, y_start = 0):
        for y in range(y_start, 9):
            for x in range(x_start, 9):
                if grid[y][x] == EMPTY_VALUE and (x, y) not in read_only:
                    return x, y

        for y in range(0, 9):
            for x in range(0, 9):
                if grid[y][x] == EMPTY_VALUE and (x, y) not in read_only:
                    return x, y

        return -1, -1

    @staticmethod
    def get_legal_values(grid, x, y):
        """
        gets all possible legal values in the grid at tile (x,y)
        """
        all_values = [i for i in range(1, 10)]

        row_values = Sudoku.get_row(grid, y)
        col_values = Sudoku.get_column(grid, x)
        block_values = Sudoku.get_block(grid, x, y)

        curr_values = reduce(np.union1d, (row_values, col_values, block_values))
        return np.setdiff1d(all_values, curr_values)

    @staticmethod
    def is_complete(grid):
        if np.any(grid == EMPTY_VALUE):
            return False

        # check rows
        for i in range(9):
            if len(set(Sudoku.get_row(grid, i))) != 9:
                return False

        # check columns
        for i in range(9):
            if len(set(Sudoku.get_column(grid, i))) != 9:
                return False

        # check blocks
        block_indices = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        for y, x in block_indices:
            if len(set(Sudoku.get_block(grid, x, y))) != 9:
                return False

        return True

    def get_grid(self):
        return self.__grid

    def get_read_only(self):
        return self.__read_only_tiles

    @staticmethod
    def __parse_file(filename):
        with open(filename) as f:
            line = f.readlines()[0]
        values = []
        read_only = []
        for index, char in enumerate(line):
            if char == '-':
                char = EMPTY_VALUE
            else:
                col = index % 9
                row = int(index / 9)
                read_only += [(col,row)]
            values += [int(char)]

        return np.array(values).reshape(9,9), read_only

    def __str__(self):
        return grid_to_string(self.__grid)


