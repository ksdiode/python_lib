import cv2

class Camera():
    def __init__(self, **kargs):
        device = kargs.get('device', -1)
        file = kargs.get('file')
        self.format = kargs.get('format', 'bgr')
        if device >=0: self.cap = cv2.VideoCapture(device)
        elif file: self.cap = cv2.VideoCapture(file)

    @property
    def image(self):
        _, frame = self.cap.read()
        if self.format == 'jpg':
            frame = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80]) 
        return frame

    @property
    def jpg(self):
        ret, image = self.cap.read()
        if ret:
            _, image = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 80])    
        return image

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace_back):
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def __iter__(self):
        return self

    def __next__(self):
        return self.image