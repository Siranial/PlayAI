from framecapture import FrameCapture
from keycapture import KeyListener
import os
import pygetwindow as gw
import time

class DataRecorder():
    def __init__(self, program_name, session_name):
        # search for the window, getting the first matched window with the title
        self.window = gw.getWindowsWithTitle(program_name)[0]

        # Make new session folder
        new_path = os.path.join(os.getcwd(), session_name)
        # Make sure session saves to unique folder
        i = 0
        self.folder_path = new_path + str(i)
        while os.path.isdir(self.folder_path):
            i+=1
            self.folder_path = new_path + str(i)
        # Make new folder names
        frames_folder_path = os.path.join(self.folder_path, "frames")
        keys_folder_path = os.path.join(self.folder_path, "keys")
        # Make new folders
        os.mkdir(self.folder_path)
        os.mkdir(frames_folder_path)
        os.mkdir(keys_folder_path)
        
        #Print initialization details
        print(r"Saving to " + str(self.folder_path))

        # Construct capturing classes
        self.framecap = FrameCapture(self.window, frames_folder_path)

        # Get keys of interest from the user
        keys = input('Which keys should the logger listen to? Enter up to 10 keys each separated by a comma. For example: w,a,s,d\n')
        #self.keycap = KeyCapture(self.window, keys_folder_path, keys)
        self.keycap = KeyListener(keys_folder_path, keys)
        self.keycap.start_listen()

        # Activate recording window
        self.window.activate()

    def capture(self):
        frame_number = self.framecap.write_frame()
        self.keycap.write_keys(frame_number)


fps = 10.0

recorder = DataRecorder("Discord", "Test")

last_time = time()
time.sleep(1.0 / fps)
current_time = time()

while True:
    # Make sure that the recorder does not operate faster than the fps
    if (current_time - last_time) > (1.0 / fps):
        recorder.capture()