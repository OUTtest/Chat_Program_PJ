from server_test import Chat_Server
import socket
from threading import Thread

class Chat_server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users = {}

    def __init__(self):
        self.sock.bind(('localhost',13000))
        self.sock.listen(1)
        print("server is running")

    def send_all_message(self,msg):
        for sock, addr in self.users.values():
            sock.send(msg.encode())

    def handel(self,sock,addr):
        print(addr)

        while True:
            sock.send("채팅 이름을 입력하세요 :".encode())
            nickname = sock.recv(1024).decode()
            if nickname in self.users:
                sock.send("이미 등록된 이름입니다. 다른 닉네임을 입력하세요 \n".encode())
            else:
                self.users[nickname] = (sock,addr)
                print("현재 접속중인 인원은 {}명입니다.".format(len(self.users)))
                self.send_all_name("[{}]님이 입장하였습니다.".format(nickname))
                break
        
        while True:
            msg = sock.recv(1024)

            if msg.decode() == "/bye":
                sock.close()
                break
            self.send_all_message("[{}]: {}".format(nickname,msg.decode()))
        
        if nickname in self.users:
            del self.users[nickname]
            self.send_all_message(nickname,"[{}]님이 퇴장하였습니다.".format(nickname))
            print("현재 접속중이 인원은 {}명 입니다.".format(len(self.users)))
            
    def run(self):
        sock, addr = self.sock.accept()
        cThread=Thread(target=self.handel,args=(sock,addr))
        cThread.daemon=True
        cThread.start()
        print(str(addr[0])+':'+str(addr[1]),"connected")

if "__main__" == __name__:
    Server = Chat_Server()
    Server.run()
        



