from absl import app, flags, logging
import cv2
from cv2 import aruco
import numpy as np


from time import time, sleep
from yolov4_uavpayloadtaq import YoloV4_UAVPAYLOADTAQ as search_model
from threading import Thread
import ncnn

from draw_detect import draw_detection_objects

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from fonts.ttf import RobotoMedium as UserFont

score = 0.3
iou = 0.5
input_size = 192




class ImageProcessing:
    lcd = None
    objects = []
    img = []
    aruco_zip = []
    img_avail = False
    detect_labels = []

    def __init__(self, cameraHelper, lcdHelper=None):
        self.cameraH = cameraHelper
        self.lcd = lcdHelper
        self.detections = None
        self.net = search_model()
            
    def start(self):
        
        # start the thread to read frames from the video stream
        Thread(target=self.run, args=()).start()
        return self
        
        
    def run(self):
        
        if(self.lcd is not None):
            # Set up canvas and font
            img_data = Image.new('RGB', (self.lcd.WIDTH, self.lcd.HEIGHT), color=(0, 0, 0))

            font_size_small = 10
            font_size_large = 20
            font = ImageFont.truetype(UserFont, font_size_large)
            smallfont = ImageFont.truetype(UserFont, font_size_small)
            x_offset = 2
            y_offset = 2

        

        arucoDict = aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
        arucoParams = aruco.DetectorParameters_create()
        
        while True:

            start_cycle = time()
                  
            image_data = self.cameraH.getImage()
            
            (corners, ids, rejected) = aruco.detectMarkers(image_data, arucoDict,
            parameters=arucoParams)
            # verify *at least* one ArUco marker was detected
            if len(corners) > 0:
            # flatten the ArUco IDs list
                ids = ids.flatten()
                
                #print(ids)
                self.aruco_zip = zip(corners, ids)
            
            self.objects = self.net(image_data)
            #print(objects)
            #print("Tensor Processing1: " + str(time()-start_cycle))
            
            self.img = image_data
            self.img_avail = True
            if(len(self.objects)>0):
                self.detect_labels = list(self.net.class_names[int(self.objects[0].label)])
            else:
                self.detect_labels = []
            for (markerCorner, markerID) in self.aruco_zip:
                self.detect_labels.append("Aruco ID: " + str(markerID))
            
            FPS = 1 / ( time() - start_cycle)
            self.FPS_message = "Detect FPS: " + str(FPS)
            #print(self.FPS_message)
            
            if(self.lcd is not None):
                #convert to PIL
                self.im_pil = Image.fromarray(np.asarray(image_data))
            
                # Display the resulting frame
                # Resize the image
                self.im_pil = self.im_pil.resize((self.lcd.WIDTH, self.lcd.HEIGHT))
            
                draw = ImageDraw.Draw(self.im_pil)
                x = x_offset
                y = y_offset
                draw.text((x, y), self.FPS_message, font=smallfont, fill=(0,0,255))
                        
            if cv2.waitKey(1)==ord('q'):
                break
    
    def drawDetections(self, image_data):
        
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in self.aruco_zip:
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            # draw the bounding box of the ArUCo detection
            cv2.line(image_data, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image_data, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image_data, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image_data, bottomLeft, topLeft, (0, 255, 0), 2)
            
        draw_detection_objects(image_data, self.net.class_names, self.objects)
        
        return image_data
            
    def getDetections(self):
        
            
        return self.detect_labels
    
    def getCurImg(self):
        image_data = self.cameraH.getImage()
        
        # return the frame most recently read
        self.drawDetections(image_data)
        return image_data
        
    def getLatestDetectImg(self):
        if(self.img_avail == True):
            # return the frame most recently read
            self.img_avail = False
            self.drawDetections(self.img)
            return image_data
        else:
            return None
            
        
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


def main():
    from CameraHelper import CameraHelper
    from lcdHelper import lcdHelper
    
    
    cameraHelper = CameraHelper()
    cameraHelper.start()
    sleep(1)
    lcd = lcdHelper()
    
    IP = ImageProcessing(cameraHelper, lcd)
    IP.start()
    
    image = IP.getLatestDetectImg()
    markers = IP.getDetections()

    

if __name__ == '__main__':
    main()
    

