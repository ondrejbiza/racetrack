import agent, environment, racetracks


SOLVE_RETURN = -12

env = environment.Racetrack(racetracks.TRACK_1)
mc = agent.MonteCarlo(env, 1.0)

max_ret = None

for i in range(10000000):

  if i > 0 and i % 10000 == 0:
    print("episode", i)

  ret = mc.play_episode()
  mc.update_policy()

  if max_ret is None or ret > max_ret:
    max_ret = ret
    print("new maximum return:", max_ret, "episode", i)

  env.reset()