import cv2
import time 
# open camera
cap =cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
# take frame
ret, frame =cap.read()
# write frame to file
timer = 0
while( timer < 30):
    time.sleep(0.25)
    cap =cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    cv2.imwrite('images/image' + timer + '.jpg', frame)
    timer = timer+1
# release camera
cap.release()
