import numpy as np
import abc
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        cur_board = current_game_state.board
        succ_board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        diff = abs(cur_board - succ_board)
        minus_diff = np.sum(diff)

        count = 0

        for row in range(4):
            for col in range(4):
                count -= count_smaller_surround(col, row, succ_board, succ_board[row][col]) * succ_board[row][col]

        return count

def count_smaller_surround(col, row, board, tile):
    surrounding = [(row,col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    count = 0
    for s_tile in surrounding:
        s_row, s_col = s_tile
        try:
            if board[s_row][s_col] < tile:
                count += 1
        except:
            continue

    return count


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """

        return self.minimax(game_state, self.depth * 2 ,0)[2]


    def minimax(self, state, curr_depth, player):
        if curr_depth == 0:
            return (self.evaluation_function(state), state , Action.STOP)

        best_value = -float('inf')
        best_state = None
        best_action = None
        actions = state.get_legal_actions(player)
        succ_states = [state.generate_successor(player, action) for action in actions]

        for index, succ in enumerate(succ_states):
            value, drop, drop2 = self.minimax(succ, curr_depth - 1, abs(1 - player))
            if player == 1:
                value = -value

            if value > best_value:
                best_state = succ
                best_value = value
                best_action = actions[index]

        return (best_value, best_state, best_action)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""
        return self.alphabeta(game_state, self.depth * 2 ,0, -float('inf'), float('inf'))[2]


    def alphabeta(self, state, curr_depth, player, alpha, beta):
        if curr_depth == 0:
            return (self.evaluation_function(state), state , Action.STOP)

        best_value = -float('inf')
        best_state = None
        best_action = None
        actions = state.get_legal_actions(player)
        succ_states = [state.generate_successor(player, action) for action in actions]

        for index, succ in enumerate(succ_states):
            value, drop, drop2 = self.alphabeta(succ, curr_depth - 1, abs(1 - player), -beta, -alpha)
            if player == 1:
                value = -value

            if value > best_value:
                best_state = succ
                best_value = value
                best_action = actions[index]

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return (best_value, best_state, best_action)



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        util.raiseNotDefined()





def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = better_evaluation_function
