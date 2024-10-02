import argparse


def create_argument_parser():
    env_list = [
        "donkey-warehouse-v0",
        "donkey-generated-roads-v0",
        "donkey-avc-sparkfun-v0",
        "donkey-generated-track-v0",
        "donkey-roboracingleague-track-v0",
        "donkey-waveshare-v0",
        "donkey-minimonaco-track-v0",
        "donkey-warren-track-v0",
        "donkey-circuit-launch-track-v0",
    ]

    parser = argparse.ArgumentParser(
        description="Python utility to generate data from donkey car."
    )

    parser.add_argument("--number",
        type=lambda x: list(map(lambda y: y if y >= 0 else 0, map(int, x.split(',')))),
        default=[1,1,1],
        required=False,
        help="comma seperated numbers of files to generate for each test type. ex:[X:straight, Y:turn, Z:random]\nDefault to 1,1,1"
    )
    # parser.add_argument(
    #     "type",
    #     choices=["straight", "turn", "random", "fixed"],
    #     help="How are the tests conducted.",
    # )
    parser.add_argument(
        "--env",
        choices=env_list + ["all"],
        default="donkey-generated-track-v0",
        help="Which map is used.",
    )
    parser.add_argument(
        "--frames",
        "-f",
        required=False,
        default=100,
        type=int,
        help="How many frames to record, better if between 100 and 10000. Default: 100.",
    )
    parser.add_argument(
        "--logfile",
        type=str,
        required=False,
        dest="log",
        help="A file in which to save the logs.",
    )
    parser.add_argument(
        "--autologfile",
        action="store_true",
        dest="autolog",
        help="Create the logfiles automatically at a default location. Cannot be used in conjunction with --logfile.",
    )
    parser.add_argument(
        "--noise",
        "-n",
        action="store_true",
        required=False,
        dest="noise",
        help="Whether to add artificial noise to the accelerometer data",
    )

    return parser, env_list
