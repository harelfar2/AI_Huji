import numpy
from sudoku import Sudoku



if __name__ == '__main__':
    # game = Sudoku(filename="puzzles/easy.txt", display_enabled=False, print=False, solver_type='backtracking')
    # game.play()

    game = Sudoku(filename="puzzles/backtracking_hard.txt", display_enabled=False, print=False, solver_type='csp')
    game.play()