from video import Video
from time import sleep
import socket
import json
import net
HOST = '127.0.0.1'
PORT = 5000

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        writer = s.makefile('wb')
        reader = s.makefile('rb')
        with Video(device=0) as v:
            for image in v:
                # jpg 이미지 변환 및 전송
                image = Video.to_jpg(image)
                net.send(writer, image)
                # net.send(writer, image.tobytes())
                # 처리 결과 수신
                result = net.receive(reader)[0]
    
