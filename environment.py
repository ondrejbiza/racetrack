import random
import numpy as np
import matplotlib.pyplot as plt


class Racetrack:

  TRACK_VALUE = 0
  GRASS_VALUE = 1
  START_VALUE = 2
  END_VALUE = 3

  STEP_REWARD = -1
  OUT_OF_BOUNDS_REWARD = -10000

  def __init__(self, racetrack):
    """
    Initialize racetrack environment.
    The environment is described in Sutton and Barto's Reinforcement Learning: Introduction chapter 5.
    To simply the code, I modified the environment so that once the race car leaves the track the episode finishes.
    The book suggest that the race car should be put back on track but that would be difficult to calculate.
    :param racetrack:     Racetrack map.
    """

    self.racetrack = racetrack
    self.start_coordinates = None
    self.get_start_positions()

    self.position = None
    self.velocity = None
    self.done = None
    self.reset()

  def get_start_positions(self):
    """
    Select start position by random (from a list of start positions).
    :return:      None.
    """

    self.start_coordinates = []
    x_coordinates, y_coordinates = np.where(self.racetrack == self.START_VALUE)

    for x, y in zip(x_coordinates, y_coordinates):

      self.start_coordinates.append((x, y))

  def act(self, x_change, y_change):
    """
    Act in the environment.
    :param x_change:    X acceleration.
    :param y_change:    Y acceleration.
    :return:            None.
    """

    assert not self.done

    # validation actions
    assert -1 <= x_change <= 1
    assert -1 <= y_change <= 1

    # update velocity
    self.velocity = (self.velocity[0] + x_change, self.velocity[1] + y_change)
    self.correct_velocity()

    # move car
    self.position = (self.position[0] - self.velocity[0], self.position[1] + self.velocity[1])

    # check if finished
    if self.check_finish():
      self.done = True
      return self.STEP_REWARD

    # check for invalid position
    if self.check_position_out_of_bounds() or self.check_position_grass():
      self.done = True
      return self.OUT_OF_BOUNDS_REWARD

    return self.STEP_REWARD

  def check_finish(self):
    """
    Check if the race car reached finish.
    :return:      None.
    """
    tmp_position = self.position

    if self.position[0] < 0 or self.position[0] >= self.racetrack.shape[0]:
      return False

    if self.position[1] < 0:
      tmp_position = (self.position[0], 0)
    elif self.position[1] >= self.racetrack.shape[1]:
      tmp_position = (self.position[0], self.racetrack.shape[1] - 1)

    if self.racetrack[tmp_position] == self.END_VALUE:
      return True
    else:
      return False

  def correct_velocity(self):
    """
    Correct race car velocity. It cannot be (0, 0) and must be between 0 and 4 for both axes.
    :return:    None.
    """

    # maybe correct the x component
    if self.velocity[0] < 0:
      self.velocity = (0, self.velocity[1])
    elif self.velocity[0] > 4:
      self.velocity = (4, self.velocity[1])

    # maybe correct the y component
    if self.velocity[1] < 0:
      self.velocity = (self.velocity[0], 0)
    elif self.velocity[1] > 4:
      self.velocity = (self.velocity[0], 4)

    # make sure the velocity is not 0
    if self.velocity == (0, 0):
      if random.choice([True, False]):
        self.velocity = (1, 0)
      else:
        self.velocity = (0, 1)

  def check_position_out_of_bounds(self):
    """
    Check if the race car is out of bounds.
    :return:    True if out of bounds, otherwise False.
    """

    return self.position[0] < 0 or self.position[0] >= self.racetrack.shape[0] or self.position[1] < 0 or \
           self.position[1] >= self.racetrack.shape[1]

  def check_position_grass(self):
    """
    Check if the race car is on grass.
    :return:    True if on grass, otherwise False.
    """

    return self.racetrack[self.position] == self.GRASS_VALUE

  def reset(self):
    """
    Reset environment.
    :return:      None.
    """

    self.position = random.choice(self.start_coordinates)
    self.velocity = (0, 0)
    self.done = False

  def show_racetrack(self):

    plt.imshow(self.racetrack)
    plt.show()

  def get_state(self):

    return self.position[0], self.position[1], self.velocity[0], self.velocity[1]