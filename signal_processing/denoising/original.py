import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def original(input_data):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)
    signal_x = accel_data['x']
    #signal_x = signal_x.iloc[:100]
    #print(signal_x[signal_x.index<100])
    signal_y = accel_data['y']
    signal_z = accel_data['z']
    plt.figure(figsize=(10, 6))

    plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')
    plt.plot(accel_data['Time'], signal_y, color='red', label='Signal Y Original')
    plt.plot(accel_data['Time'], signal_z, color='green', label='Signal Z Original')

    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.title('Seuil')
    plt.legend()
    plt.grid(True)
    plt.show()