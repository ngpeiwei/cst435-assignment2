import numpy as np

# Filter 1: Convert RGB images to grayscale using luminance formula
def grayscale_conversion(img_array):
    gray = np.dot(img_array[..., :3], [0.299, 0.587, 0.114])
    
    return np.clip(gray, 0, 255).astype(np.uint8)

# Core convolution operation: Perform convolution on 2D (grayscale) or 3D (RGB) images
def _convolve(img_array, kernel, clip=True):
    """
    Apply a convolution kernel to an image.
    clip=True  → output limited to 0–255 (normal image)
    clip=False → keep float values (for edge detection)
    """
    h, w = img_array.shape[:2]
    kh, kw = kernel.shape
    pad = kh // 2

    # Multi-channel image
    if img_array.ndim == 3:  
        padded = np.pad(img_array, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        output = np.zeros((h, w, img_array.shape[2]), dtype=float)
        for i in range(kh):
            for j in range(kw):
                output += padded[i:i+h, j:j+w, :] * kernel[i, j]
    else:  # Grayscale 2D
        padded = np.pad(img_array, ((pad, pad), (pad, pad)), mode='edge')
        output = np.zeros((h, w), dtype=float)
        for i in range(kh):
            for j in range(kw):
                output += padded[i:i+h, j:j+w] * kernel[i, j]

    if clip:
        return np.clip(output, 0, 255).astype(np.uint8)
    else:
        # Return float result
        return output  

# Wrapper: apply kernel with optional float output
def apply_kernel(img_array, kernel, preserve_dtype=False):
    return _convolve(img_array, kernel, clip=not preserve_dtype)

# Filter 2: Apply 3×3 Gaussian kernel for smoothing
def gaussian_blur(img_array):
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]], dtype=float) / 16.0
    return apply_kernel(img_array, kernel)

# Filter 3: Sobel filter to detect edges
def sobel_edge_detection(img_array):
    if img_array.ndim == 3:
        gray = grayscale_conversion(img_array)
    else:
        gray = img_array

    Kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], dtype=float)
    Ky = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]], dtype=float)

    gx = apply_kernel(gray, Kx, preserve_dtype=True).astype(float)
    gy = apply_kernel(gray, Ky, preserve_dtype=True).astype(float)

    magnitude = np.sqrt(gx**2 + gy**2)
    return np.clip(magnitude, 0, 255).astype(np.uint8)

# Filter 4: Sharpen image to enhance details
def image_sharpening(img_array):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=float)
    return apply_kernel(img_array, kernel)

# Filter 5: Adjust image brightness
def brightness_adjustment(img_array, factor=1.2):
    return np.clip(img_array.astype(float) * factor, 0, 255).astype(np.uint8)




