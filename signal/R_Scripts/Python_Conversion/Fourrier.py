import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
accel_data = pd.read_csv(r"C:\Users\Gérard Grokoum\pfee-munic\signal\output.csv")
accel_data['Time'] = range(1, len(accel_data) + 1)

signal_x = accel_data['z']

noise_level = 0.5
np.random.seed(123)
noisy_signal_x = signal_x + np.random.normal(0, noise_level, len(signal_x))

signal_fft = np.fft.fft(noisy_signal_x)
n = len(noisy_signal_x)
freq = np.fft.fftfreq(n)

cutoff = 0.1
signal_fft[np.abs(freq) > cutoff] = 0
signal_fft[np.abs(freq) > (1 - cutoff)] = 0


signal_filtered = np.fft.ifft(signal_fft)


plt.figure(figsize=(10, 6))
plt.plot(accel_data['Time'], signal_x, color='blue', label='Signal X Original')
plt.plot(accel_data['Time'], signal_filtered.real, color='red', label='Signal X filtré')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Fourrier')
plt.legend()
plt.grid(True)
plt.show()
