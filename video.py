import cv2

class Video:
    def __init__(self, **kargs):
        device = kargs.get('device', -1)
        file = kargs.get('file')
        if device >=0 :
            self.cap = cv2.VideoCapture(device)
        elif file:
            self.cap = cv2.VideoCapture(file)

    def __iter__(self):
        return self

    def __next__(self):
        ret, image = self.cap.read()
        if ret:
            return image
        else:
            raise StopIteration

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace_back):
        if self.cap and self.cap.isOpened():
            # print('video release-----')
            self.cap.release()

    @staticmethod
    def to_jpg(frame, quality=80):
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),quality]
        is_success, jpg = cv2.imencode(".jpg", frame, encode_param)
        return jpg

    @staticmethod
    def show(image, exit_char=ord('q')):
        cv2.imshow('frame',image)
        if cv2.waitKey(1) & 0xFF == exit_char:
            return False
        return True

    @staticmethod
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    @staticmethod
    def resize_frame(frame, width, height):
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

if __name__ == '__main__':
    with Video(device=1) as v:
        for image in v:
            # jpg = Video.to_jpg(image, 60)
            image = Video.resize_frame(image, 320, 240)
            # image = Video.rescale_frame(image, 50)
            if not Video.show(image): break










