from pickle import NONE
import socketserver
import socket
import threading
import sys
import zmq
import base64
import numpy as np
import cv2

class MyHandler(socketserver.BaseRequestHandler):
    users = {}
    print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

    def send_all_message(self, msg):
        for sock, _ in self.users.values():
            sock.send(msg.encode())
    
    def handle(self):
        print(self.client_address)
                
        while True:
            self.request.send("채팅 닉네임을 입력하세요".encode())
            nickname = self.request.recv(1024).decode()
            if nickname in self.users:
                self.request.send("이미 등록된 닉네임 입니다.\n".encode())
            else:
                self.users[nickname] = (self.request, self.client_address)
                print("현재 {} 명 참여중".format(len(self.users)))
                self.send_all_message("[{}] 님이 입장 했습니다.".format(nickname))
                break
                
        while True:
            msg = self.request.recv(1024)
            if msg.decode() == "/bye":
                self.request.close()
                break
            self.send_all_message("[{}] {}".format(nickname, msg.decode()))
            
        if nickname in self.users:
            del self.users[nickname]
            self.send_all_message("[{}]님이 퇴장하였습니다.".format(nickname))
            print("현재 {} 명 참여중".format(len(self.users)))
              

    


class ChatClient:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, addrs):
        self.sock.connect((addrs, 10000))
        th = threading.Thread(target=self.recv_message, args=(self.sock, ))
        th.daemon = True
        th.start()

    def recv_message(self, o_sock):
        while True:
            msg = o_sock.recv(1024)
            print(msg.decode())
        
    while True:
        msg = input("입력: ")
        sock.send(msg.encode())
    
        if msg == "/bye":
            break

    sock.close()

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

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if(len(sys.argv)>1):
    # viewer=Viewer(sys.argv[1])
    # viewer.run()
    chat_client = ChatClient(sys.argv[0])
else:
    # streamer=Streamer()
    # streamer.run()
    Chat_server = ChatServer(("", 10000), MyHandler)
    Chat_server.serve_forever()
    Chat_server.shutdown()
    Chat_server.server_close()