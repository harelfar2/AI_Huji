import numpy
from sudoku import Sudoku, SolverType

if __name__ == '__main__':


    puzzles = ["easy.txt", "medium.txt", "hard.txt"]
    solvers = [SolverType.BACKTRACKING, SolverType.AC, SolverType.CSP]
    solvers_names = ["Backtracking", "Arc", "CSP"]

    with open('results.txt', 'a') as the_file:
        for puzzle in puzzles:
            the_file.write("\n"+puzzle + "\n")
            for j, solver in enumerate(solvers):
                sum_time = 0
                actions = 0
                for i in range(10):
                    game = Sudoku(filename="puzzles/" + puzzle, display_enabled=False, print=False, solver_type=solver)
                    time, actions = game.play()
                    sum_time += time
                the_file.write(solvers_names[j] + " time: " + str(sum_time / 10) + " actions: " + str(actions) +" \n")



