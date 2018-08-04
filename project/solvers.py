import abc
from random import randint, shuffle, random, sample
from util import Action, EMPTY_VALUE, solved_example
from collections import deque
from math import exp, ceil
import sys
import numpy as np
from copy import deepcopy


class Solver(object):
    def __init__(self, game):
        super(Solver, self).__init__()
        self.actions_queue = deque()
        self.is_solved = False
        self.game = game
        self.grid = deepcopy(game.get_grid())
        self.read_only_tiles = deepcopy(game.get_read_only())
        self.full_tiles = deepcopy(self.read_only_tiles.copy())

    @abc.abstractmethod
    def solve(self):
        """abstract method, each solver will solve in its way."""
        return


    def insert(self, x, y, value):
        """
        update insetrion to the grid with the value in coordibate (x,y)
        insert coordinate and value to the queue in order to recreate the actions that led to the solution.
        """
        if (x, y) in self.read_only_tiles:
            print("READ ONLY TILE ON ( ", x, y, ") CAN'T INSERT VALUE", value)
            sys.exit()
        self.grid[y][x] = value
        self.full_tiles += [(x, y)]
        self.actions_queue.append((Action(x, y, value)))


    def delete(self, x, y):
        """
        update deletion from the grid in the coordibate (x,y)
        delete content from coordinate from the queue in order to recreate the actions that led to the solution.
        """
        if (x, y) in self.read_only_tiles:
            print("READ ONLY TILE ON ( ", x, y, ") CAN'T DELETE")
            sys.exit()
        self.grid[y][x] = EMPTY_VALUE
        self.full_tiles.remove((x, y))
        self.actions_queue.append(Action(x, y))


    def quit(self):
        """ quit action"""
        self.actions_queue.append(Action(quit=True))


    def get_value(self, x, y):
        """ get value from coordinate"""
        return self.grid[y][x]


class StupidSolver(Solver):
    """
    This solver just puts some random (yet legal values) anywhere he can and when if he gets stuck he quits
    """
    def solve(self):

        stuck = False

        x, y = self.game.get_first_empty_cell(self.grid, self.read_only_tiles)
        while (x, y) is not None:
            legal_values = self.game.get_legal_values(self.grid, x, y)
            if len(legal_values) == 0:
                stuck = True
                break
            else:
                self.insert(x, y, legal_values[randint(0, len(legal_values) - 1)])
                x, y = self.game.get_first_empty_cell(self.grid, self.read_only_tiles, x, y)

        if stuck:
            self.quit()

        if self.game.is_complete(self.grid):
            self.is_solved = True
            print("OMG COMPLETE")

        return self.actions_queue


class BackTrackingSolver(Solver):
    """
    This solver will look for free spots and put possible values in there.
    If got stuck, will backtrace and try different value from where got stuck.
    """

    def solve(self):
        if self.__recursive_backtracking():
            self.is_solved = True
        return self.actions_queue

    def __recursive_backtracking(self, x=0, y=0):
        """Recursively try to put values in the first free spot, will stop if no empty cells exist."""
        x, y = self.game.get_first_empty_cell(self.grid, self.read_only_tiles, x, y)
        if y == -1:
            return True

        legal_values = self.game.get_legal_values(self.grid, x, y)

        for value in legal_values:
            self.insert(x, y, value)
            if self.__recursive_backtracking(x, y):
                return True
            self.delete(x, y)
        return False


