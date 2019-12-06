import RPi.GPIO as GPIO
from time import sleep
import statistics


def measureLight(ldr_pin):
    count = 0
    counts = []

    # Output on the pin for
    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    sleep(0.1)
    # Change the pin back to input
    GPIO.setup(ldr_pin, GPIO.IN)
    # Count until the pin goes high
    while GPIO.input(ldr_pin) == GPIO.LOW:
        count += 1
    return count


def init_ldr(ldr_pin):
    counts = []
    for x in range(0, 30):
        ldrValue = measureLight(ldr_pin)
        print(ldrValue)
        counts.append(ldrValue)
    return statistics.median(counts)
