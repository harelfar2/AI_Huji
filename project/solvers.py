import abc
from random import randint, shuffle
from util import Action, EMPTY_VALUE
from collections import deque
import sys


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


