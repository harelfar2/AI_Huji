import numpy
from sudoku import Sudoku, SolverType

if __name__ == '__main__':

    puzzles = ["easy.txt", "medium.txt", "hard.txt"]
    solvers = [SolverType.BACKTRACKING, SolverType.CONSTRAINT_SATISFACTION_PROBLEM_HEURISTICS, SolverType.ARC_CONSISTENCY, SolverType.FORWARD_CHECKING]
    solvers_names = ["Backtracking", "Arc-Consistency", "CSP-Heuristics", "Forward-Checking"]

    RUNS = 10

    with open('results.txt', 'a') as results_file:
        results_file.write(str(RUNS) + " runs for each solver on each puzzle\n\n")
        for puzzle in puzzles:
            print("puzzle:", puzzle)
            results_file.write("\n~~~   " + puzzle + "   ~~~\n")
            for j, solver in enumerate(solvers):
                print("    solver:", solver)
                sum_time = 0
                actions = 0
                for i in range(RUNS):
                    game = Sudoku(filename="puzzles/" + puzzle, display_enabled=False, print=False, solver_type=solver)
                    time, actions = game.play()
                    sum_time += time
                results_file.write("    " + solvers_names[j] + " time: " + str(round(sum_time / RUNS, 3)) + " actions: " + str(actions) + " \n")

    # game = Sudoku(filename="puzzles/" + "backtracking_hard.txt", display_enabled=False, print=True, solver_type=SolverType.BACKTRACKING)
    # time, actions = game.play()



