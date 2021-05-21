import tkinter
import socket
from threading import Thread

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

screen_width = w_connect.winfo_screenwidth()
screen_height = w_connect.winfo_screenheight()

x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))

w_connect.geometry('{}x{}+{}+{}'.format(width, height, x, y))
w_connect.mainloop()

window = tkinter.Tk()
window.title("클라이언트")




# 채팅 구문
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

th = Thread(target=recv_message, args=(sock,))
th.daemon = True
th.start()

window.mainloop()