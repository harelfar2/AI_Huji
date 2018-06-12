# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util
import numpy as np

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0

    states = mdp.getStates()

    for i in range(iterations):
        new_values = util.Counter()
        for state in states:
            chosen_action = self.getAction(state)
            if chosen_action is not None:
                new_values[state] = self.getQValue(state, chosen_action)

        self.values = new_values

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    q_value = 0
    states_probabilities = self.mdp.getTransitionStatesAndProbs(state, action)

    for trans_state, probability in states_probabilities:
        reward = self.mdp.getReward(state, action, trans_state)
        value = self.getValue(trans_state)
        q_value += probability * (reward + self.discount * value)

    return q_value

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    return self.get_action_by_value(state)

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)

  def get_action_by_value(self, state):
      if self.mdp.isTerminal(state):
          return None
      else:
          actions = self.mdp.getPossibleActions(state)
          max_action_value = -np.inf
          max_action = 0

          for action in actions:
              value = self.getQValue(state, action)
              if max_action_value <= value:
                  max_action_value = value
                  max_action = action

          return max_action



