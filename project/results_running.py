from sudoku import Sudoku, SolverType
import sys


solvers = [SolverType.BACKTRACKING,
           SolverType.ARC_CONSISTENCY,
           SolverType.CSP,
           SolverType.FORWARD_CHECKING]

def deterministic_algorithms_on_paper_puzzles(runs):
    print("*******************************************\n"
          "Deterministic algorithms on regular puzzles\n"
          "*******************************************")
    with open('results.txt', 'a') as results_file:

        paper_puzzles = ["easy.txt", "medium.txt", "hard.txt", "backtracking_hard.txt"]

        results_file.write(str(runs) + " runs for each deterministic solver on each puzzle\n\n")
        results_file.flush()
        for puzzle in paper_puzzles:
            print("~puzzle:", puzzle, flush=True)
            results_file.write("\n~~~   " + puzzle + "   ~~~\n")
            results_file.flush()
            for solver in solvers:
                print("    -", solver)
                sum_time = 0
                actions = 0
                for i in range(runs):
                    game = Sudoku(filename="puzzles/" + puzzle, display_enabled=False, print=False, solver_type=solver)
                    time, actions, is_solved = game.play()
                    sum_time += time
                results_file.write("    " + solver + " time: " + str(round(sum_time / runs, 3)) + " actions:" +
                                   str(actions) + "\n")
                results_file.flush()


def simulated_annealing(runs):

    print("**************************************\n"
          "Simulated Annealing on regular puzzles\n"
          "**************************************")

    paper_puzzles = ["easy2.txt",
                     "medium.txt", "medium2.txt", "medium3.txt", "medium4.txt",
                     "hard.txt", "hard2.txt",
                     "evil.txt", "evil2.txt"]

    with open('results.txt', 'a') as results_file:

        results_file.write("\n\n\n" + str(runs) + " runs simulated annealing solver on each puzzle\n\n")
        results_file.flush()

        for puzzle in paper_puzzles:
            print("~puzzle:", puzzle, flush=True)
            results_file.write("\n~~~   " + puzzle + "   ~~~\n")
            results_file.flush()
            sum_time = 0
            successes = 0
            for i in range(runs):
                game = Sudoku(filename="puzzles/" + puzzle, display_enabled=False, print=False,
                              solver_type=SolverType.SIMULATED_ANNEALING)
                time, actions, is_solved = game.play()
                if is_solved:
                    sys.stdout.write("1")
                    sys.stdout.flush()
                    sum_time += time
                    successes += 1
                else:
                    sys.stdout.write("0")
                    sys.stdout.flush()
            print(flush=True)

            results_file.write("    success rate: " + str(successes / runs * 100) + "%" +
                               " with average time: " + str(round(sum_time / successes, 3)))
            results_file.flush()


def backtracking_hard(runs):

    print("*********************************************\n"
          "Deterministic Algorithms on backtracking_hard\n"
          "*********************************************")

    puzzle = "backtracking_hard.txt"

    with open('results.txt', 'a') as results_file:

        results_file.write("\n\n\n" + str(runs) + " runs for each deterministic solver on backtracking_hard puzzle\n\n")
        results_file.flush()

        print("~puzzle:", puzzle, flush=True)
        results_file.write("\n~~~   " + puzzle + "   ~~~\n")
        results_file.flush()
        for solver in solvers:
            print("    -", solver)
            sum_time = 0
            actions = 0
            for i in range(runs):
                game = Sudoku(filename="puzzles/" + puzzle, display_enabled=False, print=False, solver_type=solver)
                time, actions, is_solved = game.play()
                sum_time += time
            results_file.write("    " + solver + " time: " + str(round(sum_time / runs, 3)) + " actions:" +
                               str(actions) + "\n")
            results_file.flush()


if __name__ == '__main__':
    deterministic_algorithms_on_paper_puzzles(100)
    simulated_annealing(100)
    backtracking_hard(5)