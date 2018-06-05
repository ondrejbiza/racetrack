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

  def test_eventual_finish(self):

    env = environment.Racetrack(racetracks.TRACK_1)

    env.act(0, 1)

    done = False

    for i in range(10000):
      env.act(0, 0)
      print(env.position)
      if env.done:
        done = True
        break

    self.assertTrue(done)