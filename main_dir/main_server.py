from pickle import NONE
import socketserver
import socket
import threading
import tkinter
import zmq
import base64
import cv2

class MyHandler(socketserver.BaseRequestHandler):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass             

class ChatClient:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = ""
    PORT = 0
    input_string = ""
    input_msg = ""
    chat_list = None
    window = None

    def recv_message(self,sock):
        while True:
            msg = sock.recv(1024)
            self.chat_list.insert(tkinter.END, msg.decode())
            self.chat_list.see(tkinter.END)

    def connect(self, event=None):       
        connect_string = self.input_string.get()
        addr = connect_string.split(":")
        self.IP = addr[0]
        self.PORT = int(addr[1])
        self.w_connect.destroy()

    def send_message(self, event=None):
        msg = self.input_msg.get()
        self.sock.send(msg.encode())
        self.input_msg.set("")

        if msg == "/bye":
            self.sock.close()
            self.window.quit()

    def connect_gui(self):
        #접속 창
        w_connect = tkinter.Tk()
        w_connect.title("접속대상")
        tkinter.Label(w_connect, text="접속대상").grid(row = 0, column = 0)

        input_string = tkinter.StringVar(value="127.0.0.1:10000")
        input_addr = tkinter.Entry(w_connect, textvariable=input_string, width=20)
        input_addr.grid(row=0, column=1, padx=5, pady=5)

        c_button = tkinter.Button(w_connect, text="접속하기",command=self.connect)
        c_button.grid(row=0, column= 2, padx=5, pady=5)

        width = 280
        height = 45

        screen_width = w_connect.winfo_screenwidth()                        #컴퓨터 해상도 계산
        screen_height = w_connect.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))                           #컴퓨터 해상도 계산하여 가운데의 좌표값을 계산
        y = int((screen_height / 2) - (height / 2))

        w_connect.geometry('{}x{}+{}+{}'.format(width, height, x, y))       #창을 실행하였을때 실행할 위치를 지정
        w_connect.mainloop()

        self.run()

    def run(self):
        # 채팅 구문
        self.window = tkinter.Tk()
        self.window.title("클라이언트")

        cg_frame = tkinter.Frame(self.window)
        scroll = tkinter.Scrollbar(cg_frame)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.chat_list = tkinter.Listbox(cg_frame, height=15, width=50, yscrollcommand= scroll.set)
        self.chat_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=5, pady=5)
        cg_frame.pack()

        self.input_msg = tkinter.StringVar()
        inputbox = tkinter.Entry(self.window, textvariable=self.input_msg)
        inputbox.bind("<Return>", self.send_message)
        inputbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, padx=5, pady=5)
        send_button = tkinter.Button(self.window, text="전송",command=self.send_message)
        send_button.pack(side=tkinter.RIGHT, fill=tkinter.X, padx=5, pady=5)

        # 소켓 생성과 스레드 작동부분
        self.sock.connect((self.IP, self.PORT))

        th = threading.Thread(target=self.recv_message, args=(self.sock,))
        th.daemon = True
        th.start()

        self.window.mainloop()

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

streamer = Streamer()
streamer.run()
Chat_server = ChatServer(("", 10000), MyHandler)
Chat_server.serve_forever()
Chat_server.shutdown()

Chat_server.server_close()