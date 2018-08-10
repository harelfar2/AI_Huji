from sudoku import Sudoku, SolverType

if __name__ == '__main__':

    puzzles = ["easy.txt", "easy2.txt", "easy3.txt", "easy4.txt",
               "medium.txt", "medium2.txt", "medium3.txt", "medium4.txt",
               "hard.txt", "hard2.txt",
               "evil.txt", "evil2.txt"]

    solvers = [SolverType.BACKTRACKING,
               SolverType.ARC_CONSISTENCY,
               SolverType.CSP,
               SolverType.FORWARD_CHECKING]
    RUNS = 10

    with open('results.txt', 'w') as results_file:
        results_file.write(str(RUNS) + " runs for each solver on each puzzle\n\n")
        for puzzle in puzzles:
            print("~puzzle:", puzzle, flush=True)
            results_file.write("\n~~~   " + puzzle + "   ~~~\n")
            for solver in solvers:
                print("    -", solver)
                sum_time = 0
                actions = 0
                for i in range(RUNS):
                    game = Sudoku(filename="puzzles/" + puzzle, display_enabled=False, print=False, solver_type=solver)
                    time, actions = game.play()
                    sum_time += time
                results_file.write("    " + solver + " time: " + str(round(sum_time / RUNS, 3)) + " actions:" +
                                   str(actions) + " mistakes: "  + "\n")





