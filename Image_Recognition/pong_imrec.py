import cv2 as cv
import numpy as np
import os
from windowcapture import WindowCapture
from vision import Vision

#Change working directory to folder this script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
print('Please input the name of the window to be recorded')
window_name = input()
wincap = WindowCapture(window_name)

# initialize the Vision classes
targetBall = Vision('pong_ball.jpg',cv.TM_CCOEFF_NORMED)
#targetBar = Vision('pong_bar.jpg')


while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # convert screenshot to np array for opencv
    frame = np.array(screenshot)
    # convert colors from BGR to RGB
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # find the coordinates where the targets lie
    pointsBall = targetBall.find(screenshot, 0.4, 'points')
    #pointsBar = targetBar.find(screenshot, 0.49, 'rectangles')

    #COMBINE POINTSBALL AND BAR HERE TO MAKE THE IMAGE AND PRINT IT
    #need to edit vision.py to return the points only


    #Show the points where ball is recognized
    #cv.imshow('Ball matches', pointsBall)

    # polls for q press to quit capture
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