class CSPSolver(Solver):
    def solve(self):
        if self.__recursive_csp_backtracking():
            self.is_solved = True
        return self.actions_queue

    def __recursive_csp_backtracking(self, x = 0, y= 0):
        """Solves the sudoku with 3 CSP heuristics:
        Minimum Remaining Values, degree heuristics, least constraining value
        """
        x, y = self._get_tile()
        if y == -1 and self.game.is_complete(self.grid):
            return True
        elif y == -1:
            return False
        chosen_values = self.__get_least_constraining_values(x, y)
        for value in chosen_values:
            self.insert(x, y, value)
            if self.__recursive_csp_backtracking(x, y):
                return True
            self.delete(x, y)
        return False

    def _get_tile(self):
        """Returns the tile that satisfies Minimum Remaining Values, degree heuristics"""
        min_values_count_tiles = []
        min_values_count = np.inf

        '''
        Minimum Remaining Values - tiles with least legal values.
        '''
        for y in range(0,9):
            for x in range(0,9):
                if (x,y) not in self.read_only_tiles and\
                        self.get_value(x,y) == EMPTY_VALUE:
                    values_count = len(self.game.get_legal_values(self.grid, x, y))
                    if values_count == 1: # just one possible value. go for it
                        return x,y
                    if 0 < values_count < min_values_count:
                        min_values_count_tiles = [(x,y)] # reset the array and add (x,y)
                        min_values_count = values_count
                    elif values_count == min_values_count:
                        min_values_count_tiles += [(x, y)] # just add (x,y)


        if len(min_values_count_tiles) == 0:
            return -1, -1

        if len(min_values_count_tiles) == 1:
            return min_values_count_tiles[0]

        '''
        for the tiles from the previous heuristic:
        Degree Heuristic - tiles with least empty neighbors (row, col, block)
        '''
        min_empty_neighbors_count_tiles = []
        min_empty_neighbors_count = 0
        for (x, y) in min_values_count_tiles:
            row, col, block = self.game.get_row(self.grid, x), \
                              self.game.get_column(self.grid, y), \
                              self.game.get_block(self.grid, x, y)

            empty_neighbors_count = np.count_nonzero(row) + np.count_nonzero(col) + np.count_nonzero(block)
            if empty_neighbors_count > min_empty_neighbors_count:
                min_empty_neighbors_count_tiles = [(x,y)]
                min_empty_neighbors_count = empty_neighbors_count
            elif empty_neighbors_count == min_empty_neighbors_count:
                min_empty_neighbors_count_tiles += [(x, y)]

        return min_empty_neighbors_count_tiles[0]

    def __get_least_constraining_values(self, x, y):
        """Return the value that will constrain other tiles the least.
        Go through every neighbor the the chosen tile, and check how many possibilities all the neighbor have,
         and choose the value that gives the neighbors the most possibilities."""
        legal_values = np.ndarray.tolist(self.game.get_legal_values(self.grid, x, y))

        legal_values.sort(key=lambda value: -self._neighbor_legal_values_count(x,y, value))

        return legal_values



    def _neighbor_legal_values_count(self, x, y, value):
        """Get the number of possible values for all the neighbor for the given value"""
        values_count = 0
        self.insert(x, y, value)
        for x_neighbor, y_neighbor in self.game.get_neighbors(x, y):
            if self.get_value(x_neighbor, y_neighbor) == EMPTY_VALUE:
                neighbor_legal_values_count = len(self.game.get_legal_values(self.grid, x_neighbor, y_neighbor))
                if neighbor_legal_values_count == 0:
                    values_count = -np.inf  # no way to chose it
                    break
                values_count += neighbor_legal_values_count

        self.delete(x, y)

        return values_count


        # todo if one of neigbors gets 0 return -1


