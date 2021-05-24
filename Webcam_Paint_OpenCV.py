import numpy as np
import cv2
from collections import deque

# Define the upper and lower boundaries for a color to be considered "Blue"  ->  포인트 색(파랑) 범위 지정 
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

print('|1. Black | 2. Blue | 3. Yellow | 4. Red | 5. Sky | 6. Purple | 7. Lime | 8. Pink |')    # 몇가지 색을 저장해둔 뒤 시작할때 불러올수 있는 코드
co1 = int(input('첫번째 색을 입력하세요.... '))      # 1~8 번까지 색 입력 코드 추가
if co1 == 1:
    x1=0
    y1=0
    z1=0
elif co1 == 2:
    x1=0
    y1=0
    z1=255
elif co1 == 3:
    x1=0
    y1=255
    z1=255
elif co1 == 4:
    x1=255
    y1=0
    z1=0
elif co1 ==5:
    x1=255
    y1=204
    z1=0
elif co1 ==6:
    x1=255
    y1=0
    z1=150
elif co1 ==7:
    x1=0
    y1=255
    z1=204
elif co1 ==8:
    x1=204
    y1=0
    z1=255

co2 = int(input('두번째 색을 입력하세요.... '))
if co2 == 1:
    x2=0
    y2=0
    z2=0
elif co2 == 2:
    x2=0
    y2=0
    z2=255
elif co2 == 3:
    x2=0
    y2=255
    z2=255
elif co2 == 4:
    x2=255
    y2=0
    z2=0
elif co2 == 5:
    x2=255
    y2=204
    z2=0
elif co2 == 6:
    x2=255
    y2=0
    z2=105
elif co2 == 7:
    x2=0
    y2=255
    z2=204
elif co2 == 8:
    x2=204
    y2=0
    z2=255

co3 = int(input('세번째 색을 입력하세요.... '))
if co3 == 1:
    x3=0
    y3=0
    z3=0
elif co3 == 2:
    x3=0
    y3=0
    z3=255
elif co3 == 3:
    x3=0
    y3=255
    z3=255
elif co3 == 4:
    x3=255
    y3=0
    z3=0
elif co3 == 5:
    x3=255
    y3=204
    z3=0
elif co3 == 6:
    x3=255
    y3=0
    z3=105
elif co3 == 7:
    x3=0
    y3=255
    z3=204
elif co3 == 8:
    x3=204
    y3=0
    z3=255

co4 = int(input('네번째 색을 입력하세요.... '))
if co4 == 1:
    x4=0
    y4=0
    z4=0
elif co4 == 2:
    x4=0
    y4=0
    z4=255
elif co4 == 3:
    x4=0
    y4=255
    z4=255
elif co4 == 4:
    x4=255
    y4=0
    z4=0
elif co4 == 5:
    x4=255
    y4=204
    z4=0
elif co4 == 6:
    x4=255
    y4=0
    z4=105
elif co4 == 7:
    x4=0
    y4=255
    z4-204
elif co4 == 8:
    x4=204
    y4=0
    z4=255

colors = [(x1,y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4)]
colorIndex = 0

# Setup the Paint interface  -> 화면에 보이는 사격형 입력
paintWindow = np.zeros((471,636,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)
cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Load the video
camera = cv2.VideoCapture(0)

# Keep looping -> 초인트가 화면안에 존재하면 선이 그려짐
while True:
    # Grab the current paintWindow
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Add the coloring options to the frame -> 화면에 표시되는 색상 사각형 생성 코드
    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Color 1", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Color 2", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Color 3", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Color 4", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    # Check to see if we have reached the end of the video -> 화면에 포인트가 나가면 선이 그려지지 않음
    if not grabbed:
        break

    # Determine which pixels fall within the blue boundaries and then blur the binary image
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # Find contours in the image
    (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,                                                 # 오류 부분 -> (_, cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL 코드 실행시 받는값이 3개인데 실제 입력값은 2개여서 오류 발생
    	cv2.CHAIN_APPROX_SIMPLE)                                                                                     # 수정 코드 -> (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL 입력 받는 값을 2개로 바꿔서 오류 수정
    center = None

    # Check to see if any contours were found
    if len(cnts) > 0:
    	# Sort the contours and find the largest one -- we
    	# will assume this contour correspondes to the area of the bottle cap
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Get the moments to calculate the center of the contour (in this case Circle)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear All
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                bindex = 0
                gindex = 0
                rindex = 0
                yindex = 0

                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Green
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
        else :
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

	# If the 'q' key is pressed, stop the loop -> q를 누르면 프로그램 종료 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
