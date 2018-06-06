import agent, environment, racetracks


env = environment.Racetrack(racetracks.TRACK_1)
mc = agent.MonteCarlo(env, 0.1)

max_ret = None

for i in range(10000000):

  ret = mc.play_episode()
  mc.update_policy()

  if max_ret is None or ret > max_ret:
    max_ret = ret
    print("new maximum return:", max_ret, "episode", i)

  env.reset()