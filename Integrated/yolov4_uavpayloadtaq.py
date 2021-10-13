# Tencent is pleased to support the open source community by making ncnn available.
#
# Copyright (C) 2020 THL A29 Limited, a Tencent company. All rights reserved.
#
# Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import ncnn
from ncnn.utils.objects import Detect_Object
from time import time

class YoloV4_UAVPAYLOADTAQ:
    def __init__(self, target_size=192, num_threads=4, use_gpu=True):
        self.target_size = target_size
        self.num_threads = num_threads
        self.use_gpu = use_gpu

        self.mean_vals = []
        self.norm_vals = [1 / 255.0, 1 / 255.0, 1 / 255.0]

        self.net = ncnn.Net()
        self.net.opt.use_vulkan_compute = self.use_gpu
        self.net.opt.num_threads = self.num_threads
        #self.net.opt.use_sgemm_convolution = True
        #self.net.opt.use_winograd_convolution = True
        #self.net.opt.use_packing_layout = True
        #self.net.opt.use_shader_pack8 = True
        #self.net.opt.use_image_storage = True
        #self.net.opt.use_int8_inference = True
        #self.net.opt.use_int8_packed = True
        #self.net.opt.use_int8_storage = True
        #self.net.opt.use_int8_arithmetic = True

        # original pretrained model from https://github.com/AlexeyAB/darknet
        # the ncnn model https://drive.google.com/drive/folders/1YzILvh0SKQPS_lrb33dmGNq7aVTKPWS0?usp=sharing
        # the ncnn model https://github.com/nihui/ncnn-assets/tree/master/models
        self.net.load_param("models/uavpayloadtaq-yolov4-tiny-192-detector-merge-opt-fp16.param")
        
        self.net.load_model("models/uavpayloadtaq-yolov4-tiny-192-detector-merge-opt-fp16.bin")
 
        
        self.class_names = [
            "background",
            "target_backpack",
            "target_person"
        ]

    def __del__(self):
        self.net = None

    def __call__(self, img):
        img_h = img.shape[0]
        img_w = img.shape[1]

        mat_in = ncnn.Mat.from_pixels_resize(
            img,
            ncnn.Mat.PixelType.PIXEL_RGB,
            img.shape[1],
            img.shape[0],
            self.target_size,
            self.target_size,
        )
        mat_in.substract_mean_normalize(self.mean_vals, self.norm_vals)
        #print(mat_in)

        ex = self.net.create_extractor()
        ex.set_light_mode(True)
        ex.input("data", mat_in)
        #start_time = time()
        ret, mat_out = ex.extract("yolo0")
        
        #print("Op Time: " + str(time() - start_time))

        objects = []

        # method 1, use ncnn.Mat.row to get the result, no memory copy
        for i in range(mat_out.h):
            values = mat_out.row(i)

            obj = Detect_Object()
            obj.label = values[0]
            obj.prob = values[1]
            obj.rect.x = values[2] * img_w
            obj.rect.y = values[3] * img_h
            obj.rect.w = values[4] * img_w - obj.rect.x
            obj.rect.h = values[5] * img_h - obj.rect.y

            objects.append(obj)

        """
        #method 2, use ncnn.Mat->numpy.array to get the result, no memory copy too
        out = np.array(mat_out)
        for i in range(len(out)):
            values = out[i]
            obj = Detect_Object()
            obj.label = values[0]
            obj.prob = values[1]
            obj.x = values[2] * img_w
            obj.y = values[3] * img_h
            obj.w = values[4] * img_w - obj.x
            obj.h = values[5] * img_h - obj.y
            objects.append(obj)
        """

        return objects
