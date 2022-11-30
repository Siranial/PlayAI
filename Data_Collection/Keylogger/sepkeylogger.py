import os
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import sys
from pynput.keyboard import Key, Listener

#Keylogging
filepath = ''
file_name = ''
keys = []

#Video capture
window_name = ''
frameNum = 0

#Initialize keylog file path
def init_log_var():
    #init globals
    global filepath
    global file_name
    global window_name

    #Poll user where to store keylogs
    print('Please input file location for storing keylogs')
    print('Example: C:/Users/USERNAME/Desktop')
    filepath = input()

    #Ensure filepath exists
    while not os.path.exists(filepath):
            print('Folder not found, please enter existing folder location')
            filepath = input()

    #Check what to call keylog file and set file name
    i = 0
    file_name = '/log0'
    while os.path.exists(filepath + file_name + '.txt'):
        i+=1
        file_name = '/log' + str(i)
    
    print('Please input the name of the window to be recorded')
    window_name = input()

#Detect when a key is pressed
def on_press(key):
    keys.append(key)
    write_file(keys)

#Write keys and framestamps to file
def write_file(keys):
    #init globals
    global filepath
    global file_name
    global frameNum

    with open(filepath + file_name + '.txt', 'w') as f:
        for key in keys:
            # removing '' and writing to file
            f.write(str(key).replace("'", "") + ',' + str(frameNum))
            # add new line
            f.write('\n')

#Detect when a key is released
def on_release(key):
    # Stop keylogger when esc is pressed
    if key == Key.esc:
        # Stop listener
        return False
  

#Initialize variables
init_log_var()

cap = cv2.VideoCapture(0)
# define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# frames per second
fps = 12.0
# search for the window, getting the first matched window with the title
w = gw.getWindowsWithTitle(window_name)[0]
# activate the window
w.activate()
# create the video write object
out = cv2.VideoWriter(filepath + file_name + '.avi', fourcc, fps, tuple(w.size))

#Start recording keys and video
with Listener(on_press = on_press,on_release = on_release) as listener:
    listener.join()

while True:
    # make a screenshot
    img = pyautogui.screenshot(region=(w.left, w.top, w.width, w.height))
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    # convert colors from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # write the frame
    out.write(frame)

    #Read stdin and write all keys from buffer into file with frame number

    frameNum+=1

    if cv2.waitKey(1) & 0xFF == 27:
        break

# make sure everything is closed when exited
cap.release()
out.release()
cv2.destroyAllWindows()