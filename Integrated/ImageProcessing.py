
import cv2
from cv2 import aruco
import numpy as np
from io import BytesIO
import requests

from time import time, sleep
from Yolov4Tiny_uavpayloadtaq import YoloV4_UAVPAYLOADTAQ as search_model
from threading import Thread
import ncnn

from draw_detect import draw_detection_objects

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from fonts.ttf import RobotoMedium as UserFont



TARGET_FPS = 15
WEB_ON = False    #try to communicate with webserver
LCD_ON = True    #try to write to lcd screen
USE_LIVE_IMAGE = False  #draw detections over a live capture instead of the image they were inferenced on.
CV2_IMSHOW = False   #draw the image on the screen of the pi (if connected to hdmi)
PRINT_FPS_TO_CONSOLE = False

# Gets a file buffer from a PIL image
def pil_to_buf(pil_image):
    # Setup a buffer for the image
    buf = BytesIO()
    # Save the image to the buffer
    pil_image.save(buf, 'jpeg')
    # Return the buffer value
    return buf.getvalue()


class ImageProcessing:
    lcd = None
    wed = None
    objects = []
    img = []
    aruco_zip = []
    img_avail = False
    detect_labels = []
    FPS_message= ""

    def __init__(self, cameraHelper, lcdHelper=None, web=None, mode = 0):
        self.cameraH = cameraHelper
        self.lcd = lcdHelper
        self.detections = None
        self.net = search_model()
        self.web = web
        self.mode = mode
        if(lcdHelper is not None):
            # Set up canvas and font
            #img_data = Image.new('RGB', (self.lcd.WIDTH, self.lcd.HEIGHT), color=(0, 0, 0))

            self.font_size_small = 10
            self.font_size_large = 20
            self.font = ImageFont.truetype(UserFont, self.font_size_large)
            self.smallfont = ImageFont.truetype(UserFont, self.font_size_small)
            self.x_offset = 2
            self.y_offset = 2
        
            
    def start(self):
        
        # start the thread to read frames from the video stream
        Thread(target=self.run, args=()).start()
        return self
        
        
    def run(self):
        

        arucoDict = aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)
        arucoParams = aruco.DetectorParameters_create()
        
        while True:

            start_cycle = time()
                  
            image_data = self.cameraH.getImage()

            self.detect_labels = dict( 
                markerDetected=False,
                personDetected=False,
                backpackDetected=False)
            #image_data = cv2.imread("./test.jpg")
            
            (corners, ids, rejected) = aruco.detectMarkers(image_data, arucoDict,
            parameters=arucoParams)
            # verify *at least* one ArUco marker was detected
            if len(corners) > 0:
                self.detect_labels['markerDetected'] = True
            # flatten the ArUco IDs list
                ids = ids.flatten()
                
                print(ids)
                self.aruco_zip = zip(corners, ids)
            
            self.objects = self.net(image_data)
            #print(self.objects)
            #print("Tensor Processing1: " + str(time()-start_cycle))
            
            self.img = image_data
            self.img_avail = True

            # 
            for obj in self.objects:
                if obj.label == 1:
                    self.detect_labels['backpackDetected'] = True
                if obj.label == 2:
                    self.detect_labels['personDetected'] = True

                
            # for (markerCorner, markerID) in self.aruco_zip:
            #     self.detect_labels.append("Aruco ID: " + str(markerID))
            

            if(self.mode==1):
                if(self.web is not None or self.lcd is not None or CV2_IMSHOW):
                    self.img_avail = False
                    self.__drawDetections(self.img)
                    
                if(self.web is not None):
                    self.web.image_message(self.img, self.getDetections())
                    
                if(self.lcd is not None):
                    im_pil = self.convert2LCD(self.img)
                    self.lcd.display(im_pil)
                    
                if(CV2_IMSHOW):
                    #image = cv2.cvtColor(image_data,cv2.COLOR_RGB2BGR)
                    cv2.imshow("image", image_data)
                    
            FPS = 1 / ( time() - start_cycle)
            self.FPS_message = "Detect FPS: " + str(FPS)
            if(PRINT_FPS_TO_CONSOLE):
                print(self.FPS_message)
                
            im_pil = Image.fromarray(np.asarray(image_data))
            im_pil = im_pil.resize((480, 360))
                
            requests.post('http://localhost:5000/image', 
                files=dict(file=pil_to_buf(im_pil)), 
                data=self.detect_labels)

            print("\nIM TRYING TO SEND A PHOTO\n")
            
                
            

            
            
         
            if cv2.waitKey(1)==ord('q'):
                break
    
    def __drawDetections(self, image_data):
        
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
        
        # return the frame most recently captured with previous detections drawn on
        self.__drawDetections(image_data)
        return image_data
        
    def getLatestDetectImg(self):
        if(self.img_avail == True):
            # return the frame most recently inferenced with its detections drawn on
            self.img_avail = False
            self.__drawDetections(self.img)
            return self.img
        else:
            return None
            
    def convert2LCD(self, image_data):
        #convert to PIL
        im_pil = Image.fromarray(np.asarray(image_data))
    
        # Display the resulting frame
        # Resize the image
        im_pil = im_pil.resize((self.lcd.WIDTH, self.lcd.HEIGHT))
    
        draw = ImageDraw.Draw(im_pil)
        x = self.x_offset
        y = self.y_offset
        #draw.text((x, y), self.FPS_message, font=self.smallfont, fill=(0,0,255))
        return im_pil
        
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


def main():
    from CameraHelper import CameraHelper
    conn = None
    lcd = None
    if(LCD_ON):
        from lcdHelper import lcdHelper
        lcd = lcdHelper()
    if(WEB_ON):
        from webServerConnection import webServerConnection
        conn = webServerConnection()
    
    cameraHelper = CameraHelper(framerate=TARGET_FPS)
    cameraHelper.start()
    sleep(1)
    
    if(USE_LIVE_IMAGE):
        IP = ImageProcessing(cameraHelper, lcd)
    else:
        IP = ImageProcessing(cameraHelper, lcd, conn, mode=1)
        
    IP.start()
    
    if((LCD_ON or WEB_ON) and USE_LIVE_IMAGE):
        while True:
            
            #sleep(1/(TARGET_FPS*10))
          
            image = IP.getCurImg()   
               
            if(WEB_ON):
                pass
               
                # Post the image to the server
                #requests.post('http://localhost:5000/image', 
                 #   files=dict(file=pil_to_buf(image)), 
                  #  data=markers)
                # conn.image_message(image, markers)
            if(LCD_ON):
                im_pil = IP.convert2LCD(image)
                lcd.display(im_pil)

    

if __name__ == '__main__':
    main()
    

