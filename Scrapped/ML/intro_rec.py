import cv2 as cv
import numpy as np
import os


# Change CWD to folder where script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# read canvas and target images
canvas = cv.imread('pong_img1.png', cv.IMREAD_UNCHANGED)
target = cv.imread('pong_ball.png', cv.IMREAD_UNCHANGED)

# There are 6 comparison methods to choose from:
# TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
# You can see the differences at a glance here:
# https://docs.opencv.org/master/d4/dc6/tutorial_py_template_matching.html
# Note that the values are inverted for TM_SQDIFF and TM_SQDIFF_NORMED
result = cv.matchTemplate(canvas, target, cv.TM_SQDIFF_NORMED)

# I've inverted the threshold and where comparison to work with TM_SQDIFF_NORMED
threshold = 0.17
# The np.where() return value will look like this:
# (array([482, 483, 483, 483, 484], dtype=int32), array([514, 513, 514, 515, 514], dtype=int32))
locations = np.where(result <= threshold)
# We can zip those up into a list of (x, y) position tuples
locations = list(zip(*locations[::-1]))
print(locations)

if locations:
    print('Found needle.')

    needle_w = target.shape[1]
    needle_h = target.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for loc in locations:
        # Determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        # Draw the box
        cv.rectangle(canvas, top_left, bottom_right, line_color, line_type)

    cv.imshow('Matches', canvas)
    cv.waitKey()
    #cv.imwrite('result.jpg', haystack_img)

else:
    print('Needle not found.')