"""
In search.py, you will implement generic search algorithms
"""

from queue import PriorityQueue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()




def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state())
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """

    fringe =[]
    seen = []

    fringe.append(((problem.get_start_state(), None, 0), []))

    while fringe:
        l_state, path = fringe.pop()
        board = l_state[0]
        move = l_state[1]
        if move is not None:
            path = path + [move]  # add the move object to the path

        seen = seen + [board]
        if problem.is_goal_state(board):
            return path

        successors = problem.get_successors(board)
        for l_succ in successors:
            if l_succ[0] not in seen:
                fringe.append((l_succ, path))

    return None


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    fringe =[]
    seen = []

    fringe.append(((problem.get_start_state(), None, 0), []))

    while fringe:
        l_state, path = fringe.pop()
        board = l_state[0]
        move = l_state[1]
        if move is not None:
            path = path + [move]  # add the move object to the path

        seen = seen + [board]
        if problem.is_goal_state(board):
            return path

        successors = problem.get_successors(board)
        for l_succ in successors:
            if l_succ[0] not in seen:
                fringe.insert(0,(l_succ, path))

    return None


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    fringe = PriorityQueue()
    seen = set()

    counter = 0

    fringe.put((0, 0, ([], (problem.get_start_state(), None, 0))))

    while fringe:
        cost, yeah, (path, l_state) = fringe.get()

        board = l_state[0]
        move = l_state[1]

        if move is not None:
            path = path + [move]  # add the move object to the path

        if problem.is_goal_state(board):
                return path

        seen.add(board)

        successors = problem.get_successors(board)
        for l_succ in successors:
            if l_succ[0] not in seen:
                counter = counter + 1
                fringe.put((cost + l_succ[1].piece.num_tiles, counter, (path, l_succ)))


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = PriorityQueue()
    seen = set()

    counter = 0

    fringe.put((0, 0, ([], (problem.get_start_state(), None, 0))))

    while fringe:
        path_g, yeah, (path, l_state) = fringe.get()

        board = l_state[0]
        move = l_state[1]

        path_g = path_g - heuristic((board, move), problem)

        if move is not None:
            path = path + [move]  # add the move object to the path

        if problem.is_goal_state(board):
                return path

        seen.add(board)

        successors = problem.get_successors(board)
        for l_succ in successors:
            if l_succ[0] not in seen:
                # print("current board is:")
                # print(board)
                # print("after move the board will be:")
                # print(l_succ[0])
                g =  path_g + l_succ[1].piece.num_tiles #todo replace path g with counter of -1
                h = heuristic(l_succ, problem)
                counter = counter + 1
                fringe.put((g + h, counter, (path, l_succ)))




# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
