import numpy
from sudoku import Sudoku, SolverType

if __name__ == '__main__':

    game = Sudoku(filename="puzzles/backtracking_hard.txt", display_enabled=False, print=True, solver_type=SolverType.AC)
    game.play()

    game = Sudoku(filename="puzzles/backtracking_hard.txt", display_enabled=False, print=False, solver_type=SolverType.CPS)
    game.play()




