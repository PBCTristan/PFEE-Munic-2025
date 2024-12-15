rm(list = ls())


accel_data <- read.csv("C:/Users/tanth/Downloads/accelerometer/accelerometer.csv")
accel_data$Time <- seq(from = 1, to = nrow(accel_data))


signal_x <- accel_data$x


set.seed(123) 
noise_level <- 0.1 
noisy_signal_x <- signal_x + rnorm(length(signal_x), mean = 0, sd = noise_level)

plot(noisy_signal_x, type = 'l', col = 'green', xlab = 'Temps', ylab = 'Valeur du signal', main = 'Signal bruité du capteur x')

cor_matrix <- cor(accel_data[, c("x", "y", "z")])
print(cor_matrix)

model <- lm(noisy_signal_x ~ accel_data$y + accel_data$z)

filtered_signal_x <- fitted(model)

accel_data$filtered_x <- filtered_signal_x


plot(accel_data$Time, noisy_signal_x, type = "l", col = "green", lwd = 2, ylim = range(c(noisy_signal_x, filtered_signal_x), na.rm = TRUE), main = "Signal X bruité et filtré")
lines(accel_data$Time, filtered_signal_x, col = "red", lwd = 2)
legend("topright", legend = c("Signal X bruité", "Signal X filtré"), col = c("green", "red"), lwd = 2)

head(accel_data)