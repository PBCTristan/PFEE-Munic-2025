import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

accel_data = pd.read_csv(r"C:\Users\tanth\pfee-munic\signal\output.csv")

accel_data['Time'] = range(1, len(accel_data) + 1)
signal_x = accel_data['z']

noise_level = 0.5
noisy_signal_x = accel_data['z'] + np.random.normal(loc=0, scale=noise_level, size=len(accel_data))

model = LinearRegression()
model.fit(accel_data[['x', 'y']], noisy_signal_x)
filtered_signal_x = model.predict(accel_data[['x', 'y']])

plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], signal_x, color='blue', linewidth=2, label='Signal X Original')
plt.plot(accel_data['Time'], noisy_signal_x, color='green', linewidth=2, label='Signal X bruité')
plt.plot(accel_data['Time'], filtered_signal_x, color='red', linewidth=2, label='Signal X filtré')
plt.xlabel('Time')
plt.ylabel('Signal Value')
plt.title('Signal X bruité et filtré')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()