class SimulatedAnnealingSolver(Solver):
    def solve(self):

        self.random_fill()

        curr_score = self.score(self.grid)

        temperature = 1
        iteration_count, escape_count, stuck_count = 0, 0, 0
        best_score = curr_score
        switches = 0

        while True:
            iteration_count += 1
            if iteration_count % 1000 == 0:
                print("iteration:", iteration_count, "escapes:", escape_count, "switches:", switches,
                      "score:", curr_score, "temp:", temperature)
                escape_count = 0
                switches = 0

            succ = self.switch_tiles()
            succ_score = self.score(succ)

            if succ_score == 243:
                print(self.score(succ))
                self.grid = succ
                self.game.set_grid(succ)
                return

            delta = float(succ_score - curr_score)


            if delta > 0:
                old_grid = deepcopy(self.grid)
                self.grid = deepcopy(succ)
                switches += 1
                curr_score = succ_score

                if exp(min(delta / temperature, 709)) - random() > 0:
                    self.grid = deepcopy(old_grid)

            else:
                if exp(delta / temperature) - random() > 0:
                    escape_count += 1
                    self.grid = deepcopy(succ)
                    switches += 1
                    curr_score = succ_score

            if best_score < curr_score:
                stuck_count = 0
                best_score = curr_score
            else:
                stuck_count += 1
                if stuck_count % (3000 + 5000//(243 - best_score)) == 0: # we've been same or worse then the best score for a long time
                    print("\nRANDOMIZE!, couldn't pass", best_score, "for", stuck_count, "iterations\n", )

                    self.randomize()
                    # todo
                    # self.delete_progress()
                    # self.random_fill()

                    stuck_count = 0
                    curr_score = self.score(self.grid)
                    print("score after random:", curr_score)
                    best_score = curr_score
                    #temperature = 1

            temperature *= .999

    def random_fill(self):
        for x in range(9):
            possible_values = np.setdiff1d(np.array([value for value in range(1, 10)]),
                                           self.game.get_column(self.grid, x))
            for y in range(9):
                if self.get_value(x,y) == 0: # or else it is read only and we don't mess with it
                    rand_index = randint(0, len(possible_values) - 1)
                    self.insert(x, y, possible_values[rand_index])
                    possible_values = np.delete(possible_values, rand_index)

    def score(self, grid):
        score = 0
        for i in range(9):
            score += len(set(self.game.get_row(grid, i)))
            score += len(set(self.game.get_column(grid, i)))

        for y in [0, 3, 6]:
            for x in [0, 3, 6]:
                score += len(set(self.game.get_block(grid, x, y)))

        return score

    def get_random_neighbors(self):
        x = randint(0,8)
        y1 = randint(0, 8)
        y2 = randint(0, 8)
        while y1 != y2 and (x, y1) not in self.read_only_tiles and (x, y2) not in self.read_only_tiles:
            x = randint(0, 8)
            y1 = randint(0, 8)
            y2 = randint(0, 8)

        return (x, y1), (x, y2)

    def switch_tiles(self):
        next_grid = deepcopy(self.grid.copy())

        (x1, y1), (x2, y2) = self.get_random_neighbors()
        value1 = self.get_value(x1, y1)
        value2 = self.get_value(x2, y2)

        next_grid[y1][x1] = value2
        next_grid[y2][x2] = value1

        return next_grid

    def randomize(self):
        columns_to_shuffle = sample(range(0, 9), randint(1, 5))

        for x in columns_to_shuffle:
            for y in range(0, 9):
                if (x, y) not in self.read_only_tiles:
                    self.delete(x, y)

        for x in columns_to_shuffle:
            possible_values = np.setdiff1d(np.array([value for value in range(1, 10)]),
                                           self.game.get_column(self.grid, x))
            for y in range(0, 9):
                if self.get_value(x,y) == 0: # or else it is read only and we don't mess with it
                    rand_index = randint(0, len(possible_values) - 1)
                    self.insert(x, y, possible_values[rand_index])
                    possible_values = np.delete(possible_values, rand_index)







    def delete_progress(self):
        for y in range(9):
            for x in range(9):
                if (x, y) not in self.read_only_tiles:
                    self.delete(x,y)


class ArcConsistencySolver(Solver):
    def solve(self):
        self.create_domains_matrix()
        self.create_arcs_queue()
        self.domains_reduction()

        if self.__recursive_backtracking():
            self.is_solved = True
        return self.actions_queue


    def __recursive_backtracking(self, x=0, y=0):
        x, y = self.game.get_first_empty_cell(self.grid, self.read_only_tiles, x, y)
        if y == -1:
            return True

        legal_values = np.intersect1d(self.domain_matrix[y][x], self.game.get_legal_values(self.grid, x, y))

        for value in legal_values:
            self.insert(x, y, value)
            if self.__recursive_backtracking(x, y):
                return True
            self.delete(x, y)
        return False

    def create_domains_matrix(self):
        '''
        create an 9x9 matrix where each entry (x,y) holds the domain of the (x,y) tile
        '''

        self.domain_matrix = np.empty((9,9), dtype=object)

        for y in range(9):
            for x in range(9):
                if self.get_value(x, y) == EMPTY_VALUE:
                    self.domain_matrix[y][x] = self.game.get_legal_values(self.grid, x, y)
                else:
                    self.domain_matrix[y][x] = np.array([self.get_value(x,y)])

    def create_arcs_queue(self):
        '''
        creates a queue of pairs of neighbors ((x1,y1),(x2,y2)) of the matrix
        :return:
        '''
        self.arcs_queue = set()
        for y in range(9):
            for x in range(9):

                if self.get_value(x, y) == EMPTY_VALUE:
                    for neighbor in self.game.get_neighbors_indexes(x, y):
                        self.arcs_queue.add(((x,y), neighbor))

    def domains_reduction(self):
        while self.arcs_queue:
            pair = self.arcs_queue.pop()
            if self.remove_inconsistent_values(pair):
                if pair[1] not in self.read_only_tiles:
                    for neighbor in self.game.get_neighbors_indexes(pair[1][0], pair[1][1]):
                        self.arcs_queue.add((pair[1], neighbor))

    def remove_inconsistent_values(self, pair):
        (x1, y1), (x2, y2) = pair[0], pair[1]

        if len(self.domain_matrix[y2][x2]) != 1:
            return False

        removed = False
        for value1 in self.domain_matrix[y1][x1]:
            if self.domain_matrix[y2][x2][0] == value1:
                # delete value1 from [x1, y1]
                self.domain_matrix[y1][x1] = np.delete(self.domain_matrix[y1][x1],
                                                       np.argwhere(self.domain_matrix[y1][x1] == value1))

                removed = True

        return removed







