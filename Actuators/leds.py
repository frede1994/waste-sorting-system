import RPi.GPIO as GPIO
import time

def lightSetup(pin_number):
    GPIO.setup(pin_number, GPIO.OUT)

def lightOn(pin_number):
    GPIO.setup(pin_number, GPIO.OUT)
    print("LED on")
    GPIO.output(pin_number, GPIO.HIGH)

def lightOff(pin_number):
    print("LED off")
    GPIO.output(pin_number, GPIO.LOW)

