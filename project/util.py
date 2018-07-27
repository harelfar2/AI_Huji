import numpy as np

EMPTY_VALUE = 0
delay = 0.05

solved_example = np.array([[7, 3, 5, 6, 1, 4, 8, 9, 2],
                   [8, 4, 2, 9, 7, 3, 5, 6, 1],
                   [9, 6, 1, 2, 8, 5, 3, 7, 4],
                   [2, 8, 6, 3, 4, 9, 1, 5, 7],
                   [4, 1, 3, 8, 5, 7, 9, 2, 6],
                   [5, 7, 9, 1, 2, 6, 4, 3, 8],
                   [1, 5, 7, 4, 9, 2, 6, 8, 3],
                   [6, 9, 4, 7, 3, 8, 2, 1, 5],
                   [3, 2, 8, 5, 6, 1, 7, 4, 9], ])

def grid_to_string(grid):
    string = ""
    for i in range(9):
        if i in [3, 6]:
            string += '- - - + - - - + - - -\n'
        for j in range(9):
            if j in [3, 6]:
                string += '| '
            string += str(grid[i][j]) + " "
        string += "\n"

    return string


class Action:
    INSERT = 1
    DELETE = 2
    QUIT = -1

    def __init__(self, x=0, y=0, value = None, quit = False):
        if quit:
            self.id = Action.QUIT
        elif not value:
            self.id = Action.DELETE
            value = EMPTY_VALUE
        else:
            self.id = Action.INSERT

        self.x = x
        self.y = y
        self.value = value
        self.actions_count = 0