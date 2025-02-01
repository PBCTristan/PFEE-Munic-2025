import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def saving(method, dataframe):

    dataframe['Time'] = range(1, len(dataframe) + 1)
    signal_x = dataframe['accel_x']
    signal_y = dataframe['accel_y']
    signal_z = dataframe['accel_z']
    # If we don't want to save our filtered signal and just see it
    if (method == "show"):
        plt.figure(figsize=(10, 6))

        plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X')
        plt.plot(accel_data['Time'], signal_y, color='red', label='Signal Y')
        plt.plot(accel_data['Time'], signal_z, color='green', label='Signal Z')

        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.title(algo)
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        filtered_data = pd.DataFrame({
            'x': signal_x,
            'y': signal_y,
            'z': signal_z
        })
        filtered_data.to_csv("result.csv", index=False)
