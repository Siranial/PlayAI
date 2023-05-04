import cv2
import numpy as np
import os
import argparse

def create_circular_mask(h, w, center=None, radius=None):

    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

def distance_matrix(rows,cols):
    crow,ccol = rows//2, cols//2

    x = np.argwhere(np.ones((rows,cols))).reshape((rows,cols,2))
    y = np.array((crow,ccol))

    #Euclidian distance formula
    x -= y
    x = np.square(x)
    z = np.sum(x[:][:], axis=2)
    z = np.sqrt(z)

    return z

def butterworth_lowpass(img, n, D):
    #Take fourier transform
    fshift = np.fft.fftshift(np.fft.fft2(img))

    rows, cols = img.shape

    distance = distance_matrix(rows,cols) + 0.0001

    butterworth_scale = 1 / (1 + (distance / D)**(2*n))

    fshift = np.multiply(fshift, butterworth_scale)

    #Convert back to image pixel format
    img_back = np.real(np.fft.ifft2(np.fft.ifftshift(fshift)))

    return img_back


#Get the location of the folder from the arguments list
parser = argparse.ArgumentParser(prog='Preprocessor')
parser.add_argument('folderpath')
[parser.add_argument('endpath')]
args = parser.parse_args()

#Ensure folder exists and raise error if not
assert os.path.exists(args.folderpath), "Error: Could not locate folder"

#Make new directory to save processed images
processed_path = args.endpath
new_processed_path = processed_path
i = 0
while os.path.exists(new_processed_path):
    new_processed_path = processed_path + str(i)
    i+=1
os.mkdir(new_processed_path)

for filename in os.listdir(args.folderpath):
    if not filename.endswith(".jpg"):
        continue

    #Read custom image
    img = cv2.imread(os.path.join(args.folderpath,filename))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    #Process the image
    img[img < 78] = 0
    img = butterworth_lowpass(img,2,50)
    img[img < 10] = 0
    img[img >= 10] = 255


    #Save the image
    cv2.imwrite(os.path.join(new_processed_path,filename), img)



