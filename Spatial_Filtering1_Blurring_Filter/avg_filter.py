import matplotlib.pyplot as plt
import numpy as np  
from PIL import Image

#Load image
img = Image.open('images.jpg')

#Convert image to grayscale
img = img.convert('L')


#Filter Image using Average method
def average_filter(img):
    width, height = img.size
    pixels = img.load()
    #Convert image to gray
    filtered_img = Image.new('L', (width, height))
    filtered_pixels = filtered_img.load()

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            total = 0
            #Sum up all neighboring pixels
            for i in range(-1,2):
                for j in range(-1,2):
                    total += pixels[x+i, y+j] #x-1, x, x+1
                #Calculating the average
                filtered_pixels[x, y] = total // 9 # // is floor division
                
    return filtered_img
            
    
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

#Show original image
plt.figure(figsize=(18, 6))
plt.subplot(2, 3, 1)
plt.imshow(img, cmap='gray', interpolation='nearest') #cmap = Colormap Instance/  Registered Colormap Name
plt.title('Original Image')
plt.axis('off')

#Show equalized image
img_eq = HistEqualization(img)
plt.subplot(2, 3, 2)
plt.imshow(img_eq, cmap='gray', interpolation='nearest')
plt.title('Equalized Image')
plt.axis('off')

#Show negative image
img_filtered = average_filter(img)
plt.subplot(2, 3, 3)
plt.imshow(img_filtered, cmap='gray', interpolation='nearest')
plt.title('Average Filtered Image')
plt.axis('off')


#Show histogram of Original Image
hist1 = calHist(img)
plt.subplot(2, 3, 4)
plt.bar(range(256), hist1, color ='gray')
plt.title('Grayscale Histogram of Original Image')
plt.xlabel('Pixel value')
plt.ylabel('Frequency')


#Show histogram of Original Image
hist2 = calHist(img_eq)
plt.subplot(2, 3, 5)
plt.bar(range(256), hist2, color ='gray')
plt.title('Grayscale Histogram of Equalized Image')
plt.xlabel('Pixel value')
plt.ylabel('Frequency')

#Show histogram of Negative Image
hist3 = calHist(img_filtered)
plt.subplot(2, 3, 6)
plt.bar(range(256), hist3, color = 'gray')
plt.title('Grayscale Histogram of Average Filtered Image')
plt.xlabel('Pixel value')
plt.ylabel('Frequency')

plt.show()