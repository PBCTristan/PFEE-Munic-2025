import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
accel_data = pd.read_csv(r"C:\Users\Gérard Grokoum\pfee-munic\signal\output.csv")
accel_data['Time'] = range(1, len(accel_data) + 1)

signal_x = accel_data['z']


degree = 20
coefficients = np.polyfit(accel_data['Time'], signal_x, degree)
poly_model = np.poly1d(coefficients)

signal_filtered = poly_model(accel_data['Time'])


plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')

plt.plot(accel_data['Time'], signal_filtered, color='red', label='Signal X filtré')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Square')
plt.legend()
plt.grid(True)
plt.show()
