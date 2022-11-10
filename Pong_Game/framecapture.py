import cv2

# Opens the Video file
cap= cv2.VideoCapture('/Users/ajay/Downloads/2022-11-05_17-59-58.mp4') #path to video you want to frame capture
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('/Users/ajay/Documents/frame'+str(i)+'.jpg',frame) #path then name
    i+=1

cap.release()
cv2.destroyAllWindows()