rm(list = ls())

accel_data <- read.csv("C:/Users/tanth/Downloads/accelerometer/accelerometer.csv")
accel_data$Time <- seq(from = 1, to = nrow(accel_data))

signal_x <- accel_data$x

set.seed(123)
noise_level <- 0.1
noisy_signal_x <- signal_x + rnorm(length(signal_x), mean = 0, sd = noise_level)

plot(noisy_signal_x, type = 'l', col = 'green', xlab = 'Temps', ylab = 'Valeur du signal', main = 'Signal bruité du capteur x')

signal_fft <- fft(noisy_signal_x)

n <- length(noisy_signal_x)
freq <- seq(0, n - 1) * (1 / n)

plot(noisy_signal_x, type = 'l', col = 'green', xlab = 'Temps', ylab = 'Valeur du signal', main = 'Signal bruité du capteur x')

plot(freq, Mod(signal_fft), type = "h", main = "Spectre de fréquence", xlab = "Fréquence (Hz)", ylab = "Amplitude")

cutoff <- 0.5
signal_fft[freq > cutoff] <- 0
signal_fft[freq > (1 - cutoff)] <- 0

signal_filtered <- Re(fft(signal_fft, inverse = TRUE) / n)

par(mfrow = c(1, 1))
plot(noisy_signal_x, type = 'l', col = 'blue', xlab = 'Temps', ylab = 'Valeur du signal', main = 'Comparaison des Signaux')
lines(signal_filtered, col = 'red')
legend("topright", legend = c("Signal Propre", "Signal Filtré"), col = c("blue", "red"), lty = 1)
