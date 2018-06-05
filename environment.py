import random
import numpy as np
import racetracks


class Racetrack:

  TRACK_VALUE = 0
  GRASS_VALUE = 1
  START_VALUE = 2
  END_VALUE = 3

  STEP_REWARD = -1
  OUT_OF_BOUNDS_REWARD = -5

  def __init__(self, racetrack):

    self.racetrack = racetrack
    self.start_coordinates = None
    self.get_start_positions()

    self.position = None
    self.velocity = None
    self.done = None
    self.reset()

  def get_start_positions(self):

    self.start_coordinates = []
    x_coordinates, y_coordinates = np.where(self.racetrack == self.START_VALUE)

    for x, y in zip(x_coordinates, y_coordinates):

      self.start_coordinates.append((x, y))

  def act(self, x_change, y_change):

    assert not self.done

    # validation actions
    assert -1 <= x_change <= 1
    assert -1 <= y_change <= 1

    # update velocity
    self.velocity = (self.velocity[0] + x_change, self.velocity[1] + y_change)
    self.correct_velocity()

    # move car
    last_position = self.position
    self.position = (self.position[0] - self.velocity[0], self.position[1] + self.velocity[1])

    # correct position
    x_out_of_bounds, y_out_of_bounds = self.correct_position_out_of_bounds()
    correct = self.correct_position_grass()
    self.correct_same_position(last_position)

    # check if finished
    if self.racetrack[self.position] == self.END_VALUE:

      self.done = True

      if y_out_of_bounds or not correct:
        return self.OUT_OF_BOUNDS_REWARD
      else:
        return self.STEP_REWARD

    # calculate rewards
    if x_out_of_bounds or y_out_of_bounds or not correct:
      return self.OUT_OF_BOUNDS_REWARD
    else:
      return self.STEP_REWARD

  def correct_velocity(self):

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
        self.velocity = (self.velocity[0] + 1, self.velocity[1])
      else:
        self.velocity = (self.velocity[0], self.velocity[1] + 1)

  def correct_position_out_of_bounds(self):

    correct_x = False
    correct_y = False

    if self.position[0] < 0:
      self.position = (0, self.position[1])
      correct_x = True
    elif self.position[0] >= self.racetrack.shape[0]:
      self.position = (self.racetrack.shape[0] - 1, self.position[1])
      correct_x = True

    if self.position[1] < 0:
      self.position = (self.position[0], 0)
      correct_y = True
    elif self.position[1] >= self.racetrack.shape[1]:
      self.position = (self.position[0], self.racetrack.shape[1] - 1)
      correct_y = True

    return correct_x, correct_y

  def correct_position_grass(self):

    if self.racetrack[self.position] == self.GRASS_VALUE:

      print("problem velocity", self.velocity)

      # backtrack movement along x axis
      for x in range(1, self.velocity[0]):
        if self.racetrack[self.position[0] + x, self.position[1]] != self.GRASS_VALUE:
          self.position = (self.position[0] + x, self.position[1])
          return False

      # backtrack movement along y axis
      for y in range(1, self.velocity[1]):
        if self.racetrack[self.position[0], self.position[1] - y] != self.GRASS_VALUE:
          self.position = (self.position[0], self.position[1] - y)
          return False

      raise ValueError("This should not happen.")

    return True

  def correct_same_position(self, last_position):

    if self.position == last_position:

      if self.racetrack[self.position[0] - 1, self.position[1]] != self.GRASS_VALUE:

        self.position = (self.position[0] - 1, self.position[1])

      else:

        self.position = (self.position[0], self.position[1] + 1)

  def reset(self):

    self.position = random.choice(self.start_coordinates)
    self.velocity = (0, 0)
    self.done = False
