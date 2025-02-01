import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# filter using the autocorr method
def filtered(dataframe, fuse_method) -> pd.DataFrame:

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
    if (fuse_method == "mean"):
        fused_signal = (signal_filtered_x + signal_filtered_y + signal_filtered_z) / 3 #mean
        copy['filtered_accel'] = fused_signal
    elif (fuse_method == "norm"):
        fused_signal = np.sqrt(signal_filtered_x**2 + signal_filtered_y**2 + signal_filtered_z**2) #euclidian
        copy['filtered_accel'] = fused_signal
    return copy

def auto_corr_denoising(dataframe, fuse_method):
    copy = filtered(dataframe, fuse_method)
    print(f'Processed {dataframe} filter signal with auto correlation')
    return copy
