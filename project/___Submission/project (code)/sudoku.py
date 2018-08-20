from board import Board
from functools import reduce
import numpy as np

from util import EMPTY_VALUE, Action, grid_to_string
import time
from solvers import BackTrackingSolver, CSPSolver, SimulatedAnnealingSolver, ArcConsistencySolver, ForwardCheckingSolver


class SolverType:
    BACKTRACKING = 'Backtracking'
    CSP = 'CSP heuristics'
    SIMULATED_ANNEALING = 'Simulated Annealing'
    ARC_CONSISTENCY = 'Arc-Consistency'
    FORWARD_CHECKING = 'Forward Checking'


class Sudoku:
    BLOCK_INDEXES = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

    def __init__(self, filename, solver_type ='backtracking', display_enabled = False, print = False):
        self.__file_name = filename
        self.__grid, self.__read_only_tiles = self.__parse_file(filename)
        self.__solver_type = solver_type

        if solver_type == SolverType.BACKTRACKING:
            self.__solver = BackTrackingSolver(self)
        elif solver_type == SolverType.CSP:
            self.__solver = CSPSolver(self)
        elif solver_type == SolverType.SIMULATED_ANNEALING:
            self.__solver = SimulatedAnnealingSolver(self)
        elif solver_type == SolverType.ARC_CONSISTENCY:
            self.__solver = ArcConsistencySolver(self)
        elif solver_type == SolverType.FORWARD_CHECKING:
            self.__solver = ForwardCheckingSolver(self)
        self.__print_enabled = print
        self.__display_enabled = display_enabled
        if display_enabled:
            self.__board = Board(self.__grid)

    def play(self):

        if self.__print_enabled:
            print(self.__solver_type, "attempting to solve")
            print((grid_to_string(self.__grid)))

        start = time.time()
        actions_queue = self.__solver.solve()
        end = time.time()

        total = end - start

        if not self.__solver.is_solved or not self.is_complete(self.__solver.grid):
            if actions_queue:
                action_counter = len(actions_queue)
            else:
                action_counter = 0
                print(self.__solver_type, "could not find solution. quit after",
                      round(total, 3), "seconds and", action_counter, "actions")

            return total, action_counter, False

        print(self.__solver_type, "got solution after", round(total, 3), "seconds and",
              str(len(actions_queue)), "actions", flush=True)

        if self.__display_enabled:
            action_counter = 0

            while actions_queue:
                action = actions_queue.popleft()
                if action.id == Action.INSERT:
                    self.__insert(action.x, action.y, action.value)
                elif action.id == Action.DELETE:
                    self.__delete(action.x, action.y)

                action_counter += 1

            time.sleep(10)
        else:
            action_counter = len(actions_queue)

        if self.__print_enabled:
            print(grid_to_string(self.__solver.grid))

        return total, action_counter, True

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
    def get_row(grid, y):
        """
        returns a list representing the row of tile (x,y) in the grid
        """
        row = grid[y, :]
        return np.delete(row, np.where(row == EMPTY_VALUE))

    @staticmethod
    def get_column(grid, x):
        """
        returns a list representing the column of tile (x,y) in the grid
        """
        col = grid[:, x]
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
    def get_first_empty_cell(grid, read_only, y_start = 0):

        for y in range(y_start, 9):
            for x in range(0, 9):
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
    def get_neighbors(x, y):
        '''
        :param x:
        :param y:
        :return: list of indexes of neighbors of (x,y)
        '''
        row = [(j, y) for j in range(0, 9)]
        col = [(x, i) for i in range(0, 9)]

        if 0 <= x < 3:
            s_x = range(0, 3)
        elif 3 <= x < 6:
            s_x = range(3, 6)
        else:
            s_x = range(6, 9)

        if 0 <= y < 3:
            s_y = range(0, 3)
        elif 3 <= y < 6:
            s_y = range(3, 6)
        else:
            s_y = range(6, 9)
        block = []
        for i in s_x:
            for j in s_y:
                block.append((i, j))

        return row + col + block

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

    @staticmethod
    def get_block_start_indexes(x, y):
        return x // 3 * 3, y // 3 * 3

    @staticmethod
    def get_block_indexes(x,y):
        indexes = []
        x_start, y_start = Sudoku.get_block_start_indexes(x, y)
        for y_offset in range(3):
            for x_offset in range(3):
                if x != x_start + x_offset or y != y_start + y_offset:
                    indexes += [(x_start + x_offset, y_start + y_offset)]

        return np.array(indexes)

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

    @staticmethod
    def get_neighbors_indexes(x, y):
        neighbors = []
        for i in range(9):  # row and col
            if i != y:
                neighbors.append((x, i))
            if i != x:
                neighbors.append((i, y))

        # block
        for neighbor in Sudoku.get_block_indexes(x, y):
            neighbors.append(tuple(neighbor))

        return neighbors

    def get_grid(self):
        return self.__grid

    def get_read_only(self):
        return self.__read_only_tiles

    def set_grid(self, grid):
        self.__grid = grid.copy()

    def __str__(self):
        return grid_to_string(self.__grid)


