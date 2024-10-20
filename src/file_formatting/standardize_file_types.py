import os
import numpy as np
import tifffile
from nd2reader import ND2Reader
from tqdm import tqdm
from skimage.io import imsave
from skimage import img_as_ubyte

# TODO:
#   Frames correspond to time series (movies) (old videos)
#   Feilds of view correspond to different images collected at same time (new images)
#   Need to take into account when num_frames is 1 (no time series) or num_frames > 1 (time series) and save all in same format
#   Do we want to seperate the individual feilds of view that it is an individual .tiff (i think yes)
#   lets just use nd2 image shape t=time point, v=feilds_of_view

class ND2ToTiffSegmentation:
    def __init__(self, input_file, output_dir, selected_channels=None):
        self.input_file = input_file
        self.output_dir = output_dir
        self.reader = None
        self.file_type = None
        self.frames = None
        self.dimensions = ['x', 'y', 'c']
        self.selected_channels = selected_channels  # List of selected channels to process

        # Ensure output directories exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def setup_reader(self):
        """Sets up the reader based on the file type."""
        if self.input_file.endswith(".nd2"):
            self.file_type = "nd2"
            self.reader = ND2Reader(self.input_file)
            # Print ND2-specific metadata and image shape
            print(f"ND2 File Metadata: {self.reader.metadata}")
            print(f"ND2 Image Shape: {self.reader.sizes}")

        elif self.input_file.endswith(".tif") or self.input_file.endswith(".tiff"):
            self.file_type = "tif"
            self.reader = tifffile.imread(self.input_file)
            print(f"TIFF Image Shape: {self.reader.shape}")
            print(f"TIFF Data Type: {self.reader.dtype}")

        self.identify_frames()

    def identify_frames(self):
        """Identifies frames based on the dimensions of the ND2 or TIFF file."""
        if self.file_type == 'nd2':
            # Check if 't' dimension is greater than 1
            t_size = self.reader.sizes['t']
            v_size = self.reader.sizes['v']

            if t_size > 1:
                # appending the t dimension so we know which dimension to iterate through
                self.dimensions.append('t')

            elif t_size == 1 and v_size > 1:
                # appending the v dimension so we know which dimension to iterate through                
                self.dimensions.append('v')

            elif t_size == 1 and v_size == 1:
                # Only one frame available
                self.frames = [0]  # Only one frame

                # check that the dimensions are just ['x','y','c']
                if self.dimensions != ['x','y','c']:
                    raise ValueError("Dimensions must be ['x', 'y', 'c']")
            else:
                raise ValueError("Unexpected dimensions in ND2 file.")

    ## TODO:
    ## modify this method that it iterates through the v or t axis depending on 
    ## self.dimensions specification
    def get_movie_frame(self, movie, frame_idx):
        """Given a movie and a frame index, load the frame from the movie."""
        if self.file_type == "nd2":
            movie.bundle_axes = ["y", "x", "c"]
            movie_frame = movie.get_frame(frame_idx)
            return np.array(movie_frame, dtype=np.uint16)
        elif self.file_type == "tif":
            return movie[frame_idx]

    def get_movie_fov(self, movie, v_idx=None, frame_idx=0):
        """
        Given a movie and an index for the 'v' axis (such as fields of view or time points),
        load the image with 'x', 'y', and 'c' dimensions.
        
        Args:
            movie: The movie file (e.g., ND2 or TIF format).
            v_idx: The index along the 'v' axis (fields of view or time points). If None, load all.
            frame_idx: The index of the frame for ND2 files (default is 0 for static images).
        
        Returns:
            A numpy array representing the selected FOV across all channels for the 'v' index.
            If v_idx is None, returns all fields of view.
        """
        if self.file_type == "nd2":
            # Ensure x, y, and c dimensions are bundled together
            movie.bundle_axes = ["y", "x", "c"]

            # Initialize a list to hold the frames for each channel
            channel_frames = []

            # Iterate over the channels and fetch the frames
            for num_channels in range(movie.sizes['c']):
                frame = movie.get_frame_2D(t=frame_idx, c=num_channels, v=v_idx)
                channel_frames.append(np.array(frame, dtype=np.uint16))

            # Stack the frames across the channel axis
            stacked_img = np.stack(channel_frames, axis=-1)
            return stacked_img

        elif self.file_type == "tif":
            # If it's a TIF file, directly access the image at the v index (FOV index)
            return movie[v_idx],


    def process_and_save_frames(self, save_png: bool = False):
        """Processes each frame and saves TIFFs for analysis and PNGs for visualization."""
        print(f"Reading input file {self.input_file}")
        base_filename = os.path.splitext(os.path.basename(self.input_file))[0]

        ## TODO: 
        ## Implement self.frames to be used here with the channels
        ## over self.end_frame and self.start_frame 
        with self.reader as images:
            print(self.dimensions)
            if self.dimensions == ['x', 'y', 'c']:
                # we just need to save the one frame for all the channels

                tiff_stack=[]

                image = self.get_movie_frame(images, 0)

                # Determine which channels to save
                if self.selected_channels is None:
                    channels_to_save = range(image.shape[2])  # Save all channels if none specified
                else:
                    # Get indices of the selected channels
                    channels_to_save = [self.reader.metadata['channels'].index(channel) for channel in self.selected_channels]

                for ch in channels_to_save:
                    channel_name = self.reader.metadata['channels'][ch]
                    channel_image = image[..., ch]
                    
                    # Save PNG for visualization with channel info in filename
                    if save_png:
                        png_filename = f"{base_filename}_frame_0_{channel_name.lower().replace(' ', '_')}.png"
                        png_path = os.path.join(self.output_dir, png_filename)
                        imsave(png_path, img_as_ubyte(channel_image))
                        print(f"Saved PNG: {png_path}")

                # Append the image to the TIFF stack
                tiff_stack.append(image)

                # Save the stack of images as a multi-page TIFF for analysis
                output_tiff_path = os.path.join(self.output_dir, f"{base_filename}.tiff")
                tifffile.imwrite(output_tiff_path, np.array(tiff_stack))
            
            elif 't' in self.dimensions:
                t_size = self.reader.sizes['t']

                tiff_stack=[]

                for i in tqdm(range(0, t_size), desc="Frames", unit="frame"):
                    image = self.get_movie_frame(images, i)

                    # Print shape and type of the current image
                    print(f"Frame {i} Shape: {image.shape}")
                    print(f"Frame {i} Data Type: {image.dtype}")
                    
                    # Determine which channels to save
                    if self.selected_channels is None:
                        channels_to_save = range(image.shape[2])  # Save all channels if none specified
                    else:
                        # Get indices of the selected channels
                        channels_to_save = [self.reader.metadata['channels'].index(channel) for channel in self.selected_channels]

                    for ch in channels_to_save:
                        channel_name = self.reader.metadata['channels'][ch]
                        channel_image = image[..., ch]
                        
                        # Save PNG for visualization with channel info in filename
                        if save_png:
                            png_filename = f"{base_filename}_frame_{i:04d}_{channel_name.lower().replace(' ', '_')}.png"
                            png_path = os.path.join(self.output_dir, png_filename)
                            imsave(png_path, img_as_ubyte(channel_image))
                            print(f"Saved PNG: {png_path}")

                    # Append the image to the TIFF stack
                    tiff_stack.append(image)

                # Save the stack of images as a multi-page TIFF for analysis
                output_tiff_path = os.path.join(self.output_dir, f"{base_filename}.tiff")
                tifffile.imwrite(output_tiff_path, np.array(tiff_stack))

            elif 'v' in self.dimensions:
                v_size = self.reader.sizes['v']

                tiff_stack=[]

                for i in tqdm(range(0, v_size), desc="Frames", unit="frame"):
                    image = self.get_movie_fov(images, i)

                    # Print shape and type of the current image
                    print(f"Frame {i} Shape: {image.shape}")
                    print(f"Frame {i} Data Type: {image.dtype}")
                    print(f"Expected channels: {self.reader.sizes['c']}")

                    # Determine which channels to save
                    if self.selected_channels is None:
                        channels_to_save = range(0,self.reader.sizes['c'])  # Save all channels if none specified
                    else:
                        # Get indices of the selected channels
                        channels_to_save = [self.reader.metadata['channels'].index(channel) for channel in self.selected_channels]

                    for ch in channels_to_save:
                        channel_name = self.reader.metadata['channels'][ch]
                        channel_image = image[..., ch]
                        
                        # Save PNG for visualization with channel info in filename
                        if save_png:
                            png_filename = f"{base_filename}_frame_{i:04d}_{channel_name.lower().replace(' ', '_')}.png"
                            png_path = os.path.join(self.output_dir, png_filename)
                            imsave(png_path, img_as_ubyte(channel_image))
                            print(f"Saved PNG: {png_path}")

                    # Append the image to the TIFF stack
                    tiff_stack.append(image)

                # Save the stack of images as a multi-page TIFF for analysis
                output_tiff_path = os.path.join(self.output_dir, f"{base_filename}.tiff")
                tifffile.imwrite(output_tiff_path, np.array(tiff_stack))


def main(input_file, output_dir, save_png=False, selected_channels=None):
    processor = ND2ToTiffSegmentation(
        input_file=input_file,
        output_dir=output_dir,
        selected_channels=selected_channels,
    )
    processor.setup_reader()
    processor.process_and_save_frames(save_png=save_png)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ND2 to TIFF conversion and segmentation")
    parser.add_argument("--input_file", type=str, help="Path to the ND2 or TIFF input file")
    parser.add_argument("--output_dir", type=str, help="Directory to save the output TIFF and PNG files")
    parser.add_argument("--save_png", action="store_true", help="Whether to save PNG files for visualization")
    parser.add_argument("--channels", nargs='+', default=None, help="Specify which channels to save (e.g., 'Cy5', 'Mono')")

    args = parser.parse_args()

    main(
        input_file=args.input_file,
        output_dir=args.output_dir,
        save_png=args.save_png,
        selected_channels=args.channels,
    )
## example usage
##  python src/file_formatting/standardize_file_types.py \
# --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB.nd2 \
# --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground \
# --save_png