import pygame

#Keylogger class
class Keylogger():
    def __init__(self, filename):
        self.filename = filename

    #update
    def update(self,file):
        key_name = ""
        #Get key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = event.unicode
        #Write to file
        with open(self.filename, "a") as file:
            file.write(key_name + "\n")
    
    #close keylogger
    def close(file):
        file.close()
		