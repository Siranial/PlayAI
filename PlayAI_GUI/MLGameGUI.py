import os, subprocess
import PySimpleGUI as sg
import pexpect as px

# The menu of the GUI
menu_def = ['&File', ['&New File', '&Open...','Open &Module','---', '!&Recent Files','C&lose']],['&Save',['&Save File', 'Save &As','Save &Copy'  ]],['&Edit', ['&Cut', '&Copy', '&Paste']]

# The layout of the GUI
layout = [
        [sg.Menu(menu_def)],
        [sg.Text("Select a game to run")], 
        [sg.Button("Pong"), sg.Button("SpaceInvaders")],
        [sg.Button("Exit")]]

#Gui Theme
sg.theme("Dark Grey 15")

#Gui Theme Preview
#sg.theme_previewer()

# Create the window
window = sg.Window("PlayAI", layout, margins=(200, 200))

# Create an event loop
while True:
    event, values = window.read()
    #Launch Pong.py if user presses Pong button
    if event == "Pong":
        os.system("python Pong_Game/Pong.py")
    
        #Pong_Window = wx.spawn("../Pong_Game/Pong.py")
    # End program if user closes window or
    # presses the Exit button
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
