import numpy
from sudoku import Sudoku



if __name__ == '__main__':
    # game = Sudoku(filename="puzzles/easy.txt", display_enabled=False, solver_type='sa')
    # game.play()

    # sum = 0
    #
    # for i in range(1000):
    #     game = Sudoku(filename="puzzles/easy.txt", display_enabled=False, print=True, solver_type='csp')
    #     total = game.play()
    #
    #     print("i:", i, "total:", total)
    #     sum += total
    #
    # print(sum / 1000)

    # a = numpy.empty((9,9), dtype=object)
    #
    # a[0][0] = [1,2,3]
    #
    # a[8,8] = [1]
    #
    # a[5][3] = [1,2,2,3,4]
    #
    # print(a)

    game = Sudoku(filename="puzzles/backtracking_hard.txt", display_enabled=False, print=True, solver_type='ac')
    game.play()

    game = Sudoku(filename="puzzles/backtracking_hard.txt", display_enabled=False, print=False, solver_type='csp')
    game.play()
