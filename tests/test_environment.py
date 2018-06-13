import unittest
import constants, racetracks
from environment import RacetrackStrict, Racetrack


class TestRacetrack(unittest.TestCase):

  def test_load_racetrack(self):
    Racetrack(racetracks.TRACKS[constants.RACETRACK_2])
    Racetrack(racetracks.TRACKS[constants.RACETRACK_3])

  def test_eventual_finish(self):

    env = Racetrack(racetracks.TRACKS[constants.RACETRACK_2])

    for i in range(20):
      env.reset()

      while not env.done:
        env.act(0, 0)

class TestRacetrackStrict(unittest.TestCase):

  def test_load_racetrack(self):

    RacetrackStrict(racetracks.TRACKS[constants.RACETRACK_2])
    RacetrackStrict(racetracks.TRACKS[constants.RACETRACK_3])

  def test_correct_route(self):

    env = RacetrackStrict(racetracks.TRACKS[constants.RACETRACK_2])

    self.assertEqual(env.act(1, 0), RacetrackStrict.STEP_REWARD)

    for _ in range(27):
      self.assertEqual(env.act(0, 0), RacetrackStrict.STEP_REWARD)

    self.assertEqual(env.act(-1, 1), RacetrackStrict.STEP_REWARD)

    while not env.done:
      self.assertEqual(env.act(0, 1), RacetrackStrict.STEP_REWARD)

  def test_collision(self):

    env = RacetrackStrict(racetracks.TRACKS[constants.RACETRACK_2])

    reward = env.act(1, 1)
    while reward != env.OUT_OF_BOUNDS_REWARD:
      reward = env.act(0, 0)

  def test_check_finish(self):

    env = RacetrackStrict(racetracks.TRACKS[constants.RACETRACK_2])

    for i in range(5):
      for j in range(3):
        env.position = (i, racetracks.TRACKS[constants.RACETRACK_2].shape[1] + j)
        self.assertEqual(env.check_finish(), True)