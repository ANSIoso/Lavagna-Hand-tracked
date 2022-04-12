import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands()

pTime = time.time()

points = []
tollerance = 10

while True:
    succes, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    pollicePos = (1, 2, 3)
    indicePos = (1, 2, 3)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                intensity = int(lm.z * -1000)

                newPoint = (cx, cy, intensity)


                if id == 8:
                    indicePos = newPoint

                    cv2.circle(img, (cx,cy), 15, (255, 0, 255), cv2.FILLED)

                    if newPoint not in points:
                        points.append(newPoint)


                if id == 4:
                    pollicePos = newPoint

                    cv2.circle(img, (cx,cy), 15, (255, 255, 255), cv2.FILLED)


                    for point in points:
                        if (newPoint[0] <= point[0] + tollerance and newPoint[0] >= point[0] - tollerance) and (newPoint[1] <= point[1] + tollerance and newPoint[1] >= point[1] - tollerance):
                            points.remove(point)



            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if (pollicePos[0] <= indicePos[0] + tollerance and pollicePos[0] >= indicePos[0] - tollerance) and (pollicePos[1] <= indicePos[1] + tollerance and pollicePos[1] >= indicePos[1] - tollerance):
        points.clear()

    if len(points) > 0:
        oldPoint = (0,0)
        for point in points:
            cv2.line(img, oldPoint, (point[0],point[1]), (255, 255, 255), 12)
            oldPoint = point[0],point[1]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_ITALIC, 2, (255, 0, 255), 3)
    #print(result.multi_hand_landmarks)

    img = cv2.flip(img, 1)
    cv2.imshow("image", img)
    cv2.waitKey(1)
