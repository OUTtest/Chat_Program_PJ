# Chat_Program_PJ
 쳇 프로그램은 간단하게 방송을 할 수 있으며
 닉네임을 입력하여 간단하게 소통할 수 있는 채팅이 준비되어 있습니다.

## 사용 모듈

NumPy, OpenCV, ZeroMQ, Tkinter, socket

## Usage

server: 서버프로그램은 명령창에서 그대로 실행하면 서버가 실행 되면서 자신의 캠이 방송됩니다.

```
python main_server.py
```

As a client:
클라이언트 프로그램은 명령창에서 실행하게 되면 간단한 GUI가 접속 IP와 PORT를 묻습니다.
해당 PORT는 채팅 서버 접속 포트를 의미하며(기본값:10000) 비디오 접속 포트(5555)는 고정입니다.
```
python main_client.py
```
