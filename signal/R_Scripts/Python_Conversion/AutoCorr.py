import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

accel_data = pd.read_csv(r"C:\Users\Gérard Grokoum\pfee-munic\signal\output.csv")

signal_z = accel_data['z']

accel_data['Time'] = np.arange(0, len(accel_data))

arima_model = ARIMA(signal_z, order=(2, 0, 1))

arima_result = arima_model.fit()

filtered_signal_z = arima_result.fittedvalues


signal_x = accel_data['x']

accel_data['Time'] = np.arange(0, len(accel_data))

arima_model = ARIMA(signal_x, order=(2, 0, 1))

arima_result = arima_model.fit()

filtered_signal_x = arima_result.fittedvalues



signal_y = accel_data['y']

accel_data['Time'] = np.arange(0, len(accel_data))

arima_model = ARIMA(signal_y, order=(2, 0, 1))

arima_result = arima_model.fit()

filtered_signal_y = arima_result.fittedvalues



plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')

plt.plot(accel_data['Time'], signal_y, color='red', label='Signal Y Original')

plt.plot(accel_data['Time'], signal_z, color='green', label='Signal Z Original')

plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('AutoCorr')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))

plt.plot(accel_data['Time'], filtered_signal_x, color='blue', label='Signal X filtré')

plt.plot(accel_data['Time'], filtered_signal_y, color='red', label='Signal Y filtré')

plt.plot(accel_data['Time'], filtered_signal_z, color='green', label='Signal Z filtré')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('AutoCorr')
plt.legend()
plt.grid(True)
plt.show()