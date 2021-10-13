
from absl import app, flags, logging
import core.utils as utils
#from core.yolov4 import filter_boxes
import cv2
from PIL import Image
import numpy as np

from CameraHelper2 import CameraHelper
from time import time, sleep
import imutils
from imutils.video import FPS
from yolov4_uavpayloadtaq import YoloV4_UAVPAYLOADTAQ as search_model

import ncnn
#from ncnn.model_zoo import get_model
from draw_detect import draw_detection_objects

score = 0.3
iou = 0.5
input_size = 416
def main(_argv):
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config()
    
    

    #cameraHelper = CameraHelper().start()
    fps = FPS().start()
    sleep(1)
    #net = get_model("yolov4_tiny", num_threads=4, use_gpu=True)
    net = search_model()
    #net = ncnn.ncnn.Net()
    #net.load_param("uavpayloadtaq_yolov4-tiny-320-merge-opt-fp16.param")
    #net.load_model("uavpayloadtaq_yolov4-tiny-320-merge-opt-fp16.bin")
     

    while True:

        start_cycle = time()
        #original_image = cameraHelper.getImage()
        
        print("Image Collection: " + str(time()-start_cycle))
        
        #image_data = cv2.resize(original_image, (input_size, input_size))
        #image_data = image_data / 255.        
        #image_data = cameraHelper.getImage()
        image_data = cv2.imread("./test.jpg")
        #images_data = []
        
        
        
        #for i in range(1):
        #    images_data.append(image_data)
        #images_data = np.asarray(images_data).astype(np.float32)

        print("Image Preprocessing: " + str(time()-start_cycle))
        
        objects = net(image_data)
        print(objects)
        print("Tensor Processing1: " + str(time()-start_cycle))
        draw_detection_objects(image_data, net.class_names, objects)
        #sleep(0.05)
        #image.show()
        # update the FPS counter
        fps.update()
        if cv2.waitKey(1)==ord('q'):
            break
       
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

