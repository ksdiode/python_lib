import cv2
from cv2.data import haarcascades
from os import path
from video import Video
import sys

face_xml = path.join(haarcascades, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_xml)


FACE_WIDTH = 200

def detect_face(frame):
    # 흑백 영상 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 이미지에서 얼굴 검출
    # 얼굴이 검출되었다면 얼굴 위치에 대한 좌표 정보 리스트
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        # 원본 이미지에 얼굴의 위치를 표시
        # cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        minLength = min(w, h)
        if minLength < 150: break   # 너무 작은 영역은 무시
        width = max(w, h)
        
        # 얼굴 부분 검출
        x = x + w//2 - width//2
        y = y + h//2 - width//2
        
        # 얼굴 영역 표시
        cv2.rectangle(frame,(x,y),(x+width,y+width),(255,0,0),2)
        face_image = frame[y:y+width, x:x+width].copy()

        # 얼굴 부분만 좌측 상단에 출력
        face_image = cv2.resize(face_image,
                                dsize=(FACE_WIDTH, FACE_WIDTH), 
                                interpolation=cv2.INTER_AREA)
        frame[0:FACE_WIDTH, 0:FACE_WIDTH] = face_image[:]
  
    return frame


if __name__ == "__main__":
    with Video(device=0) as v:
        for image in v:
            image = detect_face(image)
            # 보여주기
            cv2.imshow('frame', image)    
            key = cv2.waitKey(1)
            if key == 27: break

    cv2.destroyAllWindows()
