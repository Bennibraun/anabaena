import argparse
import sys
import os 
import numpy as np
from PIL import Image  # Ensure you have Pillow installed for TIFF handling
from tqdm import tqdm


# Dynamically add the 'src' directory to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..')  # Go one level up to 'src'
sys.path.append(src_path)  # Add the src directory to sys.path

from file_formatting.standardize_file_types import ImageHandler  
from utils.apply_and_save_mask import apply_and_save_masks

def step_1():
    # Step 1, arg parser
    parser = argparse.ArgumentParser(description="Annotate images and save annotations.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input image file.")
    parser.add_argument("--output_file", type=str, required=False, help="Path to save the annotations.")
    parser.add_argument('--figure_type', type= str, required=False, help = 'specify the figure format when saving the figure')
    parser.add_argument('--mask_dir', type=str, required=False, help= 'directory to the masks / ground truths')
    parser.add_argument('--skip', action='store_true', help='Skip watersheding and mask generation for some files')
    args = parser.parse_args()
    return args

def step_2(args):
    # Step 2. reformat the nd2 files into png or pdf files

    ## check if input file is nd2
    if os.path.splitext(args.input_file)[1].lower() == '.nd2':
        image_handler = ImageHandler(args.input_file)
        img = image_handler.read_image()
        image_handler.save_image(args.output_file, args.figure_type)

def step_3(args, file_index:int = 0):
    # Step 3: Generate masks for the PNG files
    png_files = []
    
    # Loop through all files in the output directory
    for filename in os.listdir(args.output_file):
        if filename.lower().endswith('.png'):  # Check for .png extension
            png_files.append(os.path.join(args.output_file, filename))  # Add full file path to the list

    if not png_files:
        return  # No PNG files found, exit the function

    # runs masking for all the png files
    if not args.skip:
        # tqdm progress bar wrapping the png_files loop
        for png_file in tqdm(png_files, desc="Generating masks", unit="file"):
            
            # Use the ImageHandler class to read the image
            image_handler = ImageHandler(png_file)
            image = image_handler.read_image()

            # Apply threshold to create a mask
            threshold = 150  # Adjust threshold as needed
            mask = (image > threshold).astype(np.uint8) * 255  # Binary mask (0 or 255)
            mask_img = Image.fromarray(mask)

            # Use os.path.splitext() to separate the filename from its extension
            base_filename = os.path.splitext(os.path.basename(png_file))[0]  # Get file name without extension
            mask_filename = f"{base_filename}_mask.png"  # Append '_mask' to the file name

            # Ensure the mask directory exists
            os.makedirs(args.mask_dir, exist_ok=True)

            # Save the mask image to the specified mask directory
            mask_img.save(os.path.join(args.mask_dir, mask_filename))

    # Load and process a single PNG file
    if args.skip:
        png_file = png_files[file_index]
        image_handler = ImageHandler(png_file)
        image = image_handler.read_image()

        # Ensure the mask directory exists
        base_filename = os.path.splitext(os.path.basename(png_file))[0]  # Get file name without extension
        apply_and_save_masks(image, base_filename, args.mask_dir)




if __name__ == "__main__":
    args = step_1()

    # please remove this comment if you need to save these as png's or another file form such as tiff or pdf
    # step_2(args)
    for i in range(0, 2, 1):
        step_3(args, i)

    ## Example usage
    ### if you do not include `--skip` it will conduct this for all the frames in the movie
    # python src/segmentation/gen_ground_truths.py --input_file /Users/bebr1814/projects/anabaena/scratch_data/train_data/2020.3.5_ana33047_minusn_0003.nd2 --output_file /Users/zaca2954/academics/anabaena/data/png/ --figure_type png --mask_dir /Users/zaca2954/academics/anabaena/data/mask/ --skip
