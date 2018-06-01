import abc
from random import randint
from util import Action, EMPTY_VALUE
from collections import deque
import sys


class Solver(object):
    def __init__(self, game):
        super(Solver, self).__init__()
        self.max = 0
        self.actions_queue = deque()
        self.game = game
        self.grid = game.get_grid().copy()
        self.read_only_tiles = game.get_read_only().copy()
        self.full_tiles = self.read_only_tiles.copy()

    @abc.abstractmethod
    def solve(self):
        return

    def insert(self, x, y, value):
        if (x, y) in self.read_only_tiles:
            print("READ ONLY TIEL ON (", x, y, ") CAN'T INSERT VALUE", value)
            sys.exit()
        self.grid[y][x] = value
        self.full_tiles += [(x, y)]
        self.actions_queue.append((Action(x, y, value)))

    def delete(self, x, y):
        if (x, y) in self.read_only_tiles:
            print("READ ONLY TIEL ON (", x, y, ") CAN'T DELETE")
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

        for y in range(9):
            if stuck:
                break
            for x in range(9):
                if self.get_value(x,y) == EMPTY_VALUE and (x, y) not in self.read_only_tiles:
                    legal_values = self.game.get_legal_values(self.grid, x, y)
                    if len(legal_values) == 0:
                        stuck = True
                        continue
                    else:
                        self.insert(x, y, legal_values[randint(0, len(legal_values) - 1)])

        if stuck:
            self.quit()

        if self.game.is_complete(self.grid):
            print("OMG")

        return self.actions_queue

