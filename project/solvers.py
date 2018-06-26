import abc
from random import randint, shuffle
from util import Action, EMPTY_VALUE
from collections import deque
import sys
import numpy as np


class Solver(object):
    def __init__(self, game):
        super(Solver, self).__init__()
        self.actions_queue = deque()
        self.is_solved = False
        self.game = game
        self.grid = game.get_grid().copy()
        self.read_only_tiles = game.get_read_only().copy()
        self.full_tiles = self.read_only_tiles.copy()

    @abc.abstractmethod
    def solve(self):
        return

    def insert(self, x, y, value):
        if (x, y) in self.read_only_tiles:
            print("READ ONLY TILE ON (", x, y, ") CAN'T INSERT VALUE", value)
            sys.exit()
        self.grid[y][x] = value
        self.full_tiles += [(x, y)]
        self.actions_queue.append((Action(x, y, value)))

    def delete(self, x, y):
        if (x, y) in self.read_only_tiles:
            print("READ ONLY TILE ON (", x, y, ") CAN'T DELETE")
            sys.exit()
        self.grid[y][x] = EMPTY_VALUE
        self.full_tiles.remove((x, y))
        self.actions_queue.append(Action(x, y))

    def quit(self):
        self.actions_queue.append(Action(quit=True))

    def get_value(self, x, y):
        return self.grid[y][x]


class StupidSolver(Solver):
    """
    This solver just puts some random (yet legal values) anywhere he can and when if he gets stuck he quits
    """
    def solve(self):

        stuck = False

        x, y = self.game.get_first_empty_cell(self.grid, self.read_only_tiles)
        while (x, y) is not None:
            legal_values = self.game.get_legal_values(self.grid, x, y)
            if len(legal_values) == 0:
                stuck = True
                break
            else:
                self.insert(x, y, legal_values[randint(0, len(legal_values) - 1)])
                x, y = self.game.get_first_empty_cell(self.grid, self.read_only_tiles, x, y)

        if stuck:
            self.quit()

        if self.game.is_complete(self.grid):
            self.is_solved = True
            print("OMG COMPLETE")

        return self.actions_queue


class BackTrackingSolver(Solver):

    def solve(self):
        if self.__recursive_backtracking():
            self.is_solved = True
        return self.actions_queue

    def __recursive_backtracking(self, x=0, y=0):
        x, y = self.game.get_first_empty_cell(self.grid, self.read_only_tiles, x, y)
        if y == -1:
            return True

        legal_values = self.game.get_legal_values(self.grid, x, y)

        # # IMPROVED BACK TRACKING
        # if legal_values is not None:
        #     shuffle(legal_values)

        for value in legal_values:
            self.insert(x, y, value)
            if self.__recursive_backtracking(x, y):
                return True
            self.delete(x, y)
        return False


class CSPSolver(Solver):
    def solve(self):
        if self.__recursive_csp_backtracking():
            self.is_solved = True
        return self.actions_queue

    def __recursive_csp_backtracking(self, x = 0, y= 0):
        x, y = self._get_tile()
        if y == -1 and self.game.is_complete(self.grid):
            return True
        elif y == -1:
            return False

        chosen_value = self.__get_least_constraining_value(x,y)
        if chosen_value == -1:
            return False

        self.insert(x, y, chosen_value)
        if self.__recursive_csp_backtracking(x, y):
            return True

        # legal_values = self.game.get_legal_values(self.grid, x, y)
        # #print(legal_values)
        #
        # for value in legal_values:
        #     self.insert(x, y, value)
        #     if self.__recursive_csp_backtracking(x, y):
        #         return True
        #     self.delete(x, y)
        # return False

    def _get_tile(self):
        min_values_count_tiles = []
        min_values_count = np.inf

        '''
        Minimum Remaining Values - tiles with least legal values.
        '''
        for y in range(0,9):
            for x in range(0,9):
                if (x,y) not in self.read_only_tiles and\
                        self.get_value(x,y) == EMPTY_VALUE:
                    values_count = len(self.game.get_legal_values(self.grid, x, y))
                    if values_count == 1: # just one possible value. go for it
                        return x,y
                    if 0 < values_count < min_values_count:
                        min_values_count_tiles = [(x,y)] # reset the array and add (x,y)
                        min_values_count = values_count
                    elif values_count == min_values_count:
                        min_values_count_tiles += [(x, y)] # just add (x,y)


        if len(min_values_count_tiles) == 0:
            return -1, -1

        if len(min_values_count_tiles) == 1:
            return min_values_count_tiles[0]

        '''
        for the tiles from the previous heuristic:
        Degree Heuristic - tiles with least empty neighbors (row, col, block)
        '''
        min_empty_neighbors_count_tiles = []
        min_empty_neighbors_count = np.inf
        for (x, y) in min_values_count_tiles:
            row, col, block = self.game.get_row(self.grid, x), \
                              self.game.get_column(self.grid, y), \
                              self.game.get_block(self.grid, x, y)

            empty_neighbors_count = np.count_nonzero(row) + np.count_nonzero(col) + np.count_nonzero(block)
            if 0 < empty_neighbors_count < min_empty_neighbors_count:
                min_empty_neighbors_count_tiles = [(x,y)]
                min_empty_neighbors_count = empty_neighbors_count
            elif empty_neighbors_count == min_empty_neighbors_count:
                min_empty_neighbors_count_tiles += [(x, y)]

        return min_empty_neighbors_count_tiles[0] # todo somthing smarter

    def __get_least_constraining_value(self, x, y):
        legal_values = self.game.get_legal_values(self.grid, x, y)

        chosen_value = 0
        max_count = -np.inf
        for value in legal_values:
            values_count = 0
            self.insert(x, y, value)
            for x_n,y_n in self.game.get_neighbors(x,y):
                if self.get_value(x_n,y_n) == EMPTY_VALUE:

                    neighbor_legal_values_count = len(self.game.get_legal_values(self.grid,x_n,y_n))

                    if neighbor_legal_values_count == 0:
                        values_count = np.inf # no way to chose it
                        break
                    values_count += len(self.game.get_legal_values(self.grid, x_n,y_n))

            if values_count > max_count:
                max_count = values_count
                chosen_value = value
            self.delete(x,y)

        if chosen_value == 0:
            return -1

        return chosen_value






        # todo if one of neigbors gets 0 return -1








