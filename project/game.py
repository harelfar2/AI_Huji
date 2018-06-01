import numpy
from sudoku import Sudoku
from solvers import StupidSolver



if __name__ == '__main__':
    grid_values = numpy.random.randint(9, size = (9,9))
    game = Sudoku(filename="puzzles/easy.txt", display_enabled=True)
    game.play()