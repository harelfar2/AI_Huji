import abc
from random import randint
from util import Action, EMPTY_VALUE


class Solver(object):
    def __init__(self):
        super(Solver, self).__init__()
        self.max = 0

    @abc.abstractmethod
    def get_action(self, game):
        return


class StupidSolver(Solver):

    def get_action(self, game):

        stuck = False

        for y in range(9):
            if stuck:
                break
            for x in range(9):
                if game.get_value(x,y) == EMPTY_VALUE and (x, y) not in game.get_read_only():
                    legal_values = game.get_legal_values(x, y)
                    if len(legal_values) == 0:
                        stuck = True
                        continue
                    return Action(x, y, legal_values[randint(0, len(legal_values) - 1)])

        # delete something random
        while True:
            tile = game.get_full_tiles()[randint(0, len(game.get_full_tiles()) - 1)]
            if tile not in game.get_read_only():
                return Action(tile[0], tile[1])