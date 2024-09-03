import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

accel_data = pd.read_csv(r"C:\Users\Gérard Grokoum\pfee-munic\signal\output.csv")
accel_data['Time'] = range(1, len(accel_data) + 1)

signal_x = accel_data['z']


threshold = np.mean(signal_x) + 2 * np.std(signal_x)

signal_filtered = np.where(np.abs(signal_x) >= threshold, signal_x, np.mean(signal_x))

plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')
plt.plot(accel_data['Time'], signal_filtered, color='red', label='Signal X filtré')
plt.xlabel('Time')
plt.ylabel('Signal Value')
plt.title('Signal Filtering using Statistical Threshold')
plt.legend()
plt.grid(True)
plt.show()
