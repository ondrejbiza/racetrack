import unittest
import racetracks
from environment import RacetrackStrict, Racetrack


class TestRacetrack(unittest.TestCase):

  def test_load_racetrack(self):
    Racetrack(racetracks.TRACK_1)
    Racetrack(racetracks.TRACK_2)

  def test_check_out_of_bounds(self):

    env = Racetrack(racetracks.TRACK_1)

    positions = [(-1, 0), (0, -1), (-1, -1), (env.racetrack.shape[0], 0), (0, env.racetrack.shape[1]),
                 (env.racetrack.shape[0], env.racetrack.shape[1])]
    corrected_positions = [(0, 0), (0, 0), (0, 0), (env.racetrack.shape[0] - 1, 0), (0, env.racetrack.shape[1] - 1),
                           (env.racetrack.shape[0] -1, env.racetrack.shape[1] - 1)]

    for position, corrected_position in zip(positions, corrected_positions):

      env.position = position
      self.assertTrue(env.check_position_out_of_bounds())

      env.correct_position_out_of_bounds()
      self.assertEqual(env.position, corrected_position)

class TestRacetrackStrict(unittest.TestCase):

  def test_load_racetrack(self):

    RacetrackStrict(racetracks.TRACK_1)
    RacetrackStrict(racetracks.TRACK_2)

  def test_correct_route(self):

    env = RacetrackStrict(racetracks.TRACK_1)

    self.assertEqual(env.act(1, 0), RacetrackStrict.STEP_REWARD)

    for _ in range(27):
      self.assertEqual(env.act(0, 0), RacetrackStrict.STEP_REWARD)

    self.assertEqual(env.act(-1, 1), RacetrackStrict.STEP_REWARD)

    while not env.done:
      self.assertEqual(env.act(0, 1), RacetrackStrict.STEP_REWARD)

  def test_collision(self):

    env = RacetrackStrict(racetracks.TRACK_1)

    reward = env.act(1, 1)
    while reward != env.OUT_OF_BOUNDS_REWARD:
      reward = env.act(0, 0)

  def test_check_finish(self):

    env = RacetrackStrict(racetracks.TRACK_1)

    for i in range(5):
      for j in range(3):
        env.position = (i, racetracks.TRACK_1.shape[1] + j)
        self.assertEqual(env.check_finish(), True)
