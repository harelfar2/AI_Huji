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

class SearchNode:

    def __init__(self, state, move, father, cost):
        self.state = state
        self.move = move
        self.father = father
        self.cost = cost

def get_path(node):

    path = []
    while node.father is not None:
        path += [node.move]
        node = node.father

    return path[::-1]


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

    fringe = util.Stack()
    seen = set()

    fringe.push(SearchNode(problem.get_start_state(), None, None, 0))

    while fringe:

        current_node = fringe.pop()

        if problem.is_goal_state(current_node.state):
            return get_path(current_node)

        if current_node.state in seen:
            continue

        seen.add(current_node.state)

        successors = problem.get_successors(current_node.state)
        for l_succ in successors:
            node = SearchNode(l_succ[0], l_succ[1], current_node, 0)
            fringe.push(node)

    return []


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    fringe = util.Queue()
    seen = set()

    fringe.push(SearchNode(problem.get_start_state(), None, None, 0))

    while fringe:

        current_node = fringe.pop()

        if problem.is_goal_state(current_node.state):
            return get_path(current_node)

        if current_node.state in seen:
            continue

        seen.add(current_node.state)

        successors = problem.get_successors(current_node.state)
        for l_succ in successors:
            node = SearchNode(l_succ[0], l_succ[1], current_node, 0)
            fringe.push(node)

    return []


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    fringe = util.PriorityQueue()
    seen = set()

    fringe.push(SearchNode(problem.get_start_state(), None, None, 0), 0)

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
            node = SearchNode(succ[0], succ[1], current_node, g)

            fringe.push(node, g)

    return []


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
    fringe = util.PriorityQueue()
    seen = set()

    fringe.push(SearchNode(problem.get_start_state(), None, None, 0), 0)

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
            h = heuristic(succ[0], problem)
            node = SearchNode(succ[0], succ[1], current_node, g)

            fringe.push(node, g + h)

    return []


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
