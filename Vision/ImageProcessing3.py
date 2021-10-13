
from absl import app, flags, logging
#import core.utils as utils
#from core.yolov4 import filter_boxes
import cv2
from cv2 import aruco
#from PIL import Image
import numpy as np

from CameraHelper import CameraHelper
from time import time, sleep
#import imutils
#from imutils.video import FPS
from yolov4_uavpayloadtaq import YoloV4_UAVPAYLOADTAQ as search_model

import ncnn
#from ncnn.model_zoo import get_model
from draw_detect import draw_detection_objects

score = 0.3
iou = 0.5
input_size = 416
def main(_argv):
    #STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config()
    
    

    cameraHelper = CameraHelper().start()
    #fps = FPS().start()
    sleep(1)
    #net = get_model("yolov4_tiny", num_threads=4, use_gpu=True)
    net = search_model()
    #net = ncnn.ncnn.Net()
    #net.load_param("uavpayloadtaq_yolov4-tiny-320-merge-opt-fp16.param")
    #net.load_model("uavpayloadtaq_yolov4-tiny-320-merge-opt-fp16.bin")
     

    arucoDict = aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
    arucoParams = aruco.DetectorParameters_create()
    
    while True:

        start_cycle = time()
        #original_image = cameraHelper.getImage()
        
        #print("Image Collection: " + str(time()-start_cycle))
        
        #image_data = cv2.resize(original_image, (input_size, input_size))
        #image_data = image_data / 255.        
        image_data = cameraHelper.getImage()
        #images_data = []
        
        
        (corners, ids, rejected) = aruco.detectMarkers(image_data, arucoDict,
	parameters=arucoParams)

        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
        # flatten the ArUco IDs list
            ids = ids.flatten()
            # loop over the detected ArUCo corners
            print(ids)
            for (markerCorner, markerID) in zip(corners, ids):
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
        #for i in range(1):
        #    images_data.append(image_data)
        #images_data = np.asarray(images_data).astype(np.float32)

        #print("Image Preprocessing: " + str(time()-start_cycle))
        
        objects = net(image_data)
        for obj in objects:
            print(net.class_names[int(obj.label)])
        print(ids)
        #print("Tensor Processing1: " + str(time()-start_cycle))
        draw_detection_objects(image_data, net.class_names, objects)
        #sleep(0.05)
        #image.show()
        # update the FPS counter
        #fps.update()
        FPS = 1 / ( time() - start_cycle)
        print("FPS: " + str(FPS))
        if cv2.waitKey(1)==ord('q'):
            break
       
    # stop the timer and display FPS information
    #fps.stop()
    #print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

