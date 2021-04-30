import paho.mqtt.client as mqtt

def make_connect(topics=[]):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"연결 성공")
            for topic in topics:
                client.subscribe(topic)  # 연결 성공시 토픽 구독 신청
        else:
            print('연결 실패 :  ', rc)

    return on_connect


def make_client(host, port=1883, topics=[], on_message=None, forever=False):
    client = mqtt.Client()
    client.on_connect = make_connect(topics)
    client.on_message = on_message
    client.connect(host)

    if forever:
        client.loop_forever()   # 현재 스레드에서 무한 루프를 돌며 메시지 처리
    else:
        client.loop_start()     # 새로운 스레드를 기동하고, 스레드가 무한 루프에서 메시지 처리 
    
    return client


# def subscribe(host, topic, on_message, forever=False):
#     client = mqtt.Client()
#     client.on_connect = make_connect(topic)
#     client.on_message = on_message
#     client.connect(host)

#     if forever:
#         client.loop_forever()   # 현재 스레드에서 무한 루프를 돌며 메시지 처리
#     else:
#         client.loop_start()     # 새로운 스레드를 기동하고, 스레드가 무한 루프에서 메시지 처리 
    
#     return client
