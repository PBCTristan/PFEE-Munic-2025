import argparse
import logging
import gym
import numpy as np
import json
import record
from simulations import Simulations
import sys
import datetime
from pathlib import Path
from pid import PID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)


def setup_env(env_name):
    exe_path = "../DonkeySimLinux/donkey_sim.x86_64"
    port = 9091
    # We need throttle min to -1 to simulate braking
    conf = {"exe_path": exe_path, "port": port, "max_cte": sys.maxsize, "throttle_min": -1.0}
    return gym.make(env_name, conf=conf)


def play_simulation(env, options):
    match options.type:
        case "straight":
            play_simulation_straight(env, options)
        case "turn":
            play_simulation_turn(env, options)
        case "random":
            play_simulation_random(env, options)
        case "brake":
            play_simulation_brake(env, options)


# For now all the function does is setting the throttle to a number, without any variance
def play_simulation_straight(env, options):
    simulations = Simulations.straight(options.number)
    noise = Simulations.noise(options.frames)
    Simulations.simulationEnumarates(simulations, noise, env, options)
    env.close()


def play_simulation_turn(env, options):
    logger.info("playing simu with random curve")
    simulations = Simulations.randomTurnAngle(options.number)
    noise = Simulations.noise(options.frames)
    Simulations.simulationEnumarates(simulations, noise, env, options)
    env.close()


def play_simulation_random(env, options):
    for i in range(options.number):
        # Reset the environment
        _ = env.reset()
        logger.info(f"Running sim number {i}")
        with open(f"generated_data/random_{env.spec.id}_iter_{i}.json", "w+") as f:
            r = record.Record(options.type)
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
                hit = info["hit"]
                r.add_data(info)
            json.dump(r.to_json(), f)
    env.close()

def play_simulation_brake(env, options):
    for i in range(options.number):
        # Reset the environment
        _ = env.reset()
        logger.info(f"Running sim number {i}")
        with open(f"generated_data/brake_{env.spec.id}_iter_{i}.json", "w+") as f:
            r = record.Record(options.type)
            info = None
            acceleration_value = np.random.uniform()
            acceleration_frames = np.random.randint(10, options.frames // 2)
            for _ in range(acceleration_frames):
                action = [0, acceleration_value]
                # execute the action
                _, _, _, info = env.step(action)
                r.add_data(info)
            # Create a PID instance to control speed
            pid = PID(2, 0.2, 0.3, 1.0, -1.0, 0.1)
            command = None
            for _ in range(acceleration_frames, options.frames):
                speed = info["speed"]
                print(pid.values())
                command = pid.update(speed, 0.01)
                action = [0, command]
                _, _, _, info = env.step(action)
                r.add_data(info)
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
        choices=["straight", "turn", "random", "brake"],
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
