import matplotlib.pyplot as plt
from scipy import fftpack
import numpy as np  
from PIL import Image
import math

def dist(u, v, center):
    cu, cv = center
    return math.sqrt((u - cu) ** 2 + (v - cv) ** 2)

def lowpass(width, height, spec, radius):
    center = (width / 2, height / 2) # Circular Low pass filters => Preserve low frequency component
    for v in range(height):
        for u in range(width):
            if dist(u, v, center) > radius:
                spec[v, u] = 0
    return spec

def highpass(width, height, spec, radius):
    center = (width / 2, height / 2) 
    for v in range(height):
        for u in range(width):
            if dist(u, v, center) < radius:
                spec[v, u] = 0
    return spec

def plot_fourier_spectrum(img_path, filter_type, radius):
    print("Loading Image")
    img = Image.open(img_path)
    
    print("Converting the image to gray")
    img = img.convert('L')
    img_arr = np.array(img)
    
    height, width = img_arr.shape
    print(f"Size of image is: {width, height}")
    
    # Compute the 2-D Fourier Transform
    print("Calculate the fft of the image")
    fft2 = fftpack.fft2(img_arr)
    
    # Shift the zero-frequency component to the center of the spectrum
    print("Shift zero-frequency components to the center")
    fft2_shift = fftpack.fftshift(fft2)
    
    # Apply Filter
    print("Applying Filter")
    if filter_type == 'lowpass':
        filtered_spectrum = lowpass(width, height, fft2_shift, radius)
    elif filter_type == 'highpass':
        filtered_spectrum = highpass(width, height, fft2_shift, radius)
    else:
        raise ValueError("Invalid filter type. Use 'lowpass' or 'highpass'.")
    
    #Plotting:
    print("Plotting Images")
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(np.log(np.abs(fft2)), cmap='gray')
    plt.title('Original Fourier Spectrum')

    plt.subplot(1, 2, 2)
    plt.imshow(np.log(np.abs(filtered_spectrum)), cmap='gray')
    plt.title(f'Filtered Fourier Spectrum ({filter_type} filter with radius {radius})')

    plt.show()
    
def image_enhance_frequency_domain(img_path, filter_type, radius):
    print("Loading Image")
    img = Image.open(img_path)
    
    print("Converting the image to gray")
    img = img.convert('L')
    img_arr = np.array(img)
    
    height, width = img_arr.shape
    print(f"Size of image is: {width, height}")
    
    # Compute the 2-D Fourier Transform
    print("Calculate the fft of the image")
    fft2 = fftpack.fft2(img_arr)
    
    # Shift the zero-frequency component to the center of the spectrum
    print("Shift zero-frequency components to the center")
    fft2_shift = fftpack.fftshift(fft2)
    
    print("Applying Filter")
    # Apply Filter
    if filter_type == 'lowpass':
        filtered_spectrum = lowpass(width, height, fft2_shift, radius)
    elif filter_type == 'highpass':
        filtered_spectrum = highpass(width, height, fft2_shift, radius)
    else:
        raise ValueError("Invalid filter type. Use 'lowpass' or 'highpass'.")
    
    # Inverse Shift the Frequency Spectrum
    print("Inverse shift zero-frequency components")
    fft2_ishift = fftpack.ifftshift(filtered_spectrum)
    
    # Inverse Fourier Transform: Convert it back to spatial domain
    print("Convert back to Spatial Domain")
    img_spatial = fftpack.ifft2(fft2_ishift)
    img_spatial = np.abs(img_spatial)
    
    # Display the original and filtered image
    print("Plotting Images")
    plt.figure(figsize=(12,6))
    plt.subplot(121), plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    
    plt.subplot(122), plt.imshow(img_spatial, cmap='gray')
    plt.title('Filtered Image')
    plt.show()
    
    
    
img_path = 'D:/USTH/ImageProcessing/Data/images2.jpg'
filter_type = 'lowpass'
radius = 40
plot_fourier_spectrum(img_path, filter_type, radius)
image_enhance_frequency_domain(img_path, filter_type, radius)


