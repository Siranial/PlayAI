import os
import PySimpleGUI as sg
import wexpect as wx

# The layout of the GUI
layout = [
        [sg.Text("Select a game to run")], 
        [sg.Button("Pong"), sg.Button("SpaceInvaders")],
        [sg.Button("Exit")]]

# Create the window
window = sg.Window("PlayAI", layout, margins=(200, 200))

# Create an event loop
while True:
    event, values = window.read()
    #Launch Pong.py if user presses Pong button
    if event == "Pong":
        Pong_Window = wx.spawn("..\Pong_Game\Pong.py")
    # End program if user closes window or
    # presses the Exit button
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
