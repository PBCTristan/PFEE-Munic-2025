import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# filter using the square method
def filtered(dataframe, x_degree, y_degree, z_degree, fuse_method) -> pd.DataFrame:
    
    dataframe['Time'] = range(1, len(dataframe) + 1)

    signal_x = dataframe['accel_x']
    signal_y = dataframe['accel_y']
    signal_z = dataframe['accel_z']

    coefficients = np.polyfit(dataframe['Time'], signal_x, x_degree)
    poly_model = np.poly1d(coefficients)
    signal_filtered_x = poly_model(dataframe['Time'])


    coefficients = np.polyfit(dataframe['Time'], signal_y, y_degree)
    poly_model = np.poly1d(coefficients)
    signal_filtered_y = poly_model(dataframe['Time'])

    coefficients = np.polyfit(dataframe['Time'], signal_z, z_degree)
    poly_model = np.poly1d(coefficients)
    signal_filtered_z = poly_model(dataframe['Time'])

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

def square_denoising(dataframe, x_degree, y_degree, z_degree, fuse_method):
    copy = filtered(dataframe, x_degree, y_degree, z_degree, fuse_method)
    print(f'Processed {dataframe} filter signal with square')
    return copy
