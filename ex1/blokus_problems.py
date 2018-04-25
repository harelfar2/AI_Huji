from board import Board
from search import SearchProblem, a_star_search, SearchNode, get_path
import util

a = 1

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
    if problem.is_goal_state(board):
        return 0
    board_h = board.board_h
    board_w = board.board_w
    board_side_max = board.board_h + board.board_w

    corners = [(0, 0), (0, board_h - 1), (board_w - 1, 0), (board_w - 1, board_h - 1)]
    targets = []

    for (x, y) in corners:
        if board.get_position(x, y) == -1:
            targets += [(x, y)]

    max_distance = 0

    for row in range(board_h):
        for col in range(board_w):
            if board.get_position(row, col) == 0:
                continue
            if is_adj_to_piece(row, col, board):
                continue
            if not is_diagonal_to_piece(row, col, board):
                continue

            min_distance = board_side_max
            for target in targets:
                min_distance = min(min_distance, chess_distance((col, row), target))

            max_distance = max(min_distance, max_distance)

    return max_distance * len(targets)


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.starting_point = starting_point
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

    if problem.is_goal_state(board):
        return 0

    board_h = board.board_h
    board_w = board.board_w
    board_side_max = board.board_h + board.board_w

    targets = []

    for (x, y) in problem.targets:
        if board.get_position(x, y) == -1:
            targets += [(x, y)]

    max_distance = 0

    for row in range(board_h):
        for col in range(board_w):
            if board.get_position(row, col) == 0:
                continue
            if is_adj_to_piece(row, col, board):
                continue
            if not is_diagonal_to_piece(row, col, board):
                continue

            min_distance = board_side_max
            for target in targets:
                min_distance = min(min_distance, chess_distance((col, row), target))

            max_distance = max(min_distance, max_distance)

    return max_distance * len(targets)


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.start_board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.targets = list(targets.copy())
        self.board_w = board_w
        self.board_h = board_h
        self.piece_list = piece_list
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.start_board

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

        backtrace = []
        one_target_back_trace = None

        targets = list(reversed(sort_targets(self.targets, self.starting_point)))


        completed_targets = []

        while targets:
            cur_target = targets.pop()
            problem = BlokusCoverProblem(self.board_w, self.board_h, self.piece_list, self.starting_point,
                                         completed_targets + [cur_target])

            if one_target_back_trace:
                for action in one_target_back_trace:
                    self.board = self.board.do_move(0, action)

            problem.board = self.board

            one_target_back_trace = a_star_search_closest(problem, blokus_cover_heuristic, self.board.__copy__())
            for action in one_target_back_trace:
                backtrace.append(action)

            completed_targets.append(cur_target)

            self.expanded += problem.expanded

            print("completed target", cur_target, "with", problem.expanded, "nodes")

        return backtrace


def sort_targets(targets, starting_point):
    targets.sort(key=lambda p: chess_distance(p, starting_point))
    return targets


def a_star_search_closest(problem, heuristic, board):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    fringe.push(SearchNode(board, None, None, 0), 0)

    seen = set()

    while fringe:

        current_node = fringe.pop()

        if problem.is_goal_state(current_node.state):
            return get_path(current_node)

        if current_node.state in seen:
            continue

        seen.add(current_node.state)

        successors = problem.get_successors(current_node.state)
        for succ in successors:
            g = succ[2] + current_node.cost
            h = heuristic(succ, problem)
            node = SearchNode(succ[0], succ[1], current_node, g)

            fringe.push(node, g + h)

    return []


class MiniContestSearch :
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.targets = targets.copy()
        self.board_w = board_w
        self.board_h = board_h
        self.piece_list = piece_list
        self.starting_point = starting_point
        self.targets = targets.copy()


    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"


        #targets = list(reversed(sort_targets(self.targets, self.starting_point)))
        search = ClosestLocationSearch(self.board_w, self.board_h, self.piece_list, self.starting_point, self.targets)

        res = search.solve()

        self.expanded = search.expanded

        return res


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


def chess_distance(xy1, xy2):
    return max(abs(xy1[0] - xy2[0]), abs(xy1[1] - xy2[1]))