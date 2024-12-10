import numpy as np
def remove_noise_fft(x, dt, freq_threshhold=50):
    l = len(x)
    f_hat = np.fft.fft(x, l)
    psd = f_hat * np.conj(f_hat) / l
    freq = (1 / dt) * np.arange(l)
    L = np.arange(1, np.floor(l / 2), dtype='int')

    indices = psd > 100
    return np.real(np.fft.ifft(indices * f_hat))
