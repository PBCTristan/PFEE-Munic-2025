import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# filter using the fourrier method
def filter(input_data, cutoff):
    accel_data = pd.read_csv(input_data)
    accel_data['Time'] = range(1, len(accel_data) + 1)

    signal_x = accel_data['x']
    signal_y = accel_data['y']
    signal_z = accel_data['z']

    signal_fft = np.fft.fft(signal_x)
    freq = np.fft.fftfreq(len(signal_x))
    signal_fft[np.abs(freq) > cutoff] = 0
    signal_fft[np.abs(freq) > (1 - cutoff)] = 0
    signal_filtered_x = np.fft.ifft(signal_fft)

    signal_fft = np.fft.fft(signal_y)
    freq = np.fft.fftfreq(len(signal_y))
    signal_fft[np.abs(freq) > cutoff] = 0
    signal_fft[np.abs(freq) > (1 - cutoff)] = 0
    signal_filtered_y = np.fft.ifft(signal_fft)

    signal_fft = np.fft.fft(signal_z)
    freq = np.fft.fftfreq(len(signal_z))
    signal_fft[np.abs(freq) > cutoff] = 0
    signal_fft[np.abs(freq) > (1 - cutoff)] = 0
    signal_filtered_z = np.fft.ifft(signal_fft)


    return signal_filtered_x, signal_filtered_y, signal_filtered_z


def fourrier_denoising(input_csv_path, cutoff):
    x_result, y_result, z_result = filter(input_csv_path, cutoff)
    print(f'Processed {input_csv_path} filter signal with fourrier')
    return x_result, y_result, z_result