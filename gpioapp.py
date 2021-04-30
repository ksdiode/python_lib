import RPi.GPIO as GPIO
import time


class GPIOApplication:
    def __init__(self):
        # GPIO핀의 번호 모드 설정
        GPIO.setmode(GPIO.BCM)
        self.pin_init()

    def pin_init(self):
        pass

    def work(self):
        while 1:  #무한반복
            time.sleep(0.1)    # 0.1초 딜레이 		# 1초동안 대기상태

    def destroyed(self):
        GPIO.cleanup()     				# GPIO 설정 초기화 

    def run(self):
        try:
           self.work()
        except KeyboardInterrupt as ke:
            pass
        except Exception as e:
            print(e)
        finally:
            self.destroyed()
