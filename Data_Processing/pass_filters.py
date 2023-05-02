import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec as gridspec

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

def circular_low_pass(img,radius):
    #Take fourier transform
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    
    #Create the circular mask to filter the image
    rows, cols = img.shape
    mask = create_circular_mask(rows,cols,radius=radius)

    #Apply mask to get lowpass
    filtered = np.multiply(fshift,mask)

    #Convert back to image pixel format
    f_ishift = np.fft.ifftshift(filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.real(img_back)

    return img_back

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

def butterworth_highpass(img, n, D):
    #Take fourier transform
    fshift = np.fft.fftshift(np.fft.fft2(img))

    rows, cols = img.shape

    distance = distance_matrix(rows,cols) + 0.0001 #prevent division by zero

    butterworth_scale = 1 / (1 + (D / distance)**(2*n))

    fshift = np.multiply(fshift, butterworth_scale)

    #Convert back to image pixel format
    img_back = np.real(np.fft.ifft2(np.fft.ifftshift(fshift)))

    return img_back



#Read custom image
img1 = cv2.cvtColor(cv2.imread('img1.jpg',cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2GRAY)
img2 = cv2.cvtColor(cv2.imread('img2.jpg',cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2GRAY)
img3 = cv2.cvtColor(cv2.imread('img3.jpg',cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2GRAY)
img4 = cv2.cvtColor(cv2.imread('img4.jpg',cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2GRAY)
img5 = cv2.cvtColor(cv2.imread('img5.jpg',cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2GRAY)

img1_sharp = np.copy(img1)
img1_sharp[img1_sharp < 78] = 0
img1_blobs = butterworth_lowpass(img1_sharp,2,20)
img1_blobs[img1_blobs > 10] = 255

plt.subplot(131),plt.imshow(img1, cmap = 'gray')
plt.title('img1 original'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(img1_sharp, cmap = 'gray')
plt.title('img1 sharp'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(img1_blobs, cmap = 'gray')
plt.title('img1 blobs'), plt.xticks([]), plt.yticks([])
plt.show()

exit()

img2_low = butterworth_lowpass(img2,2,30)
plt.subplot(121),plt.imshow(img2, cmap = 'gray')
plt.title('img2 original'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img2_low, cmap = 'gray')
plt.title('img2 low'), plt.xticks([]), plt.yticks([])
plt.show()


img3_low = butterworth_lowpass(img3,2,30)



img4_low = butterworth_lowpass(img4,2,30)



img5_low = butterworth_lowpass(img5,2,30)







