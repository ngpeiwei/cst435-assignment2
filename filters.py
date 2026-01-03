import numpy as np

def grayscale_conversion(img_array):
    """Convert RGB to grayscale using luminance formula"""
    return np.dot(img_array[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)

def apply_kernel(img_array, kernel):
    """Basic 2D convolution for filters"""
    img_h, img_w = img_array.shape[:2]
    kh, kw = kernel.shape
    pad = kh // 2
    
    # Pad the image to handle borders
    if len(img_array.shape) == 3: # RGB
        padded_img = np.pad(img_array, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        output = np.zeros_like(img_array)
        for c in range(3):
            for i in range(img_h):
                for j in range(img_w):
                    region = padded_img[i:i+kh, j:j+kw, c]
                    output[i, j, c] = np.clip(np.sum(region * kernel), 0, 255)
    else: # Grayscale
        padded_img = np.pad(img_array, pad, mode='edge')
        output = np.zeros_like(img_array)
        for i in range(img_h):
            for j in range(img_w):
                region = padded_img[i:i+kh, j:j+kw]
                output[i, j] = np.clip(np.sum(region * kernel), 0, 255)
    return output.astype(np.uint8)

def gaussian_blur(img_array):
    kernel = np.array([[1, 2, 1], 
                       [2, 4, 2], 
                       [1, 2, 1]]) / 16.0
    return apply_kernel(img_array, kernel)

def sobel_edge_detection(img_array):
    # Ensure grayscale for edge detection
    if len(img_array.shape) == 3:
        gray = grayscale_conversion(img_array)
    else:
        gray = img_array
        
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    
    gx = apply_kernel(gray, Kx)
    gy = apply_kernel(gray, Ky)
    
    magnitude = np.sqrt(gx.astype(float)**2 + gy.astype(float)**2)
    return np.clip(magnitude, 0, 255).astype(np.uint8)

def image_sharpening(img_array):
    kernel = np.array([[0, -1, 0], 
                       [-1, 5, -1], 
                       [0, -1, 0]])
    return apply_kernel(img_array, kernel)

def brightness_adjustment(img_array, factor=1.2):
    return np.clip(img_array * factor, 0, 255).astype(np.uint8)