import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# filter using the autocorr method
def filter(dataframe) -> pd.DataFrame:

    dataframe['Time'] = range(1, len(dataframe) + 1)

    signal_x = dataframe['accel_x']
    signal_y = dataframe['accel_y']
    signal_z = dataframe['accel_z']

    arima_model = ARIMA(signal_x, order=(2, 0, 1))
    arima_result = arima_model.fit()
    signal_filtered_x = arima_result.fittedvalues

    arima_model = ARIMA(signal_y, order=(2, 0, 1))
    arima_result = arima_model.fit()
    signal_filtered_y = arima_result.fittedvalues

    arima_model = ARIMA(signal_z, order=(2, 0, 1))
    arima_result = arima_model.fit()
    signal_filtered_z = arima_result.fittedvalues

    copy = dataframe.copy()
    copy['accel_x'] = signal_filtered_x
    copy['accel_y'] = signal_filtered_y
    copy['accel_z'] = signal_filtered_z
    return copy

def auto_corr_denoising(dataframe):
    copy = filter(dataframe)
    print(f'Processed {dataframe} filter signal with auto correlation')
    return copy