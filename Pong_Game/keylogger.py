import pygame

#Keylogger class
class Keylogger():
    def __init__(self, filename):
        self.filename = filename

    #update
    def update(self,file,key_name):
        #Write to file
        with open(self.filename, "a") as file:
            file.write(key_name + "\n")
            file.close()
		