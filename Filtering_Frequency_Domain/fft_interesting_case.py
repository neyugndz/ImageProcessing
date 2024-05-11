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

def highpass_lowpass_fourier(img_path, highpass_radius, lowpass_radius):
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
    
    # Apply High-pass Filter
    print("Applying High-pass Filter")
    highpass_spectrum = highpass(width, height, fft2_shift, highpass_radius)
    
    # Apply Low-pass Filter to the high-pass filtered spectrum
    print("Applying Low-pass Filter to the high-pass filtered spectrum")
    lowpass_spectrum = lowpass(width, height, highpass_spectrum, lowpass_radius)
    
    # Inverse Shift the Frequency Spectrum
    print("Inverse shift zero-frequency components")
    fft2_ishift = fftpack.ifftshift(lowpass_spectrum)
    
    # Inverse Fourier Transform: Convert it back to spatial domain
    print("Convert back to Spatial Domain")
    img_spatial = fftpack.ifft2(fft2_ishift)
    img_spatial = np.abs(img_spatial)
    
    # Display the original and filtered image
    print("Plotting Images")
    plt.figure(figsize=(12,6))
    plt.subplot(121), plt.imshow(np.log(np.abs(fft2)), cmap='gray')
    plt.title('Original Fourier Spectrum')
    
    plt.subplot(122), plt.imshow(np.log(np.abs(lowpass_spectrum)), cmap='gray')
    plt.title('Filtered Fourier Spectrum (High-pass then Low-pass)')
    plt.show()

def highpass_lowpass(img_path, highpass_radius, lowpass_radius):
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
    
    # Apply High-pass Filter
    print("Applying High-pass Filter")
    highpass_spectrum = highpass(width, height, fft2_shift, highpass_radius)
    
    # Apply Low-pass Filter to the high-pass filtered spectrum
    print("Applying Low-pass Filter to the high-pass filtered spectrum")
    lowpass_spectrum = lowpass(width, height, highpass_spectrum, lowpass_radius)
    
    # Inverse Shift the Frequency Spectrum
    print("Inverse shift zero-frequency components")
    fft2_ishift = fftpack.ifftshift(lowpass_spectrum)
    
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
    plt.title('Filtered Image (High-pass then Low-pass)')
    plt.show()




img_path = 'D:/USTH/ImageProcessing/Data/images2.jpg'
highpass_radius = 40
lowpass_radius = 100
#highpass_lowpass_fourier(img_path, highpass_radius, lowpass_radius)
highpass_lowpass(img_path, highpass_radius, lowpass_radius)

    
    


