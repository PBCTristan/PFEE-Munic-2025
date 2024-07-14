import numpy as np
import matplotlib.pyplot as plt

accel_data = np.genfromtxt(r"C:\Users\tanth\pfee-munic\signal\output.csv", delimiter=',', skip_header=1)
time = np.arange(1, len(accel_data) + 1)


signal_x = accel_data[:, 2]

noise_level = 0.1
np.random.seed(123)
noisy_signal_x = signal_x + np.random.normal(0, noise_level, len(signal_x))

signal_fft = np.fft.fft(noisy_signal_x)
n = len(noisy_signal_x)
freq = np.fft.fftfreq(n)

cutoff = 0.5
signal_fft[np.abs(freq) > cutoff] = 0
signal_fft[np.abs(freq) > (1 - cutoff)] = 0


signal_filtered = np.fft.ifft(signal_fft)


plt.figure(figsize=(10, 6))
plt.plot(time, signal_x, color='blue', label='Original Signal')
plt.plot(time, noisy_signal_x, color='green', label='Noisy Signal')
plt.plot(time, signal_filtered.real, color='red', label='Filtered Signal')
plt.xlabel('Time')
plt.ylabel('Signal Value')
plt.title('Comparison of Signals')
plt.legend()
plt.grid(True)
plt.show()
