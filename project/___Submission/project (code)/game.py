from sudoku import Sudoku, SolverType
import sys


def print_explanation_and_terminate():
    print("USAGE: <board-path> solver=<backtracking|csp|arc|forward_checking|simulated_annealing> "
          "display=<true|false> print=<true|false>")
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

    SOLVER_TYPES = {"backtracking": SolverType.BACKTRACKING,
                    "csp": SolverType.CSP,
                    "arc": SolverType.ARC_CONSISTENCY,
                    "forward_checking": SolverType.FORWARD_CHECKING,
                    "simulated_annealing": SolverType.SIMULATED_ANNEALING}


    try:
        solver_type = SOLVER_TYPES[args[2]]
    except Exception as e:
        print_explanation_and_terminate()



    TRUE_AND_FALSE = ["true", "false"]
    if args[3] not in TRUE_AND_FALSE or args[4] not in TRUE_AND_FALSE:
        print_explanation_and_terminate()
    display_enabled = True if args[3] == "true" else False
    print_enabled = True if args[4] == "true" else False

    game = Sudoku(filename, solver_type, display_enabled, print_enabled)
    game.play()
