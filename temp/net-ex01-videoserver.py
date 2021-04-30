import net
import json

import cv2
import numpy as np

HOST = '127.0.0.1'
PORT = 5000

def show_image(data):
    # byte 배열을 numpy로 변환 
    data = np.frombuffer( data , dtype = np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('frame', image)


def receiver(client, addr):
    reader = client.makefile('rb')
    writer = client.makefile('wb')
    while True:
        data, data_len = net.receive(reader)
        if not data :
            break
        print('received ', data_len)
        show_image(data)
        result = json.dumps({ 'result': 'ok'})
        net.send(writer, result.encode())
        
    # 이미지 처리 
    print('exit receiver')

print('start server...')
net.server(HOST, PORT, receiver)
