import numpy
from sudoku import Sudoku



if __name__ == '__main__':
    game = Sudoku(filename="puzzles/easy.txt", display_enabled=False, solver_type='sa')
    game.play()

    sum = 0

    for i in range(20):
        game = Sudoku(filename="puzzles/easy.txt", display_enabled=False, print=True, solver_type='sa')
        total = game.play()

        print("i:", i, "total:", total)
        sum += total

    print(sum / 20)
