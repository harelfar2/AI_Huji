from board import Board
from search import SearchProblem, ucs
import util


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        return state.get_position(0, 0) != -1 and \
               state.get_position(state.board_w - 1, 0) != -1 and \
               state.get_position(0, state.board_h - 1) != -1 and \
               state.get_position(state.board_w - 1, state.board_h - 1) != -1

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles())
                for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """

        moves_sum = 0
        for move in actions:
            moves_sum += move.piece.num_tiles
        return moves_sum


def blokus_corners_heuristic(state, problem):

    board = state[0]
    board_h = board.board_h
    board_w = board.board_w
    board_side_max = board.board_h + board.board_w

    # min_dis_corners = [board_side_max] * 4

    min_distance = board_side_max * 4

    # if board.get_position(0, 0) == 0:
    #     min_dis_corners[0] = 0
    #
    # if board.get_position(0, board_h - 1) == 0:
    #     min_dis_corners[1] = 0
    #
    # if board.get_position(board_w - 1, 0) == 0:
    #     min_dis_corners[2] = 0
    #
    # if board.get_position(board_w - 1, board_h - 1) == 0:
    #     min_dis_corners[3] = 0

    for row in range(board_h):
        for col in range(board_w):
            if board.get_position(row, col) == 0:
                continue
            if is_adj_to_piece(row, col, board):
                continue
            if not is_diagonal_to_piece(row, col, board):
                continue

            point_sum_distances = 0

            if board.get_position(0, 0) == -1:
                point_sum_distances += util.manhattanDistance((0, 0), (col, row))

            if board.get_position(0, board_h - 1) == -1:
                point_sum_distances += util.manhattanDistance((0, board_h - 1), (col, row))

            if board.get_position(board_w - 1, 0) == -1:
                point_sum_distances += util.manhattanDistance((board_w - 1, 0), (col, row))

            if board.get_position(board_w - 1, board_h - 1) == -1:
                point_sum_distances += util.manhattanDistance((board_w - 1, board_h - 1), (col, row))


            min_distance = min(point_sum_distances, min_distance)

            # min_dis_corners = [min(min_dis_corners[0], util.manhattanDistance((0, 0), (col, row))),
            #                    min(min_dis_corners[1], util.manhattanDistance((0, board_h - 1), (col, row))),
            #                    min(min_dis_corners[2], util.manhattanDistance((board_w - 1, 0), (col, row))),
            #                    min(min_dis_corners[3], util.manhattanDistance((board_w - 1, board_h - 1), (col, row)))]

    return min_distance


    # return sum(min_dis_corners)


def is_adj_to_piece(row, col, state):
    flag = True

    board = state.state
    board_h = state.board_h
    board_w = state.board_w
    if col != 0:
        flag = flag and board[row, col - 1] == -1

    if col != board_w -1:
        flag = flag and board[row, col + 1] == -1

    if row != 0:
        flag = flag and board[row - 1, col] == -1


    if row != board_h - 1:
        flag = flag and board[row + 1, col] == -1


    return not flag


def is_diagonal_to_piece(row, col, state):
    board = state.state
    board_h = state.board_h
    board_w = state.board_w


    if row != 0 and col != 0:
        if board[row - 1, col - 1] == 0:
            return True

    if row != board_h - 1 and col != board_w - 1:
        if board[row + 1, col + 1] == 0:
            return True

    if row != 0 and col != board_w - 1:
        if board[row - 1, col + 1] == 0:
            return True


    if row != board_h - 1 and col != 0:
        if board[row + 1, col - 1] == 0:
            return True

    return False



class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state): #todo can be more efficiant
        for (x, y) in self.targets:
            if state.get_position(x,y) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        moves_sum = 0
        for move in actions:
            moves_sum += move.piece.num_tiles
        return moves_sum


def blokus_cover_heuristic(state, problem):
    board = state[0]
    board_h = board.board_h
    board_w = board.board_w
    board_side_max = board.board_h + board.board_w

    targets = problem.targets
    # min_dis_targets = [board_side_max] * len(targets)

    min_distance = board_side_max * len(targets)



    # for i, (x,y) in enumerate(targets):
    #     if board.get_position(x, y) == 0:
    #         min_dis_targets[i] = 1

    for row in range(board_h):
        for col in range(board_w):
            if board.get_position(row, col) == 0:
                continue
            if is_adj_to_piece(row, col, board):
                continue
            if not is_diagonal_to_piece(row, col, board):
                continue

            point_sum_distances = 0

            for i, (x,y) in enumerate(targets):
                if board.get_position(x,y) == -1:
                    point_sum_distances += util.manhattanDistance((x, y), (col, row))

            min_distance = min(point_sum_distances, min_distance)

            # for i, target in enumerate(targets):
            #     min_dis_targets[i] = min(min_dis_targets[i],
            #                              util.manhattanDistance(target, (col, row)))

    return min_distance
    # return sum(min_dis_targets)


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()



class MiniContestSearch :
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

