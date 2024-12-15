import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def saving(input_data, algo, method, signal_filtered_x, signal_filtered_y, signal_filtered_z):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)
    # If we don't want to save our filtered signal and just see it
    if (method == "show"):
        plt.figure(figsize=(10, 6))

        plt.plot(accel_data['Time'], signal_filtered_x, color='blue', label='Signal X filtré')
        plt.plot(accel_data['Time'], signal_filtered_y, color='red', label='Signal Y filtré')
        plt.plot(accel_data['Time'], signal_filtered_z, color='green', label='Signal Z filtré')

        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.title(algo)
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        output_file = input_data.replace(".csv", "_denoised.csv")
        filtered_data = pd.DataFrame({
            'x': signal_filtered_x,
            'y': signal_filtered_y,
            'z': signal_filtered_z
        })
        filtered_data.to_csv(output_file, index=False)