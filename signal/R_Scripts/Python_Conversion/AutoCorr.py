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

accel_data['filtered_z'] = filtered_signal_z

plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], signal_z, color='blue', linewidth=2, label='Signal Z Original')
plt.plot(accel_data['Time'], filtered_signal_z, color='red', linewidth=2, label='Signal Z filtré')
plt.title('Autocorrelation')
plt.legend(loc='upper right')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.grid(True)
plt.show()