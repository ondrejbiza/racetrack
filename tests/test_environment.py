import unittest
import environment, racetracks


class TestEnvironment(unittest.TestCase):

  def test_load_racetrack(self):

    environment.Racetrack(racetracks.TRACK_1)
    environment.Racetrack(racetracks.TRACK_2)

  def test_correct_route(self):

    env = environment.Racetrack(racetracks.TRACK_1)

    self.assertEqual(env.act(1, 0), -1)

    for _ in range(27):
      self.assertEqual(env.act(0, 0), -1)

    self.assertEqual(env.act(-1, 1), -1)

    while not env.done:
      self.assertEqual(env.act(0, 0), -1)

  def test_collision(self):

    env = environment.Racetrack(racetracks.TRACK_1)

    self.assertEqual(env.act(1, 1), -1)

    reward = env.act(0, 0)
    while reward != env.OUT_OF_BOUNDS_REWARD:
      reward = env.act(0, 0)