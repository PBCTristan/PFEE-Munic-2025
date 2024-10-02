import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


accel_data = pd.read_csv(r"C:\Users\Gérard Grokoum\pfee-munic\signal\outpute.csv")
accel_data['Time'] = range(1, len(accel_data) + 1)

signal_x = accel_data['x']

threshold = np.mean(signal_x) + 2 * np.std(signal_x)

signal_filtered = np.where(np.abs(signal_x) >= threshold, signal_x, np.mean(signal_x))

signal_y = accel_data['y']

threshold = np.mean(signal_y) + 2 * np.std(signal_y)

signal_filtered_y = np.where(np.abs(signal_y) >= threshold, signal_y, np.mean(signal_y))

signal_z = accel_data['z']

threshold = np.mean(signal_z) + 2 * np.std(signal_z)

signal_filtered_z = np.where(np.abs(signal_z) >= threshold, signal_z, np.mean(signal_z))

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


plt.figure(figsize=(10, 6))

plt.plot(accel_data['Time'], signal_filtered, color='blue', label='Signal X filtré')

"""plt.plot(accel_data['Time'], signal_filtered_y, color='red', label='Signal Y filtré')"""

"""plt.plot(accel_data['Time'], signal_filtered_z, color='green', label='Signal Z filtré')"""
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Seuil')
plt.legend()
plt.grid(True)
plt.show()
