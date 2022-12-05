import cv2 as cv
import numpy as np
import os
import time
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
targetBall = Vision('pong_ball.jpg')
targetBar = Vision('pong_bar.jpg')


while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # convert screenshot to np array for opencv
    #frame = np.array(screenshot)
    # convert colors from BGR to RGB
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # find the coordinates where the targets lie
    pointsBall, frameRect = targetBall.find(screenshot, 0.4, 150, 'points')
    pointsBar, frameRect = targetBar.find(frameRect, 0.39, 30, 'rectangle')

    #Get the rightmost recognized bar
    if len(pointsBar) > 0:
        pointRightBar = (0,0)
        for point in pointsBar:
            if point[0] > pointRightBar[0]:
                pointRightBar = point
            

    #Calculate difference between ball and right paddle 
    #coordinates and send bar towards ball y coordinate
    if len(pointsBall):
        if pointRightBar[1] > pointsBall[0][1]:
            moveBar = win32con.VK_UP
        else:
            moveBar = win32con.VK_DOWN
        
        #Move bar
        win32api.PostMessage(wincap.hwnd, win32con.WM_KEYDOWN, moveBar, 0)
        time.sleep(0.5)
        win32api.PostMessage(wincap.hwnd, win32con.WM_KEYUP, moveBar, 0)
        time.sleep(0.5)
        

    #Show the points where ball is recognized
    cv.imshow('Ball matches', frameRect)

    # polls for q press to quit capture
    #if cv.waitKey(1) == ord('q'):
    #    cv.destroyAllWindows()
    #    break


