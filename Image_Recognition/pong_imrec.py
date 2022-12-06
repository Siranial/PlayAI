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
targetBall = Vision('pong_ball2.jpg')
targetBar = Vision('pong_bar2.jpg')

# initialize global variables
prevPointBall = (0,0)
predPointBall = 0
ballVelocity = 0
moveBar = win32con.VK_LEFT


while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # convert screenshot to np array for opencv
    #frame = np.array(screenshot)
    # convert colors from BGR to RGB
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # find the coordinates where the targets lie
    pointsBall, frameRect = targetBall.find(screenshot, 0.9, 1, 'points')
    pointsBar, frameRect = targetBar.find(frameRect, 0.9, 1, 'points')
    
    #Get the rightmost recognized bar
    if len(pointsBar) > 0:
        pointRightBar = (0,0)
        for point in pointsBar:
            if point[0] > pointRightBar[0]:
                pointRightBar = point
    
    #Find the ball coordinates if recognized
    if len(pointsBall):
        #Calculate ball path
        ballVelocity = tuple(map(lambda i,j:i-j, pointsBall[0], prevPointBall))
        prevPointBall = pointsBall[0]


        #Predict where to move the bar based on ball velocity
        #Calculate time before ball hits bar
        if ballVelocity[0] > 0:
            #Normalize the ball velocity
            velocity = np.sqrt(ballVelocity[0] * ballVelocity[0] + ballVelocity[1] * ballVelocity[1])
            ballVelocity = (ballVelocity[0] / velocity, ballVelocity[1] / velocity)

            airTime = (pointRightBar[0] - pointsBall[0][0]) / ballVelocity[0]
            #Predict vertical location of ball for paddle hit
            predPointBall = (pointsBall[0][1] + ballVelocity[1] * airTime)
            while predPointBall > 700 or predPointBall < 0:
                if predPointBall > 700:
                    predPointBall = 1400 - predPointBall
                else:
                    predPointBall = -predPointBall
        
        #Calculate where the bar needs to move to meet the predicted point
        if pointRightBar[1] - predPointBall > 20:
            moveBar = win32con.VK_UP
        elif pointRightBar[1] - predPointBall < -20:
            moveBar = win32con.VK_DOWN
        else:
            #bar stays still
            moveBar = win32con.VK_LEFT


        print(ballVelocity, predPointBall, airTime)


    #Move bar
    win32api.PostMessage(wincap.hwnd, win32con.WM_KEYDOWN, moveBar, 0)


    #Show the points where ball is recognized
    cv.imshow('Ball matches', frameRect)

    # polls for q press to quit capture
    if cv.waitKey(100) == ord('q'):
        cv.destroyAllWindows()
        break
    
    #Relase key
    win32api.PostMessage(wincap.hwnd, win32con.WM_KEYUP, moveBar, 0)
    #Reset movement for next loop
    moveBar = win32con.VK_LEFT

    


