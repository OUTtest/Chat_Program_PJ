import socket
from threading import Thread

class Chat_Server():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    users ={}

    def __init__(self):
        self.sock.bind(('127.0.0.1',13000))
        self.sock.listen(1)
        print("server is running")
        
    def send_all_message(self, msg):
        for sock, addr in self.users.values():
            sock.send(msg.encode())

    def handler(self,request,addr):
        print(addr+'conneted')
        while True:
            request.send("채팅 닉네임을 입력하세요".encode())
            nickname = request.recv(1024).decode()
            if nickname in self.users:
                request.send("이미 등록된 닉네임 입니다.\n".encode())
            else:
                self.users[nickname] = (request, addr)
                print("현재 {} 명 참여중".format(len(self.users)))
                self.send_all_message("[{}]님이 입장하였습니다.".format(nickname))
                break

        while True:
            msg = request.recv(1024)

            if msg.decode() == "/bye":
                request.close()
                break
            self.send_all_message("[{}] : {}".format(nickname, msg.decode()))

        if nickname in self.users[nickname]:
            del self.users[nickname]
            self.send_all_message("[{}]님이 퇴장하였습니다.".foramt(nickname))
            print("현재 {}명 참여중".format(len(self.users)))

    def run(self):
        c_sock, addr = self.sock.accept()
        self.handler(c_sock,addr)
        cThread=Thread(target=self.handler,args=(c_sock,addr))
        cThread.daemon=True
        cThread.start()
        print(str(addr[0])+':'+str(addr[1]),"connected")


if '__main__' ==  __name__:
    server = Chat_Server()
    server.run()
