import cv2
from cvcamera import Camera
import img_util 
from threading import Thread

class VideoFrame:
    def __init__(self, camera, title='Image'):
        self.camera = camera    # 사용할 카메라
        self.is_run = False     # 운영 여부
        self.thread = None      # 운영 스레드
        self.title = title      # 프레임 윈도우 타이틀
        

    def show(self, process=None):
        # 이미 운영 중이면 리턴
        if self.is_run and self.thread : return

        self.is_run = True
        self.thread = Thread(target=self.run, args=(process,))
        self.thread.setDaemon(True)
        self.thread.start()


    def run(self, process = None):
        try:
            while self.is_run:
                image = self.camera.image
                if process: process(image)
                img_util.show(image, title=self.title)
        except:
            self.is_run = False
            self.thread = None

        cv2.destroyWindow(self.title)
        

    def close(self):
        self.is_run = False
        if self.thread: self.thread.join()  # 운영 스레드가 종료할 때까지 대기
        self.thread = None
        
if __name__ == '__main__':
    camera = Camera(device=0)
    frame = VideoFrame(camera)

    while True:
        ans = int(input('명령 1: 비디오켜기, 2: 비디오끄기, 3: 종료'))
        if ans == 1:
            frame.show()
        elif ans == 2:
            frame.close()
        elif ans==3:
            break
        else:
            print('없는 명령입니다.')



