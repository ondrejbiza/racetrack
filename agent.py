import numpy as np
import utils


class MonteCarlo:

  NUM_ACTIONS = 9

  def __init__(self, env, epsilon):
    """
    Each state is visited only once in a single episode, so the first-visit / every-visit distinction does not apply.
    """

    self.env = env
    self.epsilon = epsilon

    self.action_values = None
    self.action_counts = None
    self.policy = None
    self.reset()

  def play_episode(self):

    sequence = []

    while not self.env.done:

      state = self.env.position
      action = self.policy[state]
      reward = self.env.act(*self.action_to_acceleration(action))

      sequence.append((state, action, reward))

    returns = np.zeros(len(sequence))

    for i in reversed(range(len(sequence))):

      for j in range(i + 1):

        returns[j] += sequence[i][2]

    for i in range(len(sequence)):

      state = sequence[i][0]
      action = sequence[i][1]
      ret = returns[i]

      self.action_values[state, action] += utils.update_mean(ret, self.action_values[state, action],
                                                             self.action_counts[state, action])
      self.action_counts[state, action] += 1

    return returns[0]

  def reset(self):

    self.action_values = np.zeros((self.env.racetrack.shape[0], self.env.racetrack.shape[1], self.NUM_ACTIONS),
                                  dtype=np.float32)
    self.action_counts = np.zeros((self.env.racetrack.shape[0], self.env.racetrack.shape[1], self.NUM_ACTIONS),
                                  dtype=np.int32)
    self.policy = np.zeros((self.env.racetrack.shape[0], self.env.racetrack.shape[1]), dtype=np.int32)

  def update_policy(self):

    # play action with maximum action value
    self.policy = np.argmax(self.action_values, axis=-1)

    # choose random action with probability epsilon
    for i in range(self.policy.shape[0]):
      for j in range(self.policy.shape[1]):
        if np.random.uniform(0, 1) < self.epsilon:
          self.policy[i, j] = np.random.choice(list(range(self.NUM_ACTIONS)))

  def action_to_acceleration(self, action):

    assert 0 <= action <= self.NUM_ACTIONS

    if action == 0:
      return -1, -1
    elif action == 1:
      return 0, -1
    elif action == 2:
      return 1, -1
    elif action == 3:
      return -1, 0
    elif action == 4:
      return 0, 0
    elif action == 5:
      return 1, 0
    elif action == 6:
      return -1, 1
    elif action == 7:
      return 0, 1
    elif action == 8:
      return 1, 1