import argparse
import numpy as np
import agent, constants, environment, racetracks


TRAINING_EPISODES = 50000
EVALUATION_EPISODES = 100
EVALUATION_FREQUENCY = 10000

def main(args):

  # validate input
  assert args.racetrack in racetracks.TRACKS.keys()

  # create environment
  track = racetracks.TRACKS[args.racetrack]
  env = environment.Racetrack(track)

  # create agent
  mc = agent.MonteCarlo(env, 0.1)

  print("training for {:d} episodes".format(TRAINING_EPISODES))
  for episode_idx in range(TRAINING_EPISODES):

    # play episode
    mc.play_episode()
    mc.update_policy()

    env.reset()

    # maybe evaluate without exploration
    if episode_idx > 0 and episode_idx % EVALUATION_FREQUENCY == 0:

      returns = []

      for _ in range(EVALUATION_EPISODES):

        ret, _ = mc.play_episode(explore=False, learn=False)
        returns.append(ret)

        env.reset()

      mean_return = np.mean(returns)
      print("mean return after {:d} episodes: {:.2f}".format(episode_idx, mean_return))


  # show an episode starting from each start position
  for i, start_coordinates in enumerate(env.start_coordinates):

    env.reset()
    env.position = start_coordinates

    ret, seq = mc.play_episode(explore=False, learn=False)

    print("episode return: {:.2f}".format(ret))
    save_path = "{:s}_{:d}.{:s}".format(args.save_path, i + 1, args.format)
    mc.show_sequence(seq, save_path=save_path, show_legend=not args.disable_legend)


if __name__ == "__main__":

  parser = argparse.ArgumentParser("Solve racetrack.")

  parser.add_argument("racetrack", help="{}, {} or {}".format(constants.RACETRACK_1, constants.RACETRACK_2,
                                                              constants.RACETRACK_3))
  parser.add_argument("epsilon", type=float, default=0.1, help="exploration constant")

  parser.add_argument("-s", "--save-path", help="where to save plots of episodes")
  parser.add_argument("-f", "--format", default="svg", help="image format")
  parser.add_argument("--disable-legend", default=False, action="store_true",
                      help="disable legend in the racetrack image")

  parsed = parser.parse_args()
  main(parsed)