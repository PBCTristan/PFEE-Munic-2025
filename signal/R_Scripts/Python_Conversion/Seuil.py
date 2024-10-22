import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


accel_data = pd.read_csv("/home/thibault/pfee-munic/signal/enzo_1.csv")
accel_data['Time'] = range(1, len(accel_data) + 1)

signal_x = accel_data['x']

threshold = np.mean(signal_x) + 4 * np.std(signal_x)

signal_filtered = np.where(np.abs(signal_x) >= threshold, signal_x, 0)

signal_y = accel_data['y']

threshold = np.abs(np.mean(signal_y)  + 4 * np.std(signal_y))
print(threshold)
signal_filtered_y = np.where(np.abs(signal_y) >= threshold, signal_y, 0)

signal_z = accel_data['z']

threshold = np.mean(signal_z) + 5 * np.std(signal_z)

signal_filtered_z = np.where(np.abs(signal_z) >= threshold, signal_z, 0)

plt.figure(figsize=(10, 6))
#plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')

#plt.plot(accel_data['Time'], signal_y, color='red', label='Signal Y Original')

#plt.plot(accel_data['Time'], signal_z, color='green', label='Signal Z Original')

#plt.xlabel('Time')
#plt.ylabel('Signal')
#plt.title('Seuil')
#plt.legend()
#plt.grid(True)
#plt.show()


plt.figure(figsize=(10, 6))

plt.plot(accel_data['Time'], signal_filtered, color='blue', label='Signal X filtré')
plt.plot(accel_data['Time'], signal_filtered_y, color='red', label='Signal Y filtré')
plt.plot(accel_data['Time'], signal_filtered_z, color='green', label='Signal Z filtré')

plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Seuil')
plt.legend()
plt.grid(True)
plt.show()

fused_signal_euclidian = np.sqrt(signal_filtered**2 + signal_filtered_y**2 + signal_filtered_z**2)
fused_signal_mean = (signal_filtered + signal_filtered_y + signal_filtered_z) / 3

plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], fused_signal_euclidian, label='Fused Signal (Magnitude)', color='purple')

plt.xlabel('Time')
plt.ylabel('Fused value')
plt.title('Fused value (X, Y, Z)')
plt.legend()
plt.show()
