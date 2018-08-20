~~~ SUDOKU ~~~

This project was created by Harel Farkash, Jonathan Meerson and Avi Korzac

Dependencies:
	numpy
	pygame (can be installed with pip3)

Usage:
	python3 game.py <board-path> solver=<backtracking|csp|arc|forward_checking|simulated_annealing> display=<true|false> print=<true|false>
Example:
	python3 game.py puzzles/easy.txt csp false true