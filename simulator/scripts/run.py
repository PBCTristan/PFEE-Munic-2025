import argparse
import logging
import os
import gym
import gym_donkeycar
import numpy as np
import json
import record
from simulations import Simulations
import sys
import datetime
from pathlib import Path


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)


def setup_env(env_name):
    exe_path = "../DonkeySimLinux/donkey_sim.x86_64"
    port = 9091
    conf = {"exe_path": exe_path, "port": port, "max_cte": sys.maxsize}
    return gym.make(env_name, conf=conf)


def play_simulation(env, options):
    match options.type:
        case "straight":
            play_simulation_straight(env, options)
        case "turn":
            pass
        case "random":
            play_simulation_random(env, options)
        case "fixed":
            pass


# For now all the function does is setting the throttle to a number, without any variance
def play_simulation_straight(env, options):
    simulations = Simulations.straight(options.number)
    noise = Simulations.noise(options.frames)
    for i, pos in enumerate(simulations):
        _ = env.reset()
        logger.info(f"Running sim number {i}")
        with open(f"generated_data/{options.type}_{i}.json", "w+") as f:
            r = record.Record(options.type)
            for i in range(options.frames):
                act = pos + noise[i]
                action = np.array(act)
                # execute the action
                _, _, done, info = env.step(action)
                print(info["hit"])
                # save the data
                r.add_data(info, act.tolist())
            json.dump(r.to_json(), f)
        # Exit the scene
    env.close()


def play_simulation_random(env, options):
    logger.info("playing simu with random curve")
    simulations = Simulations.randomTurnAngle(options.number)
    noise = Simulations.noise(options.frames)
    for i, pos in enumerate(simulations):
        # Reset the environment
        env.reset()
        logger.info(f"Running sim number {i}")
        with open(f"generated_data/{options.type}_{i}.json", "w+") as f:
            r = record.Record(options.type)
            for _ in range(options.frames):
                # Select an action
                
                act = pos + noise[i]
                action = np.array(act)
                
                # execute the action
                obv, reward, done, info = env.step(action)
                r.add_data(info, action.tolist())
            json.dump(r.to_json(), f)
    env.close()


if __name__ == "__main__":
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

    parser.add_argument("number", type=int, help="The number of files to generate.")
    parser.add_argument(
        "type",
        choices=["straight", "turn", "random", "fixed"],
        help="How are the tests conducted.",
    )
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
    args = parser.parse_args()

    if args.log:
        if args.autolog:
            raise AssertionError("Cannot use autologfile and logfile at the same time!")
        fileHandler = logging.FileHandler(args.log, mode="w+")
        fileHandler.setLevel(logging.DEBUG)
        logger.addHandler(fileHandler)
    elif args.autolog:
        path = Path("logs")
        if not path.exists():
            logger.warn("./logs path does not exists in current folder. Creating...")
            path.mkdir()
        fileHandler = logging.FileHandler(
            f'./logs/{datetime.datetime.now().strftime("%Y_%m_%d-%Hh%Mm%Ss.log")}',
            mode="w+",
        )
        fileHandler.setLevel(logging.DEBUG)
        logger.addHandler(fileHandler)

    if args.env != "all":
        env = setup_env(args.env)
        logger.info("Environment created, starting simulation...")
        play_simulation(env, args)
    else:
        for env_name in env_list:
            env = setup_env(env_name)
            logger.info(f"Environment {env_name} created, starting simulation...")
            play_simulation(env, args)
