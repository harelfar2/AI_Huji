import numpy
from sudoku import Sudoku



if __name__ == '__main__':
    grid_values = numpy.random.randint(9, size = (9,9))
    game = Sudoku(filename="puzzles/backtracking_hard.txt", display_enabled=False, solver_type='backtracking')
    game.play()