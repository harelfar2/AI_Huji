import numpy
from game_board import GameBoard

if __name__ == '__main__':
    grid_values = numpy.random.randint(9, size = (9,9))
    game = GameBoard(None, grid_values)
    game.play()