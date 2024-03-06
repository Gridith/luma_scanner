from os.path import abspath, dirname
from datetime import datetime
import motor_controls as mc
import RPi.GPIO as GPIO
import file_handler
import subprocess
import asyncio
import buzzer
import re

# Setup Motor
motor = mc.Motor(direction_pin=27, pulse_pin=17, enable_pin=22) # These are BCM pins
STEP_SIZE = 3200

START_SIGNAL_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(START_SIGNAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

async def capture():
    global STEP_SIZE
    
    current_time = datetime.now().strftime("%m-%d-%y_%H-%M-%S")
    process = subprocess.Popen(f"gopro-video 33 --wired --output TEST_%s.mp4" % (current_time), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        while True:
            line = process.stdout.readline()
            line = line.decode().strip()
            if line.startswith("ERROR"):
                print(line)
                return
            
            if "Capturing a video..." in line:
                print(line)
                await motor.step(STEP_SIZE*4, True) # Step multiplied by the gear ratio
                print("Motor finished, ready for rewind")
                buzzer.one_beep()
                print("Rewinding motor")
                await motor.step(STEP_SIZE*4, False)
                return
    except:
        return


async def main():
    global START_SIGNAL_PIN
    
    folder_path = dirname(abspath(__file__))
    file_handler.start_monitoring_in_background(folder_path, file_handler.on_new_file_detected)
    
    while True:
        if GPIO.input(START_SIGNAL_PIN):
            capture_task = asyncio.create_task(capture())
            print("Post start of capture")
            await capture_task

if __name__ == "__main__":
    asyncio.run(main())
    mc.cleanup()