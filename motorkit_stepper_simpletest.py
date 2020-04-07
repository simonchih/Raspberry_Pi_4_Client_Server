"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

for i in range(1):
    kit.stepper2.onestep()
    time.sleep(0.01)
