import matplotlib.pyplot as plt
import numpy as np  
from PIL import Image

#Load image
img = Image.open('images.jpg')

#Convert image to grayscale
img = img.convert('L')

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
    lut = [int(val) for val in cdf_normalized]
    
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

img_eq = HistEqualization(img)

#Show original image
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.imshow(img, cmap='gray', interpolation='nearest')
plt.title('Original Image')
plt.axis('off')

#Show equalized image
plt.subplot(2, 2, 2)
plt.imshow(img_eq, cmap='gray', interpolation='nearest')
plt.title('Equalized Image')
plt.axis('off')

#Show histogram of Original Image
hist1 = calHist(img)
plt.subplot(2, 2, 3)
plt.bar(range(256), hist1, color ='gray')
plt.title('Grayscale Histogram of Original image')
plt.xlabel('Pixel value')
plt.ylabel('Frequency')


#Show histogram of Equalized Image
hist2 = calHist(img_eq)
plt.subplot(2, 2, 4)
plt.bar(range(256), hist2, color ='gray')
plt.title('Grayscale Histogram of Equalized image')
plt.xlabel('Pixel value')
plt.ylabel('Frequency')

plt.show()