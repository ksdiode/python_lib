import cv2
import requests
import io
from video import Video
from time import sleep

def send_image(url, data):
    stream = io.BytesIO(data)
    res = requests.post(url, 
            # files= {'image': ('image_data', stream)})   # 파일명, 데이터
            files= {'image': stream})   # 파일명, 데이터
    if res.status_code == 200:
        return True
    return False

url = 'http://localhost:8000/api/image_upload'
if __name__ == '__main__':
    with Video(device=0) as v:
        for image in v:
            image = Video.to_jpg(image)
            send_image(url, image)
            sleep(1)
    
