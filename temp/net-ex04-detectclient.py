from video import Video
import socket
import json
import net
import cv2
import numpy as np
from objdetect import ObjDetectApi, NumpyDecoder

PATH_TO_LABELS = 'data/mscoco_label_map.pbtxt'
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'

api = ObjDetectApi(MODEL_NAME, PATH_TO_LABELS)

HOST = '172.30.1.52'
PORT = 5000

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        writer = s.makefile('wb')
        reader = s.makefile('rb')
        with Video(device=0) as v:
            for image in v:
                # jpg 이미지 변환 및 전송
                jpg = Video.to_jpg(image)
                net.send(writer, jpg)

                # 처리 결과 수신
                output_dict = net.receive(reader)[0].decode()
                output_dict = json.loads(output_dict, cls=NumpyDecoder)
                print(output_dict)

                labeled_image = api.visualize(image, output_dict)
                cv2.imshow('frame', labeled_image)
                key = cv2.waitKey(1)
                if key == 27: 
                    break


    
