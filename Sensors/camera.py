from time import sleep
from picamera import PiCamera
from PIL import Image

def takePicture(filename):
    camera = PiCamera()
    camera.resolution = (448, 448)
    # camera.start_preview()
    # camera.image_effect = 'watercolor'
    sleep(1)
    camera.capture(filename)
    camera.close()
    # preProcess(filename)
    return filename


def preProcess(filename):
    im = Image.open(filename)
    width = 440
    height = 270
    left = 50
    top = 65
    right = left + width
    bottom = top + height
    imCropped = im.crop((left, top, right, bottom))
    newsize = (224, 224)
    imResized = imCropped.resize(newsize)
    imResized.save(filename)
