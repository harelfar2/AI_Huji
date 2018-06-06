import numpy
from sudoku import Sudoku



if __name__ == '__main__':
    game = Sudoku(filename="puzzles/easy.txt", display_enabled=True, solver_type='backtracking')
    game.play()