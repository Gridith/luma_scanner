import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)

def one_beep():
    GPIO.output(19, GPIO.HIGH)
    sleep(0.4)
    GPIO.output(19, GPIO.LOW)
    

def two_beep():
    GPIO.output(19, GPIO.HIGH)
    sleep(0.25)
    GPIO.output(19, GPIO.LOW)
    sleep(0.1)
    GPIO.output(19, GPIO.HIGH)
    sleep(0.15)
    GPIO.output(19, GPIO.LOW)
    
def long_beep():
    GPIO.output(19, GPIO.HIGH)
    sleep(0.8)
    GPIO.output(19, GPIO.LOW)
    

if __name__ == "__main__":
    one_beep()
    sleep(2)
    two_beep()
    sleep(2)
    long_beep()
    GPIO.cleanup()