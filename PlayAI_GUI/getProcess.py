#import tkinter as tk
#from tkinter import ttk
#import tkinter.font as font
#import winsound, pickle
import psutil as ps

#Wait for user to input game name
print("Please enter name of game")
p_name = input()

#Find process with game name
for p in ps.process_iter():
    if p_name in p.name():
        break

print(p.name())
print(p.ppid())