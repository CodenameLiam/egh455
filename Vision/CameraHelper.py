from picamera import PiCamera
from io import BytesIO
from picamera.array import 
import time

class CameraHelper()
    camera = None
    #my_stream = BytesIO()
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)  #yolov4 is 416x416, no point in higher res.
        self.camera.framerate = 30  #not sure if needed...

    def getFrame():
        #camera.capture(self.my_stream, 'jpeg')
        rawCapture = PiRGBArray(camera, size=(640, 480))
        self.camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        #plotting the image
        plt.imshow(image)
        return image
    
    def end():
        self.camera = None
    



    
