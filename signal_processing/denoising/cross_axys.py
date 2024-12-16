import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# filter using the cross_axys method
def filter(dataframe) -> pd.DataFrame:

    dataframe['Time'] = range(1, len(dataframe) + 1)

    signal_x = dataframe['accel_x']
    signal_y = dataframe['accel_y']
    signal_z = dataframe['accel_z']

    model = LinearRegression()
    model.fit(dataframe[['x', 'y']], signal_z)
    signal_filtered_z = model.predict(dataframe[['x', 'y']])

    model = LinearRegression()
    model.fit(dataframe[['z', 'y']], signal_x)
    signal_filtered_x = model.predict(dataframe[['z', 'y']])

    model = LinearRegression()
    model.fit(dataframe[['x', 'z']], signal_y)
    signal_filtered_y = model.predict(dataframe[['x', 'z']])

    copy = dataframe.copy()
    copy['accel_x'] = signal_filtered_x
    copy['accel_y'] = signal_filtered_y
    copy['accel_z'] = signal_filtered_z
    return copy


def cross_axys_denoising(dataframe):
    copy = filter(dataframe)
    print(f'Processed {dataframe} filter signal with cross-axys')
    return copy