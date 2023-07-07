import cv2 as cv
import numpy as np
import os
import win32con, win32api
from windowcapture import WindowCapture
from vision import Vision

def distance_matrix(rows,cols):
    crow,ccol = rows//2, cols//2

    x = np.argwhere(np.ones((rows,cols))).reshape((rows,cols,2))
    y = np.array((crow,ccol))

    #Euclidian distance formula
    x -= y
    x = np.square(x)
    z = np.sum(x[:][:], axis=2)
    z = np.sqrt(z)

    return z

def butterworth_lowpass(img, n, D):
    #Take fourier transform
    fshift = np.fft.fftshift(np.fft.fft2(img))

    rows, cols = img.shape

    distance = distance_matrix(rows,cols) + 0.0001

    butterworth_scale = 1 / (1 + (distance / D)**(2*n))

    fshift = np.multiply(fshift, butterworth_scale)

    #Convert back to image pixel format
    img_back = np.real(np.fft.ifft2(np.fft.ifftshift(fshift)))

    return img_back


#Change working directory to folder this script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
print('Please input the name of the window to be recorded')
window_name = input()
wincap = WindowCapture(window_name)

# initialize the Vision classes
targetPlayer = Vision('si_player.JPG', color=(0,0,255))
targetBottomEnemy = Vision('si_enemy0.JPG', color=(255,0,0))
targetMiddleEnemy = Vision('si_enemy1.JPG', color=(255,0,0))
targetTopEnemy = Vision('si_enemy2.JPG', color=(255,0,0))
targetCBullet = Vision('si_bullet1.JPG', color=(0,255,0))
targetLBullet= Vision('si_bullet2.JPG',color=(0,255,0))
# initialize global variables
prevPointBall = (0,0)
predPointBall = 0
ballVelocity = 0
moveBar = win32con.VK_LEFT


while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    #Process the image
    #screenshotGray = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
    #screenshotGray[screenshotGray < 78] = 0
    #screenshotGray = butterworth_lowpass(screenshotGray,2,50)
    #screenshotGray[screenshotGray < 10] = 0
    #screenshotGray[screenshotGray >= 10] = 255
    #screenshot = cv.merge((screenshotGray, screenshotGray, screenshotGray))

    # find the coordinates where the targets lie
    pointsPlayer, frameRect = targetPlayer.find(screenshot, 0.6, 30, 'points')
    pointsBEnemy, frameRect = targetBottomEnemy.find(frameRect, 0.65, 30, 'points')
    pointsMEnemy, frameRect = targetMiddleEnemy.find(frameRect, 0.6, 30, 'points')
    pointsTEnemy, frameRect = targetTopEnemy.find(frameRect, 0.6, 30, 'points')
    pointsCBullet, frameRect = targetCBullet.find(frameRect, 0.6, 30, 'points')
    pointsLBullet, frameRect = targetLBullet.find(frameRect, 0.6, 30, 'points')
    #Get the rightmost recognized bar
    #if len(pointsBar) > 0:
        #pointRightBar = (0,0)
        #for point in pointsBar:
            #if point[0] > pointRightBar[0]:
                #pointRightBar = point

    #Find the ball coordinates if recognized
    #if len(pointsBall):
        #Calculate ball path
        #ballVector = tuple(map(lambda i,j:i-j, pointsBall[0], prevPointBall))
        #prevPointBall = pointsBall[0]


        #Predict where to move the bar based on ball velocity
        #Calculate time before ball hits bar
        #if ballVector[0] > 0:
            #Normalize the ball velocity
           # ballVelocity = np.sqrt(ballVector[0] * ballVector[0] + ballVector[1] * ballVector[1])
           # ballVector = (ballVector[0] / ballVelocity, ballVector[1] / ballVelocity)

           # airTime = (pointRightBar[0] - pointsBall[0][0]) / ballVector[0]
            #Predict vertical location of ball for paddle hit
            #predPointBall = (pointsBall[0][1] + ballVector[1] * airTime)
           # while predPointBall > 500 or predPointBall < 0:
              #  if predPointBall > 500:
               #     predPointBall = 1000 - predPointBall
              #  else:
               #     predPointBall = -predPointBall

            #Calculate where the bar needs to move to meet the predicted point
           # if pointRightBar[1] - predPointBall > 25:
            #    moveBar = win32con.VK_UP
           # elif pointRightBar[1] - predPointBall < -25:
             #   moveBar = win32con.VK_DOWN
        #Case where ball is moving to the left
       # else:
        #   if pointRightBar[1] - 250 > 0:
       #        moveBar = win32con.VK_UP
        #    elif pointRightBar[1] - 250 < 0:
       #         moveBar = win32con.VK_DOWN


    #Move bar
    #win32api.PostMessage(wincap.hwnd, win32con.WM_KEYDOWN, moveBar, 0)

    #Show the points where ball is recognized
    imS = cv.resize(frameRect, (wincap.w//2, wincap.h//2))
    cv.imshow('space invaders', imS)

    # polls for q press to quit capture
    if cv.waitKey(100) == ord('q'):
        cv.destroyAllWindows()
        break

    #Relase bar moving key
    #win32api.PostMessage(wincap.hwnd, win32con.WM_KEYUP, moveBar, 0)
    #Reset movement for next loop
    #moveBar = win32con.VK_LEFT