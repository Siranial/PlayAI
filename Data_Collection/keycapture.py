import os
import pygetwindow as gw
import keyboard
from pynput import keyboard
    

def on_press(key):
    print(key)
    
def on_release(key):
    print(key)

class KeyListener():
    def __init__(self,folder_path,keys):
        self.file_path = os.path.join(folder_path, "keys.txt")

        # Create new CSV file)
        open(self.file_path, 'w')

        # Parse the keys of interest, up to 10
        self.key_list = keys.split(',', 10)

        # Used for tracking the keys pressed during the current frame
        self.keys_pressed = [0] * len(self.key_list)
            

    def on_press(self,key):
        if key == keyboard.Key.esc:
            return False
        for element in self.keys_pressed:
            if self.key_list[element] == key:
                self.keys_pressed[element] = 1
		
    def on_release(self,key):
        for element in self.keys_pressed:
            if self.key_list[element] == key:
                self.keys_pressed[element] = 0
        
    def write_keys(self,frame_number):
        # Generate a new string to write to the CSV
        csv_string = str(frame_number) + ','
        
        # Iterate through the key list
        for key in self.keys_pressed:
            # Write the status of each key
            csv_string += str(key) + ','
        # Remove the unnecessary ',' from the end of the string
        csv_string = csv_string[:-1] + '\n'

        with open(self.file_path, 'a', newline='') as csvfile:
            csvfile.write(csv_string)
            csvfile.close()

    def start_listen(self):
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        listener.join() # wait till listener will stop
        # other stuff 


class KeyCapture():
    #Default constructor
    def __init__(self, window, folder_path, keys):
        self.file_path = os.path.join(folder_path, "keys.txt")
        self.window = window

        # Create new CSV file)
        open(self.file_path, 'w')

        # Parse the keys of interest, up to 10
        self.key_list = keys.split(',', 10)


    # Write the keys of interest which are being read
    def write_keys(self, frame_number):
        # Generate a new string to write to the CSV
        csv_string = str(frame_number) + ','
        
        # Iterate through the key list
        for key in self.key_list:
            # Check if each key is pressed
            if keyboard.is_pressed(key):
                csv_string += '1,'
            else:
                csv_string += '0,'
        # Remove the unnecessary ',' from the end of the string
        csv_string = csv_string[:-1] + '\n'

        with open(self.file_path, 'a', newline='') as csvfile:
            csvfile.write(csv_string)
            csvfile.close()