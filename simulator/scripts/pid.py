class PID:
    def __init__(self, kp, ki, kd, max_value, min_value, t) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.max_value = max_value
        self.min_value = min_value
        self.step = t

        self.last_error = 0
        self.last_deriv = 0
        self.last_command = 0
        self.last_clamped_command = 0
        self.integral = 0
        self.has_reset = False
    

    def update(self, value, setpoint) -> float:
        error = setpoint - value if value >= 0.02 else 0
        if error == 0:
            return 0.0
        p_out = self.kp * error

        self.integral += error * self.step
        
        self.integral = max(-1.0, min(self.integral, 1.0))

        deriv = (error - self.last_error) / self.step
        self.last_error = error
        d_out = self.kd * deriv

        command = p_out + self.integral * self.ki + d_out
        self.last_command = command

        clamped_command = max(self.min_value, min(command, self.max_value))
        self.last_clamped_command = clamped_command

        return clamped_command
    
    def values(self) -> str:
        return f'Last error: {self.last_error}\nLast deriv: {self.last_deriv}\nIntegral: {self.integral}'
    
    def toString(self) -> str:
        return f'PID :\n\tKp: {self.kp}\n\tKi: {self.ki}\n\tKd: {self.kd}\n\tTimestep: {self.step}\n\tValues space: [{self.min_value}, {self.max_value}]'
        
