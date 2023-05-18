import PIL
import os
import pyautogui
import pygetwindow as gw

class FrameCapture():
    # Default constructor
    def __init__(self, window, folder_path):
        self.folder_path = folder_path
        self.window = window

        # Reset frame number
        self.frame_number = 0

    def write_frame(self):
        # Capture frame from the program
        frame = pyautogui.screenshot(region=(self.window.left, self.window.top, self.window.width, self.window.height))

        # Generate a unique filename for the screenshot
        file_name = str(self.frame_number) + ".jpg"

        # Write the screenshot to the file location
        frame.save(os.path.join(self.folder_path, file_name))

        self.frame_number += 1
        # Return the frame number
        return self.frame_number - 1
