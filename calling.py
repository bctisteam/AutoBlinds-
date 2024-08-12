import RPi.GPIO as GPIO
import time
from time import sleep
from subprocess import call
import main

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

LDR = 3
MotA = 16
MotB = 18
MotE = 22
Hall = 5
T = 2

GPIO.setup(MotA,GPIO.OUT)
GPIO.setup(MotB,GPIO.OUT)
GPIO.setup(MotE,GPIO.OUT)
GPIO.setup(LDR,GPIO.IN)
GPIO.setup(Hall,GPIO.IN)

def open_main_file():
    call(["python", "main.py"])

while True:
    try:
        open_main_file()
    
    except KeyboardInterrupt:
        print("PROGRAM HAS SHUT OFF")
        GPIO.output(MotA,GPIO.LOW)
        GPIO.output(MotB,GPIO.LOW)
        GPIO.output(MotE,GPIO.LOW)
        GPIO.cleanup()
        break
