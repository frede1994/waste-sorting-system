#!/usr/bin/python

from Sensors import camera, ldr, initModel, predicter
from Firebase import firebaseUtil
from Actuators import leds, servoMotors
from PIL import Image
import RPi.GPIO as GPIO
import time

light_pin = 27
servo_pin1 = 17
servo_pin2 = 18
start_angle = 5
ldr_pin = 4
ldr_default_value = 0

# INITIALIZATION
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
print("Initializing light! \n")
leds.lightSetup(light_pin)
print("Done! \n")
print("Calibrating LDR-sensor! \n")
ldr_default_value = ldr.init_ldr(ldr_pin)
print("Done! Value: " + str(ldr_default_value) + "\n")
print("Initializing servos! \n")
gpio1 = servoMotors.initialize(servo_pin1, start_angle)
gpio2 = servoMotors.initialize(servo_pin2, start_angle)
print("Done! \n")
print("Initializing model! \n")
model = initModel.init_model()
print("Done! \n")


def trashDetected():
    # STEP 1: TAKE A PICTURE
    millis = int(round(time.time() * 1000))
    # sleep(0.5)
    filename = camera.takePicture("photo.jpg")
    millisEnd = int(round(time.time() * 1000))
    print("Done picture! \n")
    print(millisEnd-millis)

    # STEP 2: CLASSIFY ???
    millis = int(round(time.time() * 1000))
    imageToPredict = Image.open(filename)
    predictions, probability = predicter.predict(model, imageToPredict)
    typeOfTrash = predictions[5][0]
    millisEnd = int(round(time.time() * 1000))
    print("Done classifying! \n")
    print(millisEnd - millis)

    # STEP 4: UPLOAD TO DATABASE
    millis = int(round(time.time() * 1000))
    firebaseUtil.uploadToFirebase(filename, typeOfTrash, predictions)
    millisEnd = int(round(time.time() * 1000))
    print("Done uploading! \n")
    print(millisEnd - millis)

    # STEP 3: SORT USING MOTORS
    millis = int(round(time.time() * 1000))
    servoMotors.sort(typeOfTrash, gpio1, gpio2)
    millisEnd = int(round(time.time() * 1000))
    print("Done sorting! \n")
    print(millisEnd - millis)


tries = 0
try:
    # Main loop
    while True:
        ldrValue = ldr.measureLight(ldr_pin)
        tries += 1
        if tries > 10 and ldrValue > ldr_default_value+8000:
            tries = 0
            trashDetected()

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
