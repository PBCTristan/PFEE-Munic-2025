# Generating data with DonkeyCarSimulator

The objective of this folder is to generate some acceleration and gyroscopic data to use in the training of the simulator.

## Installation

The installation process is as follow : \

1. If you are working on a Windows WSL2 instance, follow the basic setup for Windows of the [official documentation of Donkey Car](http://docs.donkeycar.com/guide/host_pc/setup_windows/). On a Linux machine, this step can be safely skipped. \
2. Install Miniconda3 on your machine. Some help can be found on the [Donkey Car documentation](http://docs.donkeycar.com/guide/host_pc/setup_ubuntu/) (Only run the commands on the first frame, the bash one).
3. Import the conda environment using the `environment.yml` file. To do that simply run the command `conda env create -f environment.yml` in the folder containing the file.
4. Run the `install.sh` file from the `simulator` folder. This should fetch and setup the Gym environment.
5. You should be good to go !

## Running the simulator

To run the simulator and generate data, simply navigate to the scripts folder, and run the scripts from there. The generated data should be saved to the generated\_data folder.
