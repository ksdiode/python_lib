import socket
import struct
from threading import Thread

# 현재 스레드에서 서버 기동
def server(ip, port, thread_fn):
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        try:
            s.bind((ip, port))
            s.listen(1)     
            while True:
                client_socket, addr = s.accept()	# 접속 대기
                # 스레드 기동
                t = Thread(thread_fn, (client_socket, addr)) 
                t.setDaemon(True)
                t.start()
        except Exception as e:
            print(e)

# 서버 기동
def start_server(ip, port, thread_fn, forever=True):
    if forever: # 현재 스레드에서 서버 기동
        server(ip, port, thread_fn, daemon=True)
    else:   # 새로운 스레드에서 서버 기동
        t = Thread(server, (ip, port, thread_fn))
        t.setDaemon(True)
        t.start()


def send(writer, data):
    writer.write(struct.pack('<L', len(data)))
    writer.write(data)
    writer.flush()


def receive(reader):
    # 이미지 크기 수신 및 unpack
    data_len = reader.read(struct.calcsize('<L'))
    data_len = struct.unpack('<L', data_len)[0]

    if not data_len:    # 이미지 크기, 이미지 데이터  --> 0
        return (None, 0)

    # data_len 만큼 이미지 데이터 읽기
    data = reader.read(data_len)
    return (data, data_len)



def work(client_socket, addr):
    pass




if __name__ == '__main__':
    server('localhost', 9090, work)