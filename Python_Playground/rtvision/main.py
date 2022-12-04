import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
print('Please input the name of the window to be recorded')
window_name = input()
wincap = WindowCapture(window_name)
# initialize the Vision class
#target = Vision('pong_ball.png')

'''
# https://www.crazygames.com/game/guns-and-bottle
#wincap = WindowCapture()
#vision_pong = Vision('pong_ball.png')
'''
target = Vision('pong_ball.jpg')
#Define video codec
fourcc = cv.VideoWriter_fourcc(*"XVID")
# define frames per second
fps = 12.0
# create the video write object
out = cv.VideoWriter('video.avi', fourcc, fps, tuple((wincap.w, wincap.h)))

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # convert screenshot to np array for opencv
    frame = np.array(screenshot)
    # convert colors from BGR to RGB
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # write the frame
    
    points=target.find(screenshot, 0.6, 'rectangles')
    out.write(frame)

    # display the processed image
    #points = target.find(screenshot, 0.5, 'rectangles')
    #points = vision_gunsnbottle.find(screenshot, 0.7, 'points')

    # debug the loop rate
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
