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

def setup_env():
  PATH_TO_APP = '../DonkeySimLinux'
  exe_path = f"{PATH_TO_APP}/donkey_sim.x86_64"
  port = 9091
  conf = { "exe_path" : exe_path, "port" : port }
  return gym.make("donkey-generated-track-v0", conf=conf)


def play_simulation(env, options):
   match options.type:
     case 'straight':
       play_simulation_straight(env, options)
     case 'turn':
       pass
     case 'random':
       pass
     case 'fixed':
       pass

# For now all the function does is setting the throttle to a number, without any variance
def play_simulation_straight(env, options):
  simulations = Simulations.straight(options.number)
  noise = Simulations.noise(options.frames)
  for i, pos in enumerate(simulations):
    _ = env.reset()
    logger.info(f'Running sim number {i}')
    with open(f'generated_data/{options.type}_{i}.json', 'w+') as f:
      r = record.Record(options.type)
      for i in range(options.frames):
        act = pos + noise[i]
        action = np.array(act)
        # execute the action
        _, _, _, info = env.step(action)
        # save the data
        r.add_data(info, act.tolist())
      json.dump(r.to_json(), f)
    # Exit the scene
  env.close()

parser = argparse.ArgumentParser(description='Python utility to generate data from donkey car.')

parser.add_argument('number', type=int, help='The number of files to generate.')
parser.add_argument('type', choices=['straight', 'turn', 'random', 'fixed'], help='How are the tests conducted.')
parser.add_argument('--frames', '-f', required=False, default=100, type=int, help='How many frames to record, better if between 100 and 10000. Default: 100.')
parser.add_argument('--logfile', type=str, required=False, dest='log', help='A file in which to save the logs.')
parser.add_argument('--autologfile', action='store_true', dest='autolog', help='Create the logfiles automatically at a default location. Cannot be used in conjunction with --logfile.')
args = parser.parse_args()

if args.log:
  if (args.autolog):
    raise AssertionError("Cannot use autologfile and logfile at the same time!")
  fileHandler = logging.FileHandler(args.log, mode='w+')
  fileHandler.setLevel(logging.DEBUG)
  logger.addHandler(fileHandler)
elif (args.autolog):
  path = Path('logs')
  if not path.exists():
    logger.warn('./logs path does not exists in current folder. Creating...')
    path.mkdir()
  fileHandler = logging.FileHandler(f'./logs/{datetime.datetime.now().strftime("%Y_%m_%d-%Hh%Mm%Ss.log")}', mode='w+')
  fileHandler.setLevel(logging.DEBUG)
  logger.addHandler(fileHandler)

env = setup_env()
logger.info("Environment created, starting simulation...")
play_simulation(env, args)