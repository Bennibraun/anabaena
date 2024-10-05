import os
from PIL import Image
import numpy as np

# Function to save the mask
def save_mask(mask, method_name, base_filename, mask_dir):
    try:
        # Ensure mask is in uint8 format if it's not already
        if mask.dtype != np.uint8:
            mask = mask.astype(np.uint8)

        # Try converting the array to an image
        mask_img = Image.fromarray(mask)

        # Prepare the mask filename
        mask_filename = f"{base_filename}_{method_name}_mask.png"
        os.makedirs(mask_dir, exist_ok=True)  # Ensure directory exists

        # Save the image
        mask_img.save(os.path.join(mask_dir, mask_filename))

    except TypeError as e:
        print(f"TypeError while converting or saving the mask: {e}")

    except Exception as save_mask_error:
        print(f"Error saving the mask: {save_mask_error}")
