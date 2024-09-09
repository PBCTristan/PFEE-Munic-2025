import logging
import numpy as np

logger = logging.getLogger(__name__)

class Simulations:
  @staticmethod
  def straight(size):
    logger.info("Generating random inputs")
    steering = np.full(size, 0.0)
    throttle = np.random.uniform(size=size)
    return np.stack((steering, throttle), axis=-1)
  
  @staticmethod
  def randomTurnAngle(size):
    logger.info("Generating random inputs")
    steering = np.random.normal(-1,1, size)
    throttle = np.random.uniform(size=size)
    return np.stack((steering, throttle), axis=-1)

  
  @staticmethod
  def noise(size):
    steering = np.full(size, 0.0)
    throttle = np.random.uniform(-0.1,0.1,size)
    return np.stack((steering, throttle), axis=-1)