EMPTY_VALUE = 0
delay = 0.05

def grid_to_string(grid):
    string = ""
    for i in range(9):
        if i in [3, 6]:
            string += '---+---+---\n'
        for j in range(9):
            if j in [3, 6]:
                string += '|'
            string += str(grid[i][j])
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