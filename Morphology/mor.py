import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def getPixel(image):
    # Load the image and get pixels
    size = image.size
    rgbPixels = list(image.getdata())
    grayPixels = []
    for rgb in rgbPixels:
        gray = int((rgb[0] + rgb[1] + rgb[2])/3) # Find grayscale of the pixel by finding the mean of red, green, blue
        grayPixels.append(gray)
    return grayPixels, size[0], size[1]

def findThreshold(pixels):
    histogram = [0 for _ in range(256)]
    for gray in pixels:
        histogram[gray] += 1 # Find histogram of gray pixels
        
    for intensity in range(256):
        histogram[intensity] /= len(pixels) # Calculate intensity of pixels
    
    cdf = [0 for _ in range(256)]
    for intensity in range(256):
        for i in range(intensity):
            cdf[intensity] += histogram[i] # Calculate cdf for intensity in range(256)
    for intensity in range(256):
        cdf[intensity] *= 255
    threshold = 150
    return threshold

def binary(pixels, width, height, threshold):
    output = []
    for gray in pixels:
        if gray > threshold:
            output.append(255)
        else:
            output.append(0)
    # Initialize a 2D pixels
    binaryPixel2D = [[0 for _ in range(width)] for _ in range(height)]
    
    for i in range(len(output)):
        row = i // width # Determine which row the pixels belongs to
        col = i % width # Determine the column within that row
        binaryPixel2D[row][col] = output[i]
    return binaryPixel2D

def erosion(binaryPixel2D, width, height):
    # Create a White pixels 2D-output
    output = [[255 for _ in range(width)] for _ in range(height)]
    
    # Creating structuring element
    struct = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ])

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            fits = True
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if struct[j + 1][i + 1]== 1 and binaryPixel2D[row + j][col + i] != 0:
                        fits = False
                        break
                if not fits:
                    break
            if fits:
                output[row][col] = 0
    return output

def dilation(binaryPixel2D, width, height):
    # Create a White pixels 2D-output
    output = [[0 for i in range(width)] for j in range(height)]
    
    # Creating structuring element
    struct = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ])
    
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            hit = False
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if struct[j + 1][i + 1] == 1 and binaryPixel2D[row + j][col + 1] != 255:
                        hit = True
            if hit:
                output[row][col] = 0
            else:
                output[row][col] = 255
    return output

          
# Load the image
print("Loading the image")
img = Image.open('E:\\USTH\\Image Processing\\ImageProcessing\\Data\\images2.jpg')          

# Get pixels, width, and height of the image
pixels, width, height = getPixel(img)
print(f"The image size is {width, height}")

# Find the threshold value for binarization
t = findThreshold(pixels)
print(f"Threshold value of the image is: {t}")

# Convert the image to binary using the threshold value
binaryPixel2D = binary(pixels, width, height, t)
# plt.imshow(binaryPixel2D, cmap='gray')
# plt.show()

# Perform erosion on the binary image
# print("Performing erosion")
# output = erosion(binaryPixel2D, width, height)
print("Performing dilation")
output = dilation(binaryPixel2D, width, height)

# Plot the resulting image
plt.imshow(output, cmap='gray')
plt.show()

img.close()