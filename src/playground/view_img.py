import cv2
import numpy as np
import os

# Load your images
img1 = cv2.imread('/Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground/20241010_001_ZMB_frame_0000_mono.png')
img2 = cv2.imread('/Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground/20241010_001_ZMB_frame_0001_mono.png')

# Resize images if they are of different sizes
# For example, resize both to the same height
height = min(img1.shape[0], img2.shape[0])
img1 = cv2.resize(img1, (int(img1.shape[1] * height / img1.shape[0]), height))
img2 = cv2.resize(img2, (int(img2.shape[1] * height / img2.shape[0]), height))

# Ensure both images have the same shape for overlaying
if img1.shape != img2.shape:
    raise ValueError("Images must have the same dimensions for overlaying.")

# Overlay the images using addWeighted
alpha = 0.5  # Weight for the first image
beta = 0.5   # Weight for the second image
overlayed_img = cv2.addWeighted(img1, alpha, img2, beta, 0)

# Define the output file path
output_directory = '/Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground/'
output_filename = 'overlayed_image.png'  # or any desired filename
output_path = os.path.join(output_directory, output_filename)

# Save the overlayed image
cv2.imwrite(output_path, overlayed_img)

print(f"Overlayed image saved at: {output_path}")
