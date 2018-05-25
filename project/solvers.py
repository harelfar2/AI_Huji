import abc
from random import randint
from util import Action, EMPTY_VALUE

class Solver(object):
    def __init__(self):
        super(Solver, self).__init__()
        self.read_only = set()

    @abc.abstractmethod
    def get_action(self, game):
        return

    def add_read_only_tile(self, tile):
        self.read_only.add(tile)

class StupidSolver(Solver):

    def get_action(self, game):

        grid = game.get_grid()

        # small chance to just quit
        quit = randint(0,10000)
        if quit == 500:
            return Action(quit=True)

        full_tiles_count = 0

        stcuk = False

        for x in range(9):

            if stcuk:
                break
            for y in range(9):
                if (x, y) in self.read_only or grid[y][x] != EMPTY_VALUE:
                    full_tiles_count += 1
                else:
                    legal_values = game.get_legal_values(x, y)
                    if len(legal_values) == 0:
                        stcuk = True
                        continue
                    return Action(x, y, legal_values[randint(0, len(legal_values) - 1)])

        if stcuk:
            return Action(quit=True)

        # board is full and not legal. delete something random
        while True:
            x, y = randint(0, 8), randint(0, 8)
            if (x, y) not in self.read_only:
                return Action(x,y)
            if quit == 500:
                return Action(x,y)

