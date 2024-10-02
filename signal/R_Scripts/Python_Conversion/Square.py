import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
accel_data = pd.read_csv(r"C:\Users\Gérard Grokoum\pfee-munic\signal\output.csv")
accel_data['Time'] = range(1, len(accel_data) + 1)

signal_x = accel_data['x']
degree = 20
coefficients = np.polyfit(accel_data['Time'], signal_x, degree)
poly_model = np.poly1d(coefficients)

signal_filtered_x = poly_model(accel_data['Time'])

signal_y = accel_data['y']
degree = 20
coefficients = np.polyfit(accel_data['Time'], signal_y, degree)
poly_model = np.poly1d(coefficients)

signal_filtered_y = poly_model(accel_data['Time'])

signal_z = accel_data['z']
degree = 20
coefficients = np.polyfit(accel_data['Time'], signal_z, degree)
poly_model = np.poly1d(coefficients)

signal_filtered_z = poly_model(accel_data['Time'])



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

plt.plot(accel_data['Time'], signal_filtered_x, color='blue', label='Signal X filtré')

plt.plot(accel_data['Time'], signal_filtered_y, color='red', label='Signal Y filtré')

plt.plot(accel_data['Time'], signal_filtered_z, color='green', label='Signal Z filtré')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Seuil')
plt.legend()
plt.grid(True)
plt.show()