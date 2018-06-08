import numpy as np
import agent, environment, racetracks


SOLVE_RETURN = -12
TRAINING_EPISODES = 500000
EVALUATION_EPISODES = 10
EVALUATION_FREQUENCY = 10000


env = environment.Racetrack(racetracks.TRACK_1)
mc = agent.MonteCarlo(env, 1.0)

max_ret = None

for i in range(TRAINING_EPISODES):

  mc.play_episode()
  mc.update_policy()

  env.reset()

  if i > 0 and i % EVALUATION_FREQUENCY == 0:

    returns = []

    for j in range(EVALUATION_EPISODES):

      ret, _ = mc.play_episode(explore=False, learn=False)
      returns.append(ret)

      env.reset()

    total_return = np.mean(returns)
    print("return after {:d} episodes: {:.2f}".format(i, total_return))

for i in range(10):

  ret, seq = mc.play_episode(explore=False, learn=False)
  print("return", ret)
  mc.show_sequence(seq)
  env.reset()

mc.show_fraction_explored()
mc.show_max_action_values()