import cv2
import numpy as np
import pyautogui
import time

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1920, 1080))

# Define a function to get the pressed keys
def get_pressed_keys():
    keys = []
    for key_name in ["left", "right", "up", "down", "space"]:
        if pyautogui.keyDown(key_name):
            keys.append(key_name)
    return keys

# Define the main function
def record_game():
    # Wait for 5 seconds before starting
    time.sleep(5)
    while True:
        # Take a screenshot of the screen
        screenshot = pyautogui.screenshot()
        # Convert the screenshot to an array and resize it
        frame = np.array(screenshot)
        frame = cv2.resize(frame, (1920, 1080))
        # Get the pressed keys
        keys = get_pressed_keys()
        # Write the keys on the frame
        text = "Keys: " + " ".join(keys)
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Write the frame to the video
        out.write(frame)
        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Call the main function
record_game()

# Release everything
out.release()
cv2.destroyAllWindows()
