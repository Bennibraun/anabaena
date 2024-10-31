# In[1]: Imports
import os
import numpy as np
import tifffile
from nd2reader import ND2Reader
from tqdm import tqdm
from skimage.io import imsave
from skimage import img_as_ubyte

# In[2]: ImageHandler Class
class ImageHandler:
    def __init__(self, input_file, output_dir, selected_channels=None):
        """Initializes the ImageHandler class with the input file and output directory
        Args:
            input_file (str): Path to the input ND2 or TIFF file
            output_dir (str): Path to the output directory to save the TIFF and PNG files, makes the directory if it doesn't exist
            selected_channels (list): List of selected channels to process
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.reader = None
        self.file_type = None
        self.dimensions = ['x', 'y', 'c']
        self.selected_channels = selected_channels  # List of selected channels to process

        # Ensure output directories exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def setup_reader(self):
        """Sets up the reader based on the file type. Currently only supports ND2 files."""
        if self.input_file.endswith(".nd2"):
            self.file_type = "nd2"
            self.reader = ND2Reader(self.input_file)
            # Print ND2-specific metadata and image shape
            print(f"ND2 File Metadata: {self.reader.metadata}")
            print(f"ND2 Image Shape: {self.reader.sizes}")

        # commenting out b/c no functionality for tiff files yet

        # elif self.input_file.endswith(".tif") or self.input_file.endswith(".tiff"):
        #     self.file_type = "tif"
        #     self.reader = tifffile.imread(self.input_file)
        #     print(f"TIFF Image Shape: {self.reader.shape}")
        #     print(f"TIFF Data Type: {self.reader.dtype}")

        self.identify_frames() # Identify frames based on the dimensions of the ND2 or TIFF file

    def identify_frames(self):
        """Identifies frames based on the dimensions of the ND2 or TIFF file."""
        if self.file_type == 'nd2':
            # Check if 't' or 'v' dimensions are greater than 1
            t_size = self.reader.sizes.get('t',1)
            v_size = self.reader.sizes.get('v',0)

            if t_size > 1:
                # appending the t dimension so we know which dimension to iterate through
                self.dimensions.append('t')

            elif t_size == 1 and v_size > 1:
                # appending the v dimension so we know which dimension to iterate through                
                self.dimensions.append('v')

            elif t_size == 1 and v_size == 0:
                # check that the dimensions are just ['x','y','c']
                self.check_dimensions()

            else:
                raise ValueError("Unexpected dimensions in ND2 file.")
            
    def check_dimensions(self):
        """check that the dimensions are just ['x','y','c']

        Raises:
            ValueError: Raises error if dimensions are not ['x','y','c'] when it is expected they are
        """
        if self.dimensions != ['x','y','c']:
            raise ValueError("Dimensions must be ['x', 'y', 'c']")
        
    def get_frame(self, movie, frame_idx=0, v_idx=0):
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
            # Initialize a list to hold the frames for each channel
            channel_frames = []

            # Iterate over the channels and fetch the frames
            for num_channels in range(movie.sizes['c']):
                frame = movie.get_frame_2D(t=frame_idx, c=num_channels, v=v_idx)
                channel_frames.append(np.array(frame, dtype=np.uint16))

            # Stack the frames across the channel axis
            stacked_img = np.stack(channel_frames, axis=-1)
            return stacked_img

    def process_and_save_frames(
            self, 
            save_png: bool = False
            ):
        """Processes each frame and saves TIFFs for analysis and PNGs for visualization."""
        print(f"Reading input file {self.input_file}")
        base_filename = os.path.splitext(os.path.basename(self.input_file))[0]

        with self.reader as images:
            print(self.dimensions)

            if self.dimensions == ['x', 'y', 'c']:
                self.process_single_frame(self.get_frame(images, 0), base_filename, save_png)
            
            elif 't' in self.dimensions:
                self.process_frames_over_time(images, base_filename, save_png)
            
            elif 'v' in self.dimensions:
                self.process_frames_over_fov(images, base_filename, save_png)

    def save_individual_tiff(self, tiff_stack, base_filename: str, i: int, save_tiff: bool = False, channel_name: str = None):
        if save_tiff:
            if channel_name:
                output_tiff_path = os.path.join(self.output_dir, f'{base_filename}_{i:04d}_{channel_name.lower().replace(" ", "_")}_image.tiff')
            else:
                output_tiff_path = os.path.join(self.output_dir, f'{base_filename}_{i:04d}_image.tiff')
            tifffile.imwrite(output_tiff_path, np.array(tiff_stack))
            print('Saved TIFF:', output_tiff_path)

    def process_single_frame(self, image, base_filename, save_png):
        """Processes a single frame and saves necessary files."""
        self.save_channel_tiffs(image, base_filename, 0, save_png)

    def process_frames_over_time(self, images, base_filename, save_png:bool = False):
        """Processes frames over time and saves necessary files."""
        t_size = self.reader.sizes['t']

        for i in tqdm(range(t_size), desc="Frames", unit="frame"):
            image = self.get_frame(images, frame_idx=i)
            self.save_channel_tiffs(image, base_filename, i, save_png)
        return image

    def process_frames_over_fov(self, images, base_filename, save_png:bool = False):
        """Processes frames over fields of view and saves necessary files."""
        v_size = self.reader.sizes['v']

        for i in tqdm(range(v_size), desc="Frames", unit="frame"):

            image = self.get_frame(images, v_idx=i)
            self.save_channel_tiffs(image, base_filename, i, save_png)

        return image

    def get_channels_to_save(self):
        """Returns the indices of channels to save."""
        if self.selected_channels is None:
            return range(len(self.reader.metadata['channels']))  # Save all channels if none specified
        else:
            return [self.reader.metadata['channels'].index(channel) for channel in self.selected_channels]

    def save_png(self, base_filename, frame_index, channel_name, channel_image):
        """Saves a PNG for a given frame and channel."""
        png_filename = f"{base_filename}_frame_{frame_index:04d}_{channel_name.lower().replace(' ', '_')}.png"
        png_path = os.path.join(self.output_dir, png_filename)  
        imsave(png_path, img_as_ubyte(channel_image))
        print(f"Saved PNG: {png_path}")

    def save_channel_tiffs(self, image, base_filename, i, save_png):
        """Saves individual TIFFs for each channel in the image."""
        channels_to_save = self.get_channels_to_save()

        for ch in channels_to_save:
            channel_name = self.reader.metadata['channels'][ch]
            channel_image = image[..., ch]
            if channel_name == 'Mono':
                channel_name = 'Brightfield'

            # save individual channel tiff
            self.save_individual_tiff([channel_image], base_filename, i, save_tiff=True, channel_name=channel_name)
            if save_png:
                self.save_png(base_filename, i, channel_name, [channel_image])

# In[3]: Main Function
def main(
        input_file, 
        output_dir, 
        save_png=False, 
        selected_channels=None
        ):
    
    processor = ImageHandler(
        input_file=input_file,
        output_dir=output_dir,
        selected_channels=selected_channels,
    )
    processor.setup_reader()
    processor.process_and_save_frames(
        save_png=save_png
    )

# In[4]: Command Line Interface
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

# In[5]: Example Usage
## example usage for any file type

# python src/file_formatting/ImageHandler.py \
# --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB001/nd2/01.nd2 \
# --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground \
# --save_png
