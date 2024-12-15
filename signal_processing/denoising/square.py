import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# filter using the square method
def filter(input_data, x_degree, y_degree, z_degree):
    
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)

    signal_x = accel_data['x']
    signal_y = accel_data['y']
    signal_z = accel_data['z']

    coefficients = np.polyfit(accel_data['Time'], signal_x, x_degree)
    poly_model = np.poly1d(coefficients)
    signal_filtered_x = poly_model(accel_data['Time'])


    coefficients = np.polyfit(accel_data['Time'], signal_y, y_degree)
    poly_model = np.poly1d(coefficients)
    signal_filtered_y = poly_model(accel_data['Time'])

    coefficients = np.polyfit(accel_data['Time'], signal_z, z_degree)
    poly_model = np.poly1d(coefficients)
    signal_filtered_z = poly_model(accel_data['Time'])

    return signal_filtered_x, signal_filtered_y, signal_filtered_z

def square_denoising(input_csv_path, x_degree, y_degree, z_degree):
    x_result, y_result, z_result = filter(input_csv_path, x_degree, y_degree, z_degree)
    print(f'Processed {input_csv_path} filter signal with square')
    return x_result, y_result, z_result