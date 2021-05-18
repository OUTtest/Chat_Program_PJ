import socket
import threading
import sys
import zmq
import base64
import numpy as np
import cv2

class ChatServer:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connections=[]                          # 채팅에 참가한 유저의 정보를 담는다.

    def __init__(self):
        self.sock.bind(('0.0.0.0',10000))   # 바인드 10000포트에 자신의 IP로 접속 대기
        self.sock.listen(1)                 # 접속 대기 상태
        print("Server running on: ")
        print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
        # 접속 수락과 소켓을 따로 생성하는 역할을 수행

    def handler(self,c,a):                 
        while True:
            data=c.recv(1024)                                   #보낸 채팅 데이터를 받는다.
            for connection in self.connections:
                if(connection!=c):                              #연결 리스트를 확인 하면서 본인이 아닌 다른 사람에게 전체적으로 채팅을 전송한다.
                    connection.send(data)
            if not data:                                        #데이터를 받는 걸 실패하면 그 사용자를 이상 사용자라 판단하고 접속을 종료시킨다.
                print(str(a[0])+':'+str(a[1]),"disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c,a=self.sock.accept()                                      # c는 소켓정보, a는 해당 소켓의 주소 정보를 받는다.
            cThread=threading.Thread(target=self.handler,args=(c,a))    # 핸들러 클래스를 스레드로 활성화
            cThread.daemon=True
            cThread.start()
            self.connections.append(c)
            print(str(a[0])+':'+str(a[1]),"connected")

class ChatClient:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    user_name=""

    def sendMsg(self):
        while True:
            msg=input("")
            self.sock.send(bytes(self.user_name+"\t: "+msg,'utf-8'))

    def __init__(self,address,user_name):                                   # 처음 실행되면 연결할 IP와 유저 이름을 받는다.
        self.user_name=user_name
        self.sock.connect((address,10000))                                  # 해당 주소의 10000포트로 접속한다.
        iThread=threading.Thread(target=self.sendMsg)                       # 스레드를 이용하여 sendMsg를 실행한다.
        iThread.daemon=True
        iThread.start()

        while True:
            data=self.sock.recv(1024)                                       # 서버에서 보낸 체팅 데이터를 받는다.
            if not data:
                break
            print(str(data,'utf-8'))

class Streamer:
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    camera = cv2.VideoCapture(0)

    def __init__(self):
        self.footage_socket.bind('tcp://*:5555')                # tcp통신으로 5555포트를 이용하여 통신한다.

    def video(self):
        while True:
            try:
                grabbed, frame = self.camera.read()             # 현재 카메라의 프레임을 가져온다.
                frame = cv2.resize(frame, (640, 480))           # 프레임의 크기를 조정한다.
                encoded, buffer = cv2.imencode('.jpg', frame)   # 프레임을 jpg 파일로 전환하고
                jpg_as_text = base64.b64encode(buffer)          # 변환된 파일을 base64 형태로 인코딩 후에
                self.footage_socket.send(jpg_as_text)           # base64형태로 전송한다.

            except KeyboardInterrupt:                           # KeyboardInterrupt가 일어나면 프로그램을 종료한다.
                self.camera.release()
                cv2.destroyAllWindows()
                break

    def run(self):
        videoThread=threading.Thread(target=self.video) 
        videoThread.daemon=True
        videoThread.start()

class Viewer:
    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)

    def __init__(self,address):                                            # 처음 실행할때 인자 값으로 주소값을 받는다.
        self.footage_socket.connect('tcp://'+address+':5555')                   
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    def video(self):
        while True:
            try:
                frame = self.footage_socket.recv_string()                   # 해당 서버에서 전송한 값을 받는다.
                img = base64.b64decode(frame)                               # Base64 파일을 디코드 한다.
                npimg = np.fromstring(img, dtype=np.uint8)                  # 디코드한 파일을 Array형태의 데이터로 전환
                source = cv2.imdecode(npimg, 1)                             # Array형태의 데이터를 이미지로 전환
                cv2.imshow("Stream", source)                                # Stream이란 이름으로 이미지 출력
                cv2.waitKey(1)

            except KeyboardInterrupt:                                       # KeyboardInterrupt가 입력되면 모든 창을 닫는다.
                cv2.destroyAllWindows()
                break

    def run(self):
        videoThread=threading.Thread(target=self.video)
        videoThread.daemon=True
        videoThread.start()

if(len(sys.argv)>1):
    viewer=Viewer(sys.argv[1])
    viewer.run()
    client=ChatClient(sys.argv[1],sys.argv[2])
else:
    streamer=Streamer()
    streamer.run()
    server=ChatServer()
    server.run()