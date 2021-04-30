import cv2
import numpy as np

def to_jpg(frame, quality=80):
    encode_param=[cv2.IMWRITE_JPEG_QUALITY, quality]
    _, jpg = cv2.imencode(".jpg", frame, encode_param)
    return jpg


def to_bgr(jpg):
    data = np.frombuffer(jpg, dtype=np.uint8)	# byte 배열 -> Numpy 배열
    bgr = cv2.imdecode(data, cv2.IMREAD_COLOR) # jpg 이미지 -> BGR 이미지
    return bgr


def show(image, delay = 1, title = 'frame', exit_char=ord('q')):
    cv2.imshow(title, image)
    if cv2.waitKey(1) & 0xFF == exit_char:
        raise Exception('비디오 Show 종료')


def rescale(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


def resize(frame, width, height):
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)