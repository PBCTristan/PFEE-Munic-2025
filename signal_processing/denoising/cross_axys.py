import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# filter using the cross_axys method
def filter(input_data):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)

    signal_x = accel_data['x']
    signal_y = accel_data['y']
    signal_z = accel_data['z']

    model = LinearRegression()
    model.fit(accel_data[['x', 'y']], signal_z)
    signal_filtered_z = model.predict(accel_data[['x', 'y']])

    model = LinearRegression()
    model.fit(accel_data[['z', 'y']], signal_x)
    signal_filtered_x = model.predict(accel_data[['z', 'y']])

    model = LinearRegression()
    model.fit(accel_data[['x', 'z']], signal_y)
    signal_filtered_y = model.predict(accel_data[['x', 'z']])

    return signal_filtered_x, signal_filtered_y, signal_filtered_z


def cross_axys_denoising(input_csv_path):
    x_filtered, y_filtered, z_filtered = filter(input_csv_path)
    print(f'Processed {input_csv_path} filter signal with cross-axys')
    return x_filtered, y_filtered, z_filtered