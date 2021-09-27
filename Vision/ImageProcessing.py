import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
import cv2
from PIL import Image
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from CameraHelper2 import CameraHelper
from time import time, sleep
import imutils
from imutils.video import FPS

score = 0.3
iou = 0.5
input_size = 192
def main(_argv):
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config()
    
    counter = 0

    cameraHelper = CameraHelper().start()
    fps = FPS().start()
    sleep(2)
    interpreter = tf.lite.Interpreter(model_path="./models/tflite/uavpayloadtaq_yolov4-tiny-192-fp16.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    



    while True:

        start_cycle = time()
        original_image = cameraHelper.getImage()
        
        print("Image Collection: " + str(time()-start_cycle))
        
        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.        

        images_data = []
        for i in range(1):
            images_data.append(image_data)
        images_data = np.asarray(images_data).astype(np.float32)

        print("Image Preprocessing: " + str(time()-start_cycle))
        
        interpreter.set_tensor(input_details[0]['index'], images_data)
        
        interpreter.invoke()
        print("Tensor Processing1: " + str(time()-start_cycle))
        pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.3, input_shape=tf.constant([input_size, input_size]))
        

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=5,
            max_total_size=5,
            iou_threshold=iou,
            score_threshold=score
        )
        print("Tensor Processing2: " + str(time()-start_cycle))
        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        image = utils.draw_bbox(original_image, pred_bbox)
        # image = utils.draw_bbox(image_data*255, pred_bbox)
        image = Image.fromarray(image.astype(np.uint8))
        print("Final Image Processing: " + str(time()-start_cycle))
        print(str(counter))
        counter = counter + 1
        #sleep(0.05)
        #image.show()
        # update the FPS counter
        fps.update()
       
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

