import socket
import threading
import sys
import zmq
import base64
import numpy as np
import cv2
from collections import deque

class ChatServer:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connections=[]

    def __init__(self):
        self.sock.bind(('0.0.0.0',10000))
        self.sock.listen(1)
        print("Server running on: ")
        print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])


    def handler(self,c,a):
        while True:
            data=c.recv(1024)
            for connection in self.connections:
                if(connection!=c):
                    connection.send(data)
            if not data:
                print(str(a[0])+':'+str(a[1]),"disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c,a=self.sock.accept()
            cThread=threading.Thread(target=self.handler,args=(c,a))
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
    def __init__(self,address,user_name):
        self.user_name=user_name
        self.sock.connect((address,10000))
        iThread=threading.Thread(target=self.sendMsg)
        iThread.daemon=True
        iThread.start()

        while True:
            data=self.sock.recv(1024)
            if not data:
                break
            print(str(data,'utf-8'))

class Streamer:
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    camera = cv2.VideoCapture(0)

    def __init__(self):
        self.footage_socket.bind('tcp://*:5555')

    def video(self):
        while True:
            try:
                grabbed, frame = self.camera.read()  # grab the current frame
                # frame = cv2.resize(frame, (640, 480))  # resize the frame
                encoded, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                self.footage_socket.send(jpg_as_text)
                streamer.paint()

            except KeyboardInterrupt:
                self.camera.release()
                cv2.destroyAllWindows()
                break

    def run(self):
        videoThread=threading.Thread(target=self.video)
        videoThread.daemon=True
        videoThread.start()

    def paint(self):
        # Define the upper and lower boundaries for a color to be considered "Blue"
        blueLower = np.array([100, 60, 60])
        blueUpper = np.array([140, 255, 255])

        # Define a 5x5 kernel for erosion and dilation
        kernel = np.ones((5, 5), np.uint8)

        # Setup deques to store separate colors in separate arrays
        bpoints = [deque(maxlen=512)]
        gpoints = [deque(maxlen=512)]
        rpoints = [deque(maxlen=512)]
        ypoints = [deque(maxlen=512)]

        bindex = 0
        gindex = 0
        rindex = 0
        yindex = 0

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        colorIndex = 0

        # Setup the Paint interface
        paintWindow = np.zeros((471, 636, 3)) + 255
        paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
        paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
        paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
        paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
        paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)
        cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

        cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

        # Load the video
        camera = cv2.VideoCapture(0)

        # Keep looping
        while True:
            # Grab the current paintWindow
            (grabbed, frame) = camera.read()
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Add the coloring options to the frame
            frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
            frame = cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
            frame = cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
            frame = cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
            frame = cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
            cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

            # Check to see if we have reached the end of the video
            if not grabbed:
                break

            # Determine which pixels fall within the blue boundaries and then blur the binary image
            blueMask = cv2.inRange(hsv, blueLower, blueUpper)
            blueMask = cv2.erode(blueMask, kernel, iterations=2)
            blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
            blueMask = cv2.dilate(blueMask, kernel, iterations=1)

            # Find contours in the image
            (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)
            center = None

            # Check to see if any contours were found
            if len(cnts) > 0:
                # Sort the contours and find the largest one -- we
                # will assume this contour correspondes to the area of the bottle cap
                cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
                # Get the radius of the enclosing circle around the found contour
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                # Draw the circle around the contour
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                # Get the moments to calculate the center of the contour (in this case Circle)
                M = cv2.moments(cnt)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

                if center[1] <= 65:
                    if 40 <= center[0] <= 140:  # Clear All
                        bpoints = [deque(maxlen=512)]
                        gpoints = [deque(maxlen=512)]
                        rpoints = [deque(maxlen=512)]
                        ypoints = [deque(maxlen=512)]

                        bindex = 0
                        gindex = 0
                        rindex = 0
                        yindex = 0

                        paintWindow[67:, :, :] = 255
                    elif 160 <= center[0] <= 255:
                        colorIndex = 0  # Blue
                    elif 275 <= center[0] <= 370:
                        colorIndex = 1  # Green
                    elif 390 <= center[0] <= 485:
                        colorIndex = 2  # Red
                    elif 505 <= center[0] <= 600:
                        colorIndex = 3  # Yellow
                else:
                    if colorIndex == 0:
                        bpoints[bindex].appendleft(center)
                    elif colorIndex == 1:
                        gpoints[gindex].appendleft(center)
                    elif colorIndex == 2:
                        rpoints[rindex].appendleft(center)
                    elif colorIndex == 3:
                        ypoints[yindex].appendleft(center)
            # Append the next deque when no contours are detected (i.e., bottle cap reversed)
            else:
                bpoints.append(deque(maxlen=512))
                bindex += 1
                gpoints.append(deque(maxlen=512))
                gindex += 1
                rpoints.append(deque(maxlen=512))
                rindex += 1
                ypoints.append(deque(maxlen=512))
                yindex += 1

            # Draw lines of all the colors (Blue, Green, Red and Yellow)
            points = [bpoints, gpoints, rpoints, ypoints]
            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                        cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

            # Show the frame and the paintWindow image
            cv2.imshow("Tracking", frame)
            cv2.imshow("Paint", paintWindow)

            # If the 'q' key is pressed, stop the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # # Cleanup the camera and close any open windows
        # camera.release()
        # cv2.destroyAllWindows()

class Viewer:
    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)

    def __init__(self,address):
        self.footage_socket.connect('tcp://'+address+':5555')
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    def video(self):
        while True:
            try:
                frame = self.footage_socket.recv_string()
                img = base64.b64decode(frame)
                npimg = np.fromstring(img, dtype=np.uint8)
                source = cv2.imdecode(npimg, 1)
                cv2.imshow("Stream", source)
                cv2.waitKey(1)

            except KeyboardInterrupt:
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