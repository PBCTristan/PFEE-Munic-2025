import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# filter using the fourrier method
def filter(dataframe, cutoff) -> pd.DataFrame:
    dataframe['Time'] = range(1, len(dataframe) + 1)

    signal_x = dataframe['accel_x']
    signal_y = dataframe['accel_y']
    signal_z = dataframe['accel_z']

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

    copy = dataframe.copy()
    copy['accel_x'] = signal_filtered_x
    copy['accel_y'] = signal_filtered_y
    copy['accel_z'] = signal_filtered_z
    return copy


def fourrier_denoising(dataframe, cutoff):
    copy = filter(dataframe, cutoff)
    print(f'Processed {dataframe} filter signal with fourrier')
    return copy