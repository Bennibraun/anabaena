from PIL import Image
import tifffile as tiff
import nd2reader
import numpy as np
import os
import argparse
import nd2
import imageio

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
        
        elif self.file_extension == '.png':
            try:
                image = Image.open(self.file_path)
                self.image = np.array(image)
                return self.image
            except Exception as png_error:
                print(f'Error reading png file: {png_error}')
                return None
            
        else:
            print(f"Unsupported file format: {self.file_extension}")
            return None

    def save_image(self, save_path, figure_type:str = None):
        """Save the image to the specified path.

        Args:
            save_path (str): file path for the saved image or directory path for saving TIFF files.

        Raises:
            ValueError: If Pillow cannot save image due to being in improper format
        """
        if os.path.isdir(save_path):
            if figure_type == 'tiff':
                # If the save path is a directory, save using the ND2 method
                self.save_nd2_as_tiff(save_path)  # Pass the directory path directly
                return
            elif figure_type == 'png':
                self.save_as_png(save_path)
                return
            elif figure_type == 'pdf':
                self.save_as_pdf(save_path)
                return
    
        try:
            file_extension = os.path.splitext(save_path)[1].lower()
        except Exception as e:
            print(f"Error obtaining file extension: {e}")
            file_extension = None

        # Handle saving as TIFF
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
        
        # Handle saving as PNG
        elif file_extension == '.png':
            self.save_as_png(save_path)
        
        # Handle saving as PDF
        elif file_extension == '.pdf':
            self.save_as_pdf(save_path)

        elif file_extension is None and self.file_extension == ".nd2":
            # Save ND2 using the new method
            self.save_nd2_as_tiff(save_path)
        
        else:
            print(f"Unsupported file format for saving: {file_extension}")

    def save_nd2_as_tiff(self, output_directory):
        """Read ND2 file and save each frame as TIFF.

        Args:
            output_directory (str): Directory for saving output TIFF files.
        """
        # Extract the base filename without the extension from self.file_path
        base_filename = os.path.splitext(os.path.basename(self.file_path))[0]

        with nd2.ND2File(self.file_path) as nd2_file:
            data = nd2_file.asarray()  # Assuming data shape is (t, c, z, y, x)

            print(f"Data shape: {data.shape}")
            num_frames = data.shape[0]
            num_channels = data.shape[1]

            for t in range(num_frames):
                for c in range(num_channels):
                    frame = data[t, c]  # Extract the frame for the current time and channel
                    frame_normalized = np.clip(frame, 0, 65535).astype(np.uint16)  # Normalize the frame

                    # Use the base filename for the output, appending the appropriate elements
                    output_filename = os.path.join(output_directory, f"{base_filename}_t{t}_c{c}.tiff")
                    imageio.imwrite(output_filename, frame_normalized)
                    print(f"Saved {output_filename}")

    def save_as_png(self, save_path):
        """Save each frame of the image as individual PNG files.

        Args:
            save_path (str): Directory to save the PNG files.
        """
        # Extract the base filename without the extension from self.file_path
        base_filename = os.path.splitext(os.path.basename(self.file_path))[0]

        with nd2.ND2File(self.file_path) as nd2_file:
            data = nd2_file.asarray()  # Assuming data shape is (t, c, z, y, x)

            print(f"Data shape: {data.shape}")
            num_frames = data.shape[0]
            num_channels = data.shape[1]

            for t in range(num_frames):
                for c in range(num_channels):
                    frame = data[t, c]  # Extract the frame for the current time and channel
                    frame_normalized = np.clip(frame, 0, 65535).astype(np.uint16)  # Normalize the frame

                    # Use the base filename for the output, appending the appropriate elements
                    output_filename = os.path.join(save_path, f"{base_filename}_t{t}_c{c}.png")
                    imageio.imwrite(output_filename, frame_normalized)
                    print(f"Saved {output_filename}")

    def save_as_pdf(self, save_path):
        """Save each frame of the image as individual PDF files.

        Args:
            save_path (str): Directory to save the PDF files.
        """
        # Extract the base filename without the extension from self.file_path
        base_filename = os.path.splitext(os.path.basename(self.file_path))[0]

        with nd2.ND2File(self.file_path) as nd2_file:
            data = nd2_file.asarray()  # Assuming data shape is (t, c, z, y, x)

            print(f"Data shape: {data.shape}")
            num_frames = data.shape[0]
            num_channels = data.shape[1]

            for t in range(num_frames):
                for c in range(num_channels):
                    frame = data[t, c]  # Extract the frame for the current time and channel
                    frame_normalized = np.clip(frame, 0, 65535).astype(np.uint16)  # Normalize the frame

                    # Use the base filename for the output, appending the appropriate elements
                    output_filename = os.path.join(save_path, f"{base_filename}_t{t}_c{c}.pdf")
                    imageio.imwrite(output_filename, frame_normalized)
                    print(f"Saved {output_filename}")

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
