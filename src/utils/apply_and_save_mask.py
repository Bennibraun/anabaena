import os
import sys
import skimage as sk
from skimage.filters import threshold_local, gaussian
from skimage.morphology import disk, closing
from skimage import feature, exposure, transform
import cv2
import numpy as np

from utils.save_mask import save_mask

# Main function to apply different masking methods
def apply_and_save_masks(image, base_filename, mask_dir):
        # Downsample image for performance if large
    if max(image.shape) > 1000:
        downsample_factor = 2
        image = transform.rescale(image, 1.0 / downsample_factor)
        
    # 1. Otsu Thresholding
    threshold_otsu = sk.filters.threshold_otsu(image)
    mask_otsu = (image > threshold_otsu).astype(np.uint8) * 255
    save_mask(mask_otsu, "otsu", base_filename, mask_dir)

    # 2. Adaptive Thresholding with dynamic block size
    block_size = int(min(image.shape) / 20)  # Dynamic block size
    local_thresh = threshold_local(image, block_size, offset=10)
    mask_adaptive = (image > local_thresh).astype(np.uint8) * 255
    save_mask(mask_adaptive, "adaptive_threshold", base_filename, mask_dir)

    # 3. Otsu with Morphological Closing
    selem = disk(5)
    mask_closing = closing(mask_otsu, selem)
    save_mask(mask_closing, "otsu_closing", base_filename, mask_dir)

    # 4. Sobel Edge Detection
    edges_sobel = sk.filters.sobel(image)
    mask_sobel = (edges_sobel > 0.1).astype(np.uint8) * 255
    save_mask(mask_sobel, "sobel_edges", base_filename, mask_dir)

    # 5. Canny Edge Detection
    canny_edges = feature.canny(image, sigma=2)
    mask_canny = (canny_edges).astype(np.uint8) * 255
    save_mask(mask_canny, "canny_edges", base_filename, mask_dir)

    # 6. Gaussian Smoothing + Otsu
    smoothed_image = gaussian(image, sigma=2)
    threshold_gaussian_otsu = sk.filters.threshold_otsu(smoothed_image)
    mask_gaussian_otsu = (smoothed_image > threshold_gaussian_otsu).astype(np.uint8) * 255
    save_mask(mask_gaussian_otsu, "gaussian_otsu", base_filename, mask_dir)

    # 7. Histogram Equalization + Otsu
    equalized_image = exposure.equalize_hist(image)
    threshold_equalized_otsu = sk.filters.threshold_otsu(equalized_image)
    mask_equalized_otsu = (equalized_image > threshold_equalized_otsu).astype(np.uint8) * 255
    save_mask(mask_equalized_otsu, "equalized_otsu", base_filename, mask_dir)

    # 8. CLAHE + Otsu
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    image_clahe = clahe.apply((image * 255).astype(np.uint8))
    threshold_clahe_otsu = sk.filters.threshold_otsu(image_clahe)
    mask_clahe_otsu = (image_clahe > threshold_clahe_otsu).astype(np.uint8) * 255
    save_mask(mask_clahe_otsu, "clahe_otsu", base_filename, mask_dir)

    # 9. Contour Detection after Otsu with area filtering
    contours, _ = cv2.findContours(mask_otsu, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 100  # Experiment with this value
    filtered_contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]
    mask_filtered_contours = np.zeros_like(mask_otsu)
    cv2.drawContours(mask_filtered_contours, filtered_contours, -1, 255, thickness=cv2.FILLED)
    save_mask(mask_filtered_contours, "filtered_contours_otsu", base_filename, mask_dir)

    # 10. Multi-level Otsu Thresholding
    thresholds_multiotsu = sk.filters.threshold_multiotsu(image, classes=3)  # Experiment with classes
    mask_multiotsu = np.digitize(image, bins=thresholds_multiotsu)
    save_mask(mask_multiotsu, "multiotsu", base_filename, mask_dir)
