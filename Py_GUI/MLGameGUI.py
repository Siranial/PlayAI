import PySimpleGUI as sg

layout = [[sg.Text("Select a game to run")], [sg.Button("Pong"), sg.Button("SpaceInvaders")], [sg.Button("Exit")]]

# Create the window
window = sg.Window("PlayAI", layout, margins=(200, 200))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
