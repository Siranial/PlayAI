import os
import pygetwindow as gw
import keyboard

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
		
