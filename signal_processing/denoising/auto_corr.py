import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# filter using the fourrier method
def filter(input_data):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)

    signal_x = accel_data['x']
    signal_y = accel_data['y']
    signal_z = accel_data['z']

    arima_model = ARIMA(signal_x, order=(2, 0, 1))
    arima_result = arima_model.fit()
    signal_filtered_x = arima_result.fittedvalues

    arima_model = ARIMA(signal_y, order=(2, 0, 1))
    arima_result = arima_model.fit()
    signal_filtered_y = arima_result.fittedvalues

    arima_model = ARIMA(signal_z, order=(2, 0, 1))
    arima_result = arima_model.fit()
    signal_filtered_z = arima_result.fittedvalues

    return signal_filtered_x, signal_filtered_y, signal_filtered_z

def auto_corr_denoising(input_csv_path):
    x_filtered, y_filtered, z_filtered = filter(input_csv_path)
    print(f'Processed {input_csv_path} filter signal with auto correlation')
    return x_filtered, y_filtered, z_filtered