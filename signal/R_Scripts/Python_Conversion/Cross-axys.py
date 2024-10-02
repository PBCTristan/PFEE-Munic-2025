import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

accel_data = pd.read_csv(r"C:\Users\Gérard Grokoum\pfee-munic\signal\output.csv")

accel_data['Time'] = range(1, len(accel_data) + 1)


signal_z = accel_data['z']
model = LinearRegression()
model.fit(accel_data[['x', 'y']], signal_z)
filtered_signal_z = model.predict(accel_data[['x', 'y']])

signal_x = accel_data['x']
model = LinearRegression()
model.fit(accel_data[['z', 'y']], signal_x)
filtered_signal_x = model.predict(accel_data[['z', 'y']])

signal_y = accel_data['y']
model = LinearRegression()
model.fit(accel_data[['x', 'z']], signal_x)
filtered_signal_y = model.predict(accel_data[['x', 'z']])


plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')

plt.plot(accel_data['Time'], signal_y, color='red', label='Signal Y Original')

plt.plot(accel_data['Time'], signal_z, color='green', label='Signal Z Original')

plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Cross')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))

plt.plot(accel_data['Time'], filtered_signal_x, color='blue', label='Signal X filtré')

plt.plot(accel_data['Time'], filtered_signal_y, color='red', label='Signal Y filtré')

plt.plot(accel_data['Time'], filtered_signal_z, color='green', label='Signal Z filtré')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Cross')
plt.legend()
plt.grid(True)
plt.show()