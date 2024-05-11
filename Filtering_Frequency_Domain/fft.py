import matplotlib.pyplot as plt
from scipy import fftpack
import numpy as np  
from PIL import Image
import math as m

#Load image
print("Loading Image")
img = Image.open('E:\\USTH\\Image Processing\\ImageProcessing\\Filtering_Frequency_Domain\\images.jpg')

#Convert image to grayscale
print("Converting the image to gray")
img = img.convert('L')


#Enhance image using Point Processing (Negative Impacts)
def negativeImpact(img):
    width, height = img.size
    img_neq = Image.new('L', (width, height))
    for y in range(height):
        for x in range(width):
            origin = img.getpixel((x, y))
            negative = 255 - origin #Calculate the negative value
            img_neq.putpixel((x, y), negative)
            
    return img_neq
    
#Calculate histogram for grayscale picture
def HistEqualization(img):
    width, height = img.size
    histogram = [0] * 256
    for y in range(height):
        for x in range(width):
            pixel_value = img.getpixel((x,y))
            histogram[pixel_value] += 1
            
    #Calculate CDF
    cdf = [0] * 256
    cdf[0] = histogram[0]
    for i in range(1,256):
        cdf[i] = cdf[i - 1] + histogram[i] #Formula to calculate CDF
    
    #Normalize CDF
    cdf_min = min(cdf)
    total_pixels = width * height
    cdf_normalized = [(cdf[i] - cdf_min) / (total_pixels - cdf_min) * 255 for i in range(256)]
    
    #Look up table to match old pixel value to new pixel value
    lut = [int(val) for val in cdf_normalized] #Rounding step
    
    #Create new image
    img_eq = Image.new('L', (width, height))
    for y in range(height):
        for x in range(width):
            img_eq.putpixel((x, y), lut[img.getpixel((x, y))])
            
    return img_eq

def calHist(img):
    width, height = img.size
    histogram = [0] * 256
    for y in range(height):
        for x in range(width):
            pixel_value = img.getpixel((x, y))
            histogram[pixel_value] += 1
    
    return histogram


def dist(u, v, center):
    return m.sqrt((u + center[0]/2) ** 2 + (v - center[1]/2) **2)

def lowpass(spec, radius):
    width, height = img.size
    center = (width / 2, height / 2)
    for v in range(height):
        for u in range(width):
            if dist(u, v, center) > radius:
                spec[v, u] = 0
    return spec

def highpass(spec, radius):
    width, height = img.size
    center = (width / 2, height / 2)
    for v in range(height):
        for u in range(width):
            if dist(u, v, center)  < radius:
                spec[u, v] = 0
    return spec
                
            
# Compute the 2-D Fourier Transform
print("Calculate the fft of the image")
fft2 = fftpack.fft2(img)

# Shift the zero frequency component to the center of the spectrum => Make it a Low frequency Area
fft2_shift = fftpack.fftshift(fft2)

# Compute the magnitude spectrum
magnitude_spectrum = np.abs(fft2_shift)
# print(magnitude_spectrum)
magnitude_spectrum1 = lowpass(magnitude_spectrum, 20)

# log to scale down the range of spectrum value, +1 to avoid 0 case => Make it more visible and detail
plt.imshow(np.log(magnitude_spectrum1 + 1), cmap = 'gray')
plt.title('Magnitude Spectrum')
#plt.colorbar()
plt.show()