import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import constants


class Racetrack:

  STEP_REWARD = -1
  OUT_OF_BOUNDS_REWARD = -50

  def __init__(self, racetrack, random_displacement_probability=0.5):
    """
    Initialize racetrack environment.
    The environment is described in Sutton and Barto's Reinforcement Learning: Introduction chapter 5.
    :param racetrack:                           Racetrack map.
    :param random_displacement_probability:     Probability of a random displacement by one square up or right.
    """

    self.racetrack = racetrack
    self.random_displacement_probability = random_displacement_probability
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
    x_coordinates, y_coordinates = np.where(self.racetrack == constants.START_VALUE)

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
    last_position = self.position
    self.update_position(self.velocity)
    self.random_displacement()

    # check if finished
    if self.check_finish():
      self.done = True
      return self.STEP_REWARD

    # check for invalid position
    invalid_position = False

    if self.check_position_out_of_bounds() or self.check_position_grass():
      invalid_position = True
      self.correct_invalid_position(last_position)
      self.correct_same_position()

    # check if finished again
    if self.check_finish():
      self.done = True

      if invalid_position:
        return self.OUT_OF_BOUNDS_REWARD
      else:
        return self.STEP_REWARD

    if invalid_position:
      return self.OUT_OF_BOUNDS_REWARD
    else:
      return self.STEP_REWARD

  def update_position(self, velocity):
    """
    Update position based on the velocity.
    :param velocity:      Velocity.
    :return:    None.
    """

    self.position = (self.position[0] - velocity[0], self.position[1] + velocity[1])

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

    if self.racetrack[tmp_position] == constants.END_VALUE:
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

    return self.racetrack[self.position] == constants.GRASS_VALUE

  def correct_invalid_position(self, last_position):
    """
    Correct position that is out of bounds or on grass.
    :param last_position:       Last position.
    :return:                    None.
    """

    self.position = last_position
    self.velocity = (0, 0)

  def correct_same_position(self):
    """
    Move the car by at least one square to its target (so that each episode eventually finishes).
    :return:    None.
    """

    self.update_position((1, 0))

    if self.check_position_out_of_bounds() or self.check_position_grass():
      self.update_position((-1, 1))

  def random_displacement(self):
    """
    Sometimes displace the car by one square up or right.
    :return:    None.
    """

    if np.random.uniform(0, 1) < self.random_displacement_probability:
      if np.random.choice([True, False]):
        self.update_position((1, 0))
      else:
        self.update_position((0, 1))

  def reset(self):
    """
    Reset environment.
    :return:      None.
    """

    self.position = random.choice(self.start_coordinates)
    self.velocity = (0, 0)
    self.done = False

  def show_racetrack(self, save_path=None, show_legend=True):
    """
    Show the racetrack with labels.
    https://stackoverflow.com/questions/25482876/how-to-add-legend-to-imshow-in-matplotlib
    :param save_path:     Where to save the figure.
    :param show_legend:   Show legend.
    :return:              None.
    """

    im =  plt.imshow(self.racetrack)

    plt.axis("off")

    if show_legend:
      values = np.unique(self.racetrack.ravel())
      labels = {
        constants.START_VALUE: "start",
        constants.END_VALUE: "end",
        constants.TRACK_VALUE: "track",
        constants.GRASS_VALUE: "grass"
      }
      colors = [im.cmap(im.norm(value)) for value in values]
      patches = [mpatches.Patch(color=colors[i], label=labels[values[i]]) for i in range(len(values))]
      plt.legend(handles=patches, loc=4)

    if save_path is not None:
      plt.savefig(save_path, bbox_inches="tight")

    plt.show()

  def get_state(self):
    """
    Get current state (position and velocity).
    :return:    Current state.
    """

    return self.position[0], self.position[1], self.velocity[0], self.velocity[1]

class RacetrackStrict(Racetrack):

  STEP_REWARD = -1
  OUT_OF_BOUNDS_REWARD = -50

  def __init__(self, racetrack):
    """
    Initialize racetrack environment.
    The environment is described in Sutton and Barto's Reinforcement Learning: Introduction chapter 5.
    This version of the environment terminates when the car attempts to leave the track.
    However, there are not random displacements.
    :param racetrack:     Racetrack map.
    """

    Racetrack.__init__(self, racetrack)


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
    self.update_position(self.velocity)

    # check if finished
    if self.check_finish():
      self.done = True
      return self.STEP_REWARD

    # check for invalid position
    if self.check_position_out_of_bounds() or self.check_position_grass():
      self.done = True
      return self.OUT_OF_BOUNDS_REWARD

    return self.STEP_REWARD