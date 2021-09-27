from picamera import PiCamera
import time

camera = PiCamera()

for i in range(1):
    camera.capture('image{0:04d}.jpg'.format(i))
    time.sleep(0.05)
    
