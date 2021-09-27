
from absl import app, flags, logging
import core.utils as utils
from core.yolov4 import filter_boxes

import cv2
from PIL import Image
import numpy as np
#import onnx
#import onnxruntime as rt
from CameraHelper2 import CameraHelper
from time import time, sleep
import imutils
from imutils.video import FPS


score = 0.3
iou = 0.5
input_size = 320
def main(_argv):
    #config = ConfigProto()
    #config.gpu_options.allow_growth = True
    #session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config()
    
    counter = 0

    cameraHelper = CameraHelper().start()
    fps = FPS().start()
    sleep(2)
    #interpreter = tf.lite.Interpreter(model_path="./uavpayloadtaq_yolov4-tiny-320.tflite")
    #interpreter.allocate_tensors()
    #input_details = interpreter.get_input_details()
    #output_details = interpreter.get_output_details()
    
    net = cv2.dnn.readNetFromDarknet('models/darknet/uavpayloadtaq-yolov4-tiny-320-detector.cfg', 'models/darknet/uavpayloadtaq_yolov4-tiny-320_final.weights')
    #net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    ln = net.getLayerNames()
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(input_size, input_size), scale = 1/255, swapRB = True)
    
    
    #sess = rt.InferenceSession("model.onnx")
    #input_name = sess.get_inputs()[0].name

    while True:

        start_cycle = time()
        original_image = cameraHelper.getImage()

        print("Image Collection: " + str(time()-start_cycle))
        blob = cv2.dnn.blobFromImage(original_image, 1/255.0, (input_size, input_size), swapRB=True, crop=False)
        #image_data = cv2.resize(original_image, (input_size, input_size))
        #image_data = image_data / 255.        

        #images_data = []
        #for i in range(1):
        #    images_data.append(image_data)
        #images_data = np.asarray(images_data).astype(np.float32)
        #blob = cv2.dnn.blobFromImage(images_data, 1, (input_size, input_size))
        
        
        print("Image Preprocessing: " + str(time()-start_cycle))
        
        
        #outputs = sess.get_outputs()
        #output_names = list(map(lambda output: output.name, outputs))
        net.setInput(blob)
        
        outputs = net.forward(ln)
        #for (classid, score, box) in zip(classes, scores, boxes):
        #   color = COLORS[int(classid) % len(COLORS)]
        #   label = "%s : %f" % (class_names[classid[0]], score)
        #   cv2.rectangle(frame, box, color, 2)
        #   cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        #detections = sess.run(output_names, {input_name: image_data})
        #print("Output shape:", list(map(lambda detection: detection.shape, detections)))
        print("Tensor Processing1: " + str(time()-start_cycle))
        
        #pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        #boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.3, input_shape=tf.constant([input_size, input_size]))
        

        #boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        #    boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        #    scores=tf.reshape(
        #        pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        #    max_output_size_per_class=5,
        #    max_total_size=5,
        #    iou_threshold=iou,
        #    score_threshold=score
        #)
        print("Tensor Processing2: " + str(time()-start_cycle))
        #pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        #image = utils.draw_bbox(original_image, pred_bbox)
        # image = utils.draw_bbox(image_data*255, pred_bbox)
        #image = Image.fromarray(image.astype(np.uint8))
        print("Final Image Processing: " + str(time()-start_cycle))
        #fps.update()
        #fps_label = "FPS: {:.2f}".format(fps.elapsed())
        #cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
       
    # stop the timer and display FPS information
    fps.stop()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

