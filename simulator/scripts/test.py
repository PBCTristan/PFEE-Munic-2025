import os
import gym
import gym_donkeycar
import numpy as np
import json

# SET UP ENVIRONMENT
# You can also launch the simulator separately
# in that case, you don't need to pass a `conf` object
PATH_TO_APP = '../DonkeySimLinux'
exe_path = f"{PATH_TO_APP}/donkey_sim.x86_64"
port = 9091

conf = { "exe_path" : exe_path, "port" : port }

env = gym.make("donkey-generated-track-v0", conf=conf)

# PLAY
for i in range(3):
  obs = env.reset()
  with open(f'generated_data/test_{i}.json', 'w+') as f:
    A = []
    for t in range(100):
      action = np.array([0.0, (i+1) * 0.5]) # drive straight with small speed
      # execute the action
      obs, reward, done, info = env.step(action)
      A.append(info)
    json.dump(A, f)
      
  

# Exit the scene
env.close()
