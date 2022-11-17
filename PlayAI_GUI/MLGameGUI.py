import os, subprocess
import PySimpleGUI as sg
import pexpect as px


# The layout of the GUI
layout = [
        [sg.Text("Select a game to run")], 
        [sg.Button("Pong"), sg.Button("SpaceInvaders")],
        [sg.Button("Exit")]]
sg.theme("Dark Grey 15")
# Create the window
window = sg.Window("PlayAI", layout, margins=(200, 200))
sg.theme_previewer()
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
