import numpy
from sudoku import Sudoku



if __name__ == '__main__':
    game = Sudoku(filename="puzzles/easy.txt", display_enabled=False, solver_type='backtracking')
    game.play()

    game = Sudoku(filename="puzzles/easy.txt", display_enabled=False, solver_type='csp')
    game.play()