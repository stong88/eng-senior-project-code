'''
Features:
- Move forward, move backward
- Set speed
    - MS3 is always set to low (GND)
    - 1, 2, 3, 4 (4 is highest)
- Limit switch
'''

import RPi.GPIO as GPIO
import threading
import time

DELAY = 0.001

class joint:
    def __init__(self, step_pin, dir_pin, lim1_pin, lim2_pin, ms1_pin, ms2_pin):
        # Create state.moving (boolean) and state.thread
        self._moving = False
        self._move_thread = None

        self._STEP_PIN = step_pin
        self._DIR_PIN = dir_pin
        self._LIM1_PIN = lim1_pin
        self._LIM2_PIN = lim2_pin
        self._MS1_PIN = ms1_pin
        self._MS2_PIN = ms2_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(lim1_pin, GPIO.IN)
        GPIO.setup(lim2_pin, GPIO.IN)
        GPIO.setup(ms1_pin, GPIO.OUT)
        GPIO.setup(ms2_pin, GPIO.OUT)

    def _move(self):
        self._moving = True
        while self._moving:
            print("Moving forward")
            GPIO.output(self._STEP_PIN, GPIO.HIGH)
            time.sleep(DELAY)
            GPIO.output(self._STEP_PIN, GPIO.LOW)
            time.sleep(DELAY)
            
            if GPIO.input(self._LIM1_PIN) or GPIO.input(self._LIM2_PIN):
                self._moving = False

    
    def _stop(self):
        self._moving = False
        self._move_thread.join()
        GPIO.output(self._STEP_PIN, GPIO.LOW)
    
    
    def set_direction(self, clockwise):
        if clockwise: # TODO - need to check if this is correct
            GPIO.output(self._DIR_PIN, GPIO.HIGH)
        else:
            GPIO.output(self._DIR_PIN, GPIO.LOW)

    def toggle_move(self):
        if not self._moving:
            self._move_thread = threading.Thread(target=self._move, args=())
            self._move_thread.start()
        else:
            self._stop()
    

    def set_speed(self, speed):
        if speed == 1:
            GPIO.output(self._MS1_PIN, GPIO.HIGH)
            GPIO.output(self._MS2_PIN, GPIO.HIGH)
        elif speed == 2:
            GPIO.output(self._MS1_PIN, GPIO.LOW)
            GPIO.output(self._MS2_PIN, GPIO.HIGH)
        elif speed == 3:
            GPIO.output(self._MS1_PIN, GPIO.HIGH)
            GPIO.output(self._MS2_PIN, GPIO.LOW)
        elif speed == 4:
            GPIO.output(self._MS1_PIN, GPIO.LOW)
            GPIO.output(self._MS2_PIN, GPIO.LOW)
        else:
            print("Invalid speed")
            return