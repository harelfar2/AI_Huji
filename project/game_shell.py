from sudoku import Sudoku
import sys


def print_explanation_and_terminate():
    print("USAGE: <board-path> solver=<stupid|backtracking|csp> display=<true|false> print=<true|false>")
    print("example: puzzles/backtracking_hard.txt csp true false")
    exit(-1)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 5:
        print_explanation_and_terminate()
    filename = args[1]
    try:
        file = open(filename)
        file.close()
    except OSError as os_error:
        print(os_error)
        print_explanation_and_terminate()

    SOLVER_TYPES = ["stupid", "backtracking", "csp", "sa", "ac"]
    solver_type = args[2]
    if solver_type not in SOLVER_TYPES:
        print_explanation_and_terminate()

    TRUE_AND_FALSE = ["true", "false"]
    if args[3] not in TRUE_AND_FALSE or args[4] not in TRUE_AND_FALSE:
        print_explanation_and_terminate()
    display_enabled = True if args[3] == "true" else False
    print_enabled = True if args[4] == "true" else False

    game = Sudoku(filename, solver_type, display_enabled, print_enabled)
    game.play()
