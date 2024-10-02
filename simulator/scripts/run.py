import argparse
import logging
import gym
import numpy as np
import json
import record
from simulations import Simulations
from arg_parser import create_argument_parser
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
    if (options.number[0] != 0):
        play_simulation_straight(env, options)
    if (options.number[1] != 0):
        play_simulation_turn(env, options)
    if (options.number[2] != 0):
        play_simulation_random(env, options)
    env.close()


# For now all the function does is setting the throttle to a number, without any variance
def play_simulation_straight(env, options):
    simulations = Simulations.straight(options.number[0])
    noise = Simulations.noise(options.frames)
    Simulations.simulationEnumarates(simulations, noise, env, options, 0)


def play_simulation_turn(env, options):
    logger.info("playing simu with random curve")
    simulations = Simulations.randomTurnAngle(options.number[1])
    noise = Simulations.noise(options.frames)
    Simulations.simulationEnumarates(simulations, noise, env, options, 1)


def play_simulation_random(env, options):
    for i in range(options.number[2]):
        # Reset the environment
        _ = env.reset()
        logger.info(f"Running sim number {i}")
        with open(f"generated_data/random_{env.spec.id}_iter_{i}.json", "w+") as f:
            r = record.Record("random")
            last_action = [0, 0]
            hit = "none"
            for _ in range(options.frames):
                action = [0, 0]
                if hit == "none":
                    action = np.clip(
                        last_action + (env.action_space.sample() * 0.15), -1, 1
                    )
                last_action = action
                # execute the action
                _, _, _, info = env.step(action)
                if options.noise:
                    # random sample between -0.1 and 0.1 (do not simplify the line for lisibility)
                    info["accel"] += (0.1 + 0.1) * np.random.random_sample((3,)) - 0.1
                    info["accel"] = (info["accel"]).tolist()
                hit = info["hit"]
                r.add_data(info)
            json.dump(r.to_json(), f)


if __name__ == "__main__":
    parser, env_list = create_argument_parser()
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
            logger.warning("./logs path does not exists in current folder. Creating...")
            path.mkdir()
        fileHandler = logging.FileHandler(
            f'./logs/{datetime.datetime.now().strftime("%Y_%m_%d-%Hh%Mm%Ss.log")}',
            mode="w+",
        )
        fileHandler.setLevel(logging.DEBUG)
        logger.addHandler(fileHandler)

    if (len(args.number) < 3):
        while (len(args.number) < 3):
            args.number.append(0)
    
    print(f"numbers of runs for each type: {args.number}")

    if args.env != "all":
        env = setup_env(args.env)
        logger.info("Environment created, starting simulation...")
        play_simulation(env, args)
    else:
        for env_name in env_list:
            env = setup_env(env_name)
            logger.info(f"Environment {env_name} created, starting simulation...")
            play_simulation(env, args)
