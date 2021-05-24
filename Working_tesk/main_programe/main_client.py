import tkinter
import socket
import threading
import zmq
import base64
import numpy as np
import cv2

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

if '__main__'== __name__ :
    # view = Viewer
    # view.run()
    pass

IP = ""
PORT = 0

def recv_message(sock):
    while True:
        msg = sock.recv(1024)
        chat_list.insert(tkinter.END, msg.decode())
        chat_list.see(tkinter.END)

def connect(event=None):
    global IP, PORT
    connect_string = input_string.get()
    addr = connect_string.split(":")
    IP = addr[0]
    PORT = int(addr[1])
    w_connect.destroy()

def send_message(event=None):
    msg = input_msg.get()
    sock.send(msg.encode())
    input_msg.set("")

    if msg == "/bye":
        sock.close()
        window.quit()


#접속 창
w_connect = tkinter.Tk()
w_connect.title("접속대상")
tkinter.Label(w_connect, text="접속대상").grid(row = 0, column = 0)

input_string = tkinter.StringVar(value="127.0.0.1:10000")
input_addr = tkinter.Entry(w_connect, textvariable=input_string, width=20)
input_addr.grid(row=0, column=1, padx=5, pady=5)

c_button = tkinter.Button(w_connect, text="접속하기",command=connect)
c_button.grid(row=0, column= 2, padx=5, pady=5)


width = 280
height = 45

screen_width = w_connect.winfo_screenwidth()            #컴퓨터 해상도 계산
screen_height = w_connect.winfo_screenheight()

x = int((screen_width / 2) - (width / 2))               #컴퓨터 해상도 계산하여 가운데의 좌표값을 계산
y = int((screen_height / 2) - (height / 2))

w_connect.geometry('{}x{}+{}+{}'.format(width, height, x, y))       #창을 실행하였을때 실행할 위치를 지정
w_connect.mainloop()


# 채팅 구문

window = tkinter.Tk()
window.title("클라이언트")

cg_frame = tkinter.Frame(window)
scroll = tkinter.Scrollbar(cg_frame)
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

chat_list = tkinter.Listbox(cg_frame, height=15, width=50, yscrollcommand= scroll.set)
chat_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=5, pady=5)
cg_frame.pack()

input_msg = tkinter.StringVar()
inputbox = tkinter.Entry(window, textvariable=input_msg)
inputbox.bind("<Return>", send_message)
inputbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, padx=5, pady=5)
send_button = tkinter.Button(window, text="전송",command=send_message)
send_button.pack(side=tkinter.RIGHT, fill=tkinter.X, padx=5, pady=5)


# 소켓 생성과 스레드 작동부분
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

th = threading.Thread(target=recv_message, args=(sock,))
th.daemon = True
th.start()

window.mainloop()