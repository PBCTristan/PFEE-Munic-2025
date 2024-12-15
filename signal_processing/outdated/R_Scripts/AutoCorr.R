rm(list = ls())

accel_data <- read.csv("C:/Users/tanth/Downloads/accelerometer/accelerometer.csv")

signal_z <- accel_data$z

noise_level <- 0.1
noisy_signal_z <- signal_z + rnorm(length(signal_z), mean = 0, sd = noise_level)

accel_data$Time <- seq(from = 1, to = nrow(accel_data))

library(forecast)

arima_model <- auto.arima(noisy_signal_z)

filtered_signal_z <- fitted(arima_model)

accel_data$filtered_z <- filtered_signal_z

plot(accel_data$Time, noisy_signal_z, type = "l", col = "green", lwd = 2, ylim = range(noisy_signal_z, na.rm = TRUE), main = "Signal Z bruité et filtré")
lines(accel_data$Time, filtered_signal_z, col = "red", lwd = 2)
legend("topright", legend = c("Signal Z bruité", "Signal Z filtré"), col = c("green", "red"), lwd = 2)