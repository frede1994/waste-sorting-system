import RPi.GPIO as GPIO
import time
time_between_chutes = 0.5
delay = 1


def initialize(servo_pin, start_angle):
    GPIO.setup(servo_pin, GPIO.OUT)
    gpio = GPIO.PWM(servo_pin, 50)  # GPIO 17 for PWM with 50Hz
    gpio.start(start_angle)  # Initialization
    gpio.ChangeDutyCycle(0)
    return gpio


def sort(trash, gpio1, gpio2):
    if trash == "trash":
        print("Trash")
        toTrash(gpio1)
        time.sleep(time_between_chutes)
    else:
        print(trash)
        notTrash(gpio1)
        time.sleep(time_between_chutes)
        if trash == "glass" or trash == "metal" or trash == "plastic":
            toGlassMetalPlastic(gpio2)
        if trash == "paper" or trash == "cardboard":            toPaper(gpio2)

def toGlassMetalPlastic(gpio):
    print("GPM")
    gpio.ChangeDutyCycle(11)
    time.sleep(delay)
    gpio.ChangeDutyCycle(6.45)
    time.sleep(0.2)
    gpio.ChangeDutyCycle(0)

def toPaper(gpio):
    print("paper")
    gpio.ChangeDutyCycle(3)
    time.sleep(delay)
    gpio.ChangeDutyCycle(6.4)
    time.sleep(0.2)
    gpio.ChangeDutyCycle(0)

def notTrash(gpio):
    gpio.ChangeDutyCycle(3)
    time.sleep(delay)
    gpio.ChangeDutyCycle(4)
    time.sleep(0.2)
    gpio.ChangeDutyCycle(0)

def toTrash(gpio):
    gpio.ChangeDutyCycle(8)
    time.sleep(delay)
    gpio.ChangeDutyCycle(6.45)
    time.sleep(0.2)
    gpio.ChangeDutyCycle(0)