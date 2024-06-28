import argparse
import logging
import psutil
import sys
from subprocess import Popen

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s')
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

parser = argparse.ArgumentParser(description='Python utility to generate data from donkey car')

parser.add_argument('launch_location', type=str, help='The from which to launch drive.py')
parser.add_argument('number', type=int, help='The number of files to generate')
parser.add_argument('directory', type=str, help='Directory in which to store the generated files')
parser.add_argument('--log_file', metavar='l', dest='log', type=str, required=False, default='/home/garice/donkey_car.log')
parser.add_argument('--prefix', metavar='p', type=str, required=False, default='donkey_generated', help='The prefix of the generated files')
args = parser.parse_args()

def start_donkey():
    if (any(map(lambda x : x.name == 'donkey_sim.x86_64', psutil.process_iter()))):
        logger.info('Donkey Sim is already running, skipping...')
    else:
        f = open(args.log, 'x')
        p = Popen(['python', f'{args.launch_location}/manage.py', 'drive'], stdout=f)
        p.wait()
        f.close()


start_donkey()