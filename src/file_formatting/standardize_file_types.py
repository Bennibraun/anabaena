from PIL import Image
import tifffile as tiff
import nd2reader
import numpy as np
import os
import argparse

class ImageHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_extension = os.path.splitext(file_path)[1].lower()
        self.image = None  # This will hold the loaded image object

    def read_image(self):
        """Read image from file based on the file extension.

        Returns:
            self.image: object of the image
        """
        if self.file_extension in ['.tif', '.tiff']:
            # First attempt to read TIFF with Pillow
            try:
                self.image = Image.open(self.file_path)
                print(f"Successfully read TIFF using Pillow: {self.file_path}")
                return self.image
            except Exception as pillow_error:
                print(f"Error with Pillow, trying tifffile: {pillow_error}")
                
                # If Pillow fails, attempt to read using tifffile
                try:
                    self.image = tiff.imread(self.file_path)
                    print(f"Successfully read TIFF using tifffile: {self.file_path}")
                    return self.image
                except Exception as tifffile_error:
                    print(f"Error reading TIFF with tifffile: {tifffile_error}")
                    return None

        elif self.file_extension == '.nd2':
            # Use ND2Reader to read ND2 files
            try:
                with nd2reader.ND2Reader(self.file_path) as nd2_file:
                    self.image = np.array(nd2_file)  # Convert ND2Reader object to numpy array
                    print(f"Successfully read ND2 file: {self.file_path}")
                    return self.image
            except Exception as nd2_error:
                print(f"Error reading ND2 file: {nd2_error}")
                return None

        else:
            print(f"Unsupported file format: {self.file_extension}")
            return None

    def save_image(self, save_path):
        """Save the image to the specified path.

        Args:
            save_path (str): file path for the saved image

        Raises:
            ValueError: If Pillow cannot save image do to being in improper format
        """
        file_extension = os.path.splitext(save_path)[1].lower()
        
        if file_extension in ['.tif', '.tiff']:
            # Try saving TIFF using Pillow first
            try:
                if isinstance(self.image, Image.Image):
                    self.image.save(save_path)
                    print(f"Successfully saved image using Pillow: {save_path}")
                else:
                    raise ValueError("Image not in Pillow format, trying tifffile")
            except Exception as pillow_save_error:
                print(f"Error saving with Pillow, trying tifffile: {pillow_save_error}")
                
                # Try saving TIFF using tifffile if Pillow fails
                try:
                    tiff.imwrite(save_path, self.image)
                    print(f"Successfully saved image using tifffile: {save_path}")
                except Exception as tifffile_save_error:
                    print(f"Error saving image with tifffile: {tifffile_save_error}")
        
        elif file_extension == '.nd2':
            # Saving ND2 is not supported, notify the user
            print(f"Saving ND2 format is not currently supported in this class, or in Python.")
        
        else:
            print(f"Unsupported file format for saving: {file_extension}")


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Read and optionally save image files.")
    
    # Required input file argument
    parser.add_argument("--input_file", type=str, help="Path to the input image file.")
    
    # Optional output file argument
    parser.add_argument("--output_file", type=str, help="Path to save the output image file. If not provided, the image will not be saved.", default=None)
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Initialize the handler with the provided input file
    image_handler = ImageHandler(args.input_file)

    # Read the image
    image = image_handler.read_image()

    # If an output file is provided, save the image
    if args.output_file:
        image_handler.save_image(args.output_file)
    else:
        print("No output path provided. Image will not be saved.")

if __name__ == "__main__":
    main()

    # example usage
    ## reading an image
    ### python your_script.py --input_file /path/to/input/file.nd2

    ## saving an image
    ### python your_script.py --input_file /path/to/input/file.nd2 --output_file /path/to/output/file.tif


