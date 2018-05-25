EMPTY_VALUE = 0
delay = 0.005

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