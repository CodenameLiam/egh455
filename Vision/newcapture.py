from picamera import PiCamera
import time

camera = PiCamera()

for i in range(10000):
    camera.capture('images2/image{0:04d}.jpg'.format(i))
    time.sleep(0.05)
    
