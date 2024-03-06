import RPi.GPIO as GPIO
import numpy as np
import asyncio
import time

# Define GPIO pins
PULSE_PIN = 17
DIR_PIN = 27
ENABLE_PIN = 22

class Motor:
    # Constructor
    def __init__(self, direction_pin, pulse_pin, enable_pin):
        self.DIRECTION_PIN = direction_pin
        self.PULSE_PIN = pulse_pin
        self.ENABLE_PIN = enable_pin
        self.MIN_SPEED = 0.0008
        self.MAX_SPEED = 0.00008

        self.setup_pins()


    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)  # Use BCM numbering, or change to board
        GPIO.setup(self.DIRECTION_PIN, GPIO.OUT)
        GPIO.setup(self.PULSE_PIN, GPIO.OUT)
        GPIO.setup(self.ENABLE_PIN, GPIO.OUT)

    async def step(self, steps, direction=True):
        self.set_direction(direction)
        self.enable()

        starting_percent = int(steps * 0.025)  # Calculate the beginning of the cycle
        ending_percent = steps - int(steps * 0.015)  # Calculate end of the cycle

        for current_step in range(steps):
            # If the current step is in the first 15% of the total steps ease in
            if current_step < starting_percent:
                delay = np.interp(current_step, [0, starting_percent], [self.MIN_SPEED, self.MAX_SPEED])
                pass

            # If the current step is in the last 10% of the total steps ease out
            elif current_step >= ending_percent:
                delay = np.interp(current_step, [ending_percent, steps], [self.MAX_SPEED, self.MIN_SPEED])
                pass
            
            # Else normal top speed
            else:
                delay = self.MAX_SPEED

            GPIO.output(self.PULSE_PIN, GPIO.HIGH)
            await asyncio.sleep(delay)
            GPIO.output(self.PULSE_PIN, GPIO.LOW)
            await asyncio.sleep(delay)

        self.disable()

    def enable(self):
        # Counterintuitively, the motor is enabled when the pin is low
        GPIO.output(self.ENABLE_PIN, GPIO.LOW)

    def disable(self):
        # Counterintuitively, the motor is disabled when the pin is high
        GPIO.output(self.ENABLE_PIN, GPIO.HIGH)

    def set_direction(self, direction=True): 
        # True -> Counterclockwise; False -> Clockwise
        GPIO.output(self.DIRECTION_PIN, GPIO.HIGH if direction else GPIO.LOW)

def cleanup():
    print("Cleaning up GPIO..")
    GPIO.cleanup()
    
# Usage example
if __name__ == "__main__":
    motor = Motor(direction_pin=27, pulse_pin=17, enable_pin=22)
    motor.enable()
    
    while True:
        try:
            steps_to_take = int(input(("Enter steps to take: ")))
            break
        except ValueError:
            print("Invalid input! Please enter just a whole number.")
    asyncio.run(motor.step(steps_to_take))
    motor.disable()
      
    cleanup()
