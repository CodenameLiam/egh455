from ImageProcessing import ImageProcessing
from airQuality import airQuality

WEB_ON = False    #try to communicate with webserver
LCD_ON = False    #try to write to lcd screen
USE_LIVE_IMAGE = False  #draw detections over a live capture instead of the image they were inferenced on.
CV2_IMSHOW = True   #draw the image on the screen of the pi (if connected to hdmi)
PRINT_FPS_TO_CONSOLE = True

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
    
    aQ = airQuality(conn, lcd.WIDTH, lcd.HEIGHT)
    aQ.start()
    
    switch_counter = 0
    if(LCD_ON or WEB_ON):
        while True:
            
            #sleep(1/(TARGET_FPS*10))
            if(USE_LIVE_IMAGE):
                image = IP.getCurImg() 
				
                if(WEB_ON):
                    markers = IP.getDetections()
                    conn.image_message(image, markers)
                if(LCD_ON):
                    if(counter < LCD_SWITCH_THRESH):
                        sensor_img = aQ.getImage()
                        lcd.display(sensor_img)
                    else:
                        im_pil = IP.convert2LCD(image)
                        lcd.display(im_pil)
                        if(switch_counter >= LCD_SWITCH_THRESH):
                            switch_counter = 0;
                switch_counter = switch_counter +1

            else:
				
                if(LCD_ON):
					
                    sensor_img = aQ.getImage()
                    lcd.display(sensor_img)

    

if __name__ == '__main__':
    main()
