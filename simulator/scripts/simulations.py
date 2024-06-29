import numpy as np

class Simulations:
  @staticmethod
  def straight(size):
    steering = np.full(size, 0.0)
    throttle = np.random.normal(0,1,size)
    return np.stack((steering, throttle), axis=-1)
  
  @staticmethod
  def noise(size):
    steering = np.full(size, 0.0)
    throttle = np.random.normal(0,0.25,size)
    return np.stack((steering, throttle), axis=-1)