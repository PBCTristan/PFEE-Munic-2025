import logging
import numpy as np
import record
import json
import gym
import gym_donkeycar

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
        steering = np.random.uniform(-1, 1, size)
        throttle = np.random.uniform(size=size)
        return np.stack((steering, throttle), axis=-1)

    @staticmethod
    def noise(size):
        steering = np.full(size, 0.0)
        throttle = np.random.uniform(-0.1, 0.1, size)
        return np.stack((steering, throttle), axis=-1)

    @staticmethod
    def simulationEnumarates(simulations, noise, env, options, simu_type: int):
        simu_type_str = "straight"
        match simu_type:
            case 1:
                simu_type_str = "turn"
            case 2:
                simu_type_str = "random"
        
        for i, pos in enumerate(simulations):
            # Reset the environment
            env.reset()

            # simulation actions
            act = pos + noise[i]
            action = np.array(act)

            logger.info(f"Running sim number {i}")
            with open(
                f"generated_data/{simu_type_str}_{env.spec.id}_{i}.json", "w+"
            ) as f:
                r = record.Record(simu_type_str)
                for _ in range(options.frames):

                    # execute the action
                    obv, reward, done, info = env.step(action)
                    if info["hit"] != "none":
                        # hit detected, cutting motor by setting vector to 0
                        action = np.full(options.number[simu_type], 0.0)

                    r.add_data(info)
                json.dump(r.to_json(), f)
