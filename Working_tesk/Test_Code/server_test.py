import socket
from threading import Thread

class Chat_Server():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    users ={}

    def __init__(self):
        self.sock.bind(('127.0.0.1',13000))
        self.sock.listen(1)
        print("server is running")    

    def handler(self, request, addr):

        while True:
            request.send("채팅 닉네임을 입력하세요".encode())
            nickname = request.recv(1024)

            if nickname in self.users:
                request.send("이미 등록된 닉네임 입니다.\n".encode())
            else:
                self.users[nickname] = (request, addr)
                print("현재 {} 명 참여중".format(len(self.users)))

                for sock, addr in self.users.values():
                    sock.send("[{}]님이 입장하였습니다.".format(nickname.decode()).encode())
                break

        while True:
            msg = request.recv(1024)

            if msg.decode() == "/bye":
                request.close()
                break

            for sock, addr in self.users.values():
                    sock.send("[{}] : {}".format(nickname.decode(), msg.decode()).encode())

        if nickname in self.users[nickname]:
            del self.users[nickname]
            for sock, addr in self.users.values():
                    sock.send("[{}]님이 퇴장하였습니다.".foramt(nickname.decode()).encode())
            print("현재 {}명 참여중".format(len(self.users)))

    def run(self):
        while True:
            c_sock, addr = self.sock.accept()
            self.handler(c_sock, addr)
            Th1=Thread(target=self.handler,args=(c_sock,addr))
            Th1.daemon=True
            Th1.start()
            print(str(addr[0])+':'+str(addr[1]),"connected")
        


if '__main__' ==  __name__:
    server = Chat_Server()
    server.run()
