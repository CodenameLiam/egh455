from ImageProcessing import ImageProcessing
from airQuality import airQuality

from time import sleep

TARGET_FPS = 15
WEB_ON = False    #try to communicate with webserver
LCD_ON = True    #try to write to lcd screen
USE_LIVE_IMAGE = False  #draw detections over a live capture instead of the image they were inferenced on.
CV2_IMSHOW = True   #draw the image on the screen of the pi (if connected to hdmi)
PRINT_FPS_TO_CONSOLE = True
LCD_SWITCH_THRESH = 3

def main():
    from CameraHelper import CameraHelper
    from lcdHelper import lcdHelper

    lcd = lcdHelper()
    from webServerConnection import webServerConnection
    conn = webServerConnection()
    
    cameraHelper = CameraHelper(framerate=TARGET_FPS)
    cameraHelper.start()
    sleep(1)
    
    #if(USE_LIVE_IMAGE):
    #    IP = ImageProcessing(cameraHelper, lcd)
    #else:
    #    
    IP = ImageProcessing(cameraHelper, lcd, conn, mode=0)
    IP.start()
    
    aQ = airQuality(conn, IP, lcd.WIDTH, lcd.HEIGHT)
    aQ.start()
    
    switch_counter = 0
    while True:
         #if(switch_counter < LCD_SWITCH_THRESH):
         
           
         #else:

            sensor_img = aQ.getImage()
            lcd.display(sensor_img)
 
    

if __name__ == '__main__':
    main()
