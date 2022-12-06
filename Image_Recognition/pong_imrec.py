import cv2 as cv
import numpy as np
import os
import win32con, win32api
from windowcapture import WindowCapture
from vision import Vision

#Change working directory to folder this script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
print('Please input the name of the window to be recorded')
window_name = input()
wincap = WindowCapture(window_name)

# initialize the Vision classes
targetBall = Vision('pong_ball2.jpg', color=(255,0,255))
targetBar = Vision('pong_bar2.jpg', color=(255,255,0))

# initialize global variables
prevPointBall = (0,0)
predPointBall = 0
ballVelocity = 0
moveBar = win32con.VK_LEFT


while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # find the coordinates where the targets lie
    pointsBall, frameRect = targetBall.find(screenshot, 0.9, 1, 'points')
    pointsBar, frameRect = targetBar.find(frameRect, 0.8, 1, 'points')
    
    #Get the rightmost recognized bar
    if len(pointsBar) > 0:
        pointRightBar = (0,0)
        for point in pointsBar:
            if point[0] > pointRightBar[0]:
                pointRightBar = point
    
    #Find the ball coordinates if recognized
    if len(pointsBall):
        #Calculate ball path
        ballVector = tuple(map(lambda i,j:i-j, pointsBall[0], prevPointBall))
        prevPointBall = pointsBall[0]


        #Predict where to move the bar based on ball velocity
        #Calculate time before ball hits bar
        if ballVector[0] > 0:
            #Normalize the ball velocity
            ballVelocity = np.sqrt(ballVector[0] * ballVector[0] + ballVector[1] * ballVector[1])
            ballVector = (ballVector[0] / ballVelocity, ballVector[1] / ballVelocity)

            airTime = (pointRightBar[0] - pointsBall[0][0]) / ballVector[0]
            #Predict vertical location of ball for paddle hit
            predPointBall = (pointsBall[0][1] + ballVector[1] * airTime)
            while predPointBall > 500 or predPointBall < 0:
                if predPointBall > 500:
                    predPointBall = 1000 - predPointBall
                else:
                    predPointBall = -predPointBall
        
        #Calculate where the bar needs to move to meet the predicted point
        if pointRightBar[1] - predPointBall > 35:
            moveBar = win32con.VK_UP
        elif pointRightBar[1] - predPointBall < -35:
            moveBar = win32con.VK_DOWN


    #Move bar
    win32api.PostMessage(wincap.hwnd, win32con.WM_KEYDOWN, moveBar, 0)

    #Show the points where ball is recognized
    cv.imshow('Ball matches', frameRect)

    # polls for q press to quit capture
    if cv.waitKey(100) == ord('q'):
        cv.destroyAllWindows()
        break
    
    #Relase bar moving key
    win32api.PostMessage(wincap.hwnd, win32con.WM_KEYUP, moveBar, 0)
    #Reset movement for next loop
    moveBar = win32con.VK_LEFT

    


