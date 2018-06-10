import argparse
import constants, environment, racetracks


def main(args):

  # validate input
  assert args.racetrack in racetracks.TRACKS.keys()

  track = racetracks.TRACKS[args.racetrack]

  env = environment.Racetrack(track)
  env.show_racetrack(save_path=args.save_path, show_legend=not args.disable_legend)


if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument("racetrack", help="{}, {} or {}".format(constants.RACETRACK_1, constants.RACETRACK_2,
                                                              constants.RACETRACK_3))
  parser.add_argument("-s", "--save-path", help="where to save the figure")
  parser.add_argument("--disable-legend", default=False, action="store_true",
                      help="disable legend in the racetrack image")

  parsed = parser.parse_args()
  main(parsed)