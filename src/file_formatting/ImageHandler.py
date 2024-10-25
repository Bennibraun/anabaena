import os
import numpy as np
import tifffile
from nd2reader import ND2Reader
from tqdm import tqdm
from skimage.io import imsave
from skimage import img_as_ubyte

class ImageHandler:
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

        # commenting out b/c no functionality for tiff files yet

        # elif self.input_file.endswith(".tif") or self.input_file.endswith(".tiff"):
        #     self.file_type = "tif"
        #     self.reader = tifffile.imread(self.input_file)
        #     print(f"TIFF Image Shape: {self.reader.shape}")
        #     print(f"TIFF Data Type: {self.reader.dtype}")

        self.identify_frames()

    def identify_frames(self):
        """Identifies frames based on the dimensions of the ND2 or TIFF file."""
        if self.file_type == 'nd2':
            # Check if 't' dimension is greater than 1
            t_size = self.reader.sizes.get('t',1)
            v_size = self.reader.sizes.get('v',0)

            self.has_v_dimensions = v_size > 0

            if t_size > 1:
                # appending the t dimension so we know which dimension to iterate through
                self.dimensions.append('t')

            elif t_size == 1 and v_size > 1:
                # appending the v dimension so we know which dimension to iterate through                
                self.dimensions.append('v')

            elif t_size == 1 and v_size == 0:
                # Only one frame available
                self.frames = [0]  # Only one frame

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
        
    def get_movie_frame(self, movie, frame_idx):
        """Given a movie and a frame index, load the frame from the movie."""
        if self.file_type == "nd2":
            # print('getting movie frame')
            movie.bundle_axes = ["y", "x", "c"]
            movie_frame = movie.get_frame(frame_idx)
            # print(movie_frame.shape)
            return np.array(movie_frame, dtype=np.uint16)
        
        # comenting out b/c no funcitonality for tiff
        # elif self.file_type == "tif":
        #     return movie[frame_idx]

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
            return movie[v_idx]

    def process_and_save_frames(
            self, 
            save_png: bool = False, 
            save_frames:bool = False, 
            save_fov:bool = False, 
            ):
        """Processes each frame and saves TIFFs for analysis and PNGs for visualization."""
        print(f"Reading input file {self.input_file}")
        base_filename = os.path.splitext(os.path.basename(self.input_file))[0]

        # Initialize TIFF stack
        tiff_stack = []

        with self.reader as images:
            print(self.dimensions)

            if self.dimensions == ['x', 'y', 'c']:
                image = self.get_movie_frame(images, 0)
                tiff_stack = self.process_single_frame(image, base_filename, save_png)
            
            elif 't' in self.dimensions:
                tiff_stack = self.process_frames_over_time(images, base_filename, save_png, save_frames)
            
            elif 'v' in self.dimensions:
                tiff_stack = self.process_frames_over_fov(images, base_filename, save_png, save_fov)

            # self.save_channelsplit_tiff(base_filename, tiff_stack)
        
    def save_channelsplit_tiff(self, base_filename, tiff_stack):
        # Save TIFF stack
        output_tiff_path = os.path.join(self.output_dir, f"{base_filename}.tiff")
        n_channels = self.reader.shape[-1]
        print(self.reader.shape)

        image = self.reader[0]
        image = image.transpose(2,0,1)

        print(image.shape)
        print(image)

        print(image[0])

        for c in range(n_channels):
            name = os.path.join(self.output_dir, f"{base_filename}.tiff").replace('.tif',f'.{self.reader.metadata["channels"][c].replace(" ","_").lower().replace("mono","brightfield")}.tif')
            tifffile.imwrite(name, image[c])
            print('Saved TIFF:', name)
        # tifffile.imwrite(output_tiff_path, np.array(tiff_stack))

    def save_individual_tiff(self, tiff_stack, base_filename: str, i: int, save_tiff: bool = False, channel_name: str = None):
        if save_tiff:
            if channel_name:
                output_tiff_path = os.path.join(self.output_dir, f'{base_filename}_{i:04d}_{channel_name}.tiff')
            else:
                output_tiff_path = os.path.join(self.output_dir, f'{base_filename}_{i:04d}.tiff')
            tifffile.imwrite(output_tiff_path, np.array(tiff_stack))
            print('Saved TIFF:', output_tiff_path)

    def process_single_frame(self, image, base_filename, save_png):
        """Processes a single frame and saves necessary files."""
        tiff_stack = []

        # print('processing single frame')
        
        channels_to_save = self.get_channels_to_save(image)

        # print(channels_to_save)
        for ch in channels_to_save:
            channel_name = self.reader.metadata['channels'][ch]
            channel_image = image[..., ch]

            # save individual channel tiff
            self.save_individual_tiff([channel_image], base_filename, 0, save_tiff=True, channel_name=channel_name)

            # Save PNG if required
            if save_png:
                self.save_png(base_filename, 0, channel_name, channel_image)

        tiff_stack.append(image)
        return tiff_stack

    def process_frames_over_time(self, images, base_filename, save_png:bool = False, save_tiff:bool = False):
        """Processes frames over time and saves necessary files."""
        t_size = self.reader.sizes['t']
        tiff_stack = []

        for i in tqdm(range(t_size), desc="Frames", unit="frame"):
            image = self.get_movie_frame(images, i)
            print(f"Frame {i} Shape: {image.shape}")
            print(f"Frame {i} Data Type: {image.dtype}")

            channels_to_save = self.get_channels_to_save(image)
            channel_tiff_stack=[]

            # save this image and the individual channels to different channels
            # to individual tiffs


            for ch in channels_to_save:
                channel_name = self.reader.metadata['channels'][ch]
                channel_image = image[..., ch]
                if channel_name == 'Mono':
                    channel_name = 'Brightfield'
                # save individual channel tiff
                self.save_individual_tiff([channel_image], base_filename, i, save_tiff=True, channel_name=channel_name)

                # Append the channel image to the TIFF stack for saving
                channel_tiff_stack.append(channel_image)

                if save_png:
                    self.save_png(base_filename, i, channel_name, channel_image)

            # Save individual TIFF for the current time frame, if specified
            # self.save_individual_tiff(channel_tiff_stack, base_filename, i, save_tiff)

            tiff_stack.append(image)

        return tiff_stack

    def process_frames_over_fov(self, images, base_filename, save_png:bool = False, save_tiff:bool = False):
        """Processes frames over fields of view and saves necessary files."""
        v_size = self.reader.sizes['v']
        tiff_stack = []

        for i in tqdm(range(v_size), desc="Frames", unit="frame"):
            image = self.get_movie_fov(images, i)
            print(f"Frame {i} Shape: {image.shape}")
            print(f"Frame {i} Data Type: {image.dtype}")

            channels_to_save = self.get_channels_to_save(image)
            channel_tiff_stack = []

            for ch in channels_to_save:
                channel_name = self.reader.metadata['channels'][ch]
                channel_image = image[..., ch]
                
                if channel_name == 'Mono':
                    channel_name = 'Brightfield'

                # save individual channel tiff
                self.save_individual_tiff([channel_image], base_filename, i, save_tiff=True, channel_name=channel_name)

                # Append the channel image to the TIFF stack for saving
                channel_tiff_stack.append(channel_image)
                
                if save_png:
                    self.save_png(base_filename, i, channel_name, channel_image)

            # Save individual TIFF for the current field of view, if specified
            # self.save_individual_tiff(channel_tiff_stack, base_filename, i, save_tiff)

            tiff_stack.append(image)

        return tiff_stack

    def get_channels_to_save(self, image):
        """Returns the indices of channels to save."""
        if self.selected_channels is None:
            return range(image.shape[2])  # Save all channels if none specified
        else:
            return [self.reader.metadata['channels'].index(channel) for channel in self.selected_channels]

    def save_png(self, base_filename, frame_index, channel_name, channel_image):
        """Saves a PNG for a given frame and channel."""
        png_filename = f"{base_filename}_frame_{frame_index:04d}_{channel_name.lower().replace(' ', '_')}.png"
        png_path = os.path.join(self.output_dir, png_filename)
        imsave(png_path, img_as_ubyte(channel_image))
        print(f"Saved PNG: {png_path}")


def main(
        input_file, 
        output_dir, 
        save_png=False, 
        save_frames=False, 
        save_fov=False, 
        selected_channels=None
        ):
    
    processor = ImageHandler(
        input_file=input_file,
        output_dir=output_dir,
        selected_channels=selected_channels,
    )
    processor.setup_reader()
    processor.process_and_save_frames(
        save_png=save_png,
        save_frames=save_frames, 
        save_fov=save_fov,
    )

if __name__ == "__main__":
    import argparse

    # Function to parse boolean values from the command line
    def str_to_bool(v):
        if v.lower() in ('true', '1'):
            return True
        elif v.lower() in ('false', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError("Boolean value expected.")

    parser = argparse.ArgumentParser(description="ND2 to TIFF conversion and segmentation")
    parser.add_argument("--input_file", type=str, help="Path to the ND2 or TIFF input file")
    parser.add_argument("--output_dir", type=str, help="Directory to save the output TIFF and PNG files")
    parser.add_argument("--save_png", action="store_true", help="Whether to save PNG files for visualization")
    parser.add_argument('--save_frames', action='store_true', help="Whether to save each frame individually")
    parser.add_argument('--save_fov', action='store_true', help="Whether to save each fov individually")
    parser.add_argument("--channels", nargs='+', default=None, help="Specify which channels to save (e.g., 'Cy5', 'Mono')")

    args = parser.parse_args()

    main(
        input_file=args.input_file,
        output_dir=args.output_dir,
        save_png=args.save_png,
        save_frames=args.save_frames,
        save_fov=args.save_fov,
        selected_channels=args.channels,
    )

## example usage

# multi fov tiff, pngs
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_png

# multi fov tiff, no png's
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground 

# single fov tiff
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB002/1.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_png

# single fov tiff, no png's
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB002/1.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground 

# multi frames tiff, pngs
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20210709_Ana_-N_to_-N_channelbf,cy5,cfp,rfp_seq0000_0000.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_png

# multi frames tiff, no png's
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20210709_Ana_-N_to_-N_channelbf,cy5,cfp,rfp_seq0000_0000.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground

# multi fov tiff, individual fov tiff, pngs
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_png --save_fov

# multi fov tiff, individual fov tiff, no png's
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_fov

# individual fov's no multi tiff, no png
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground

# mutli frame tiff combined, individual frame tiff, pngs
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20210709_Ana_-N_to_-N_channelbf,cy5,cfp,rfp_seq0000_0000.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_png --save_frames

# individual frame tiff, no multiframe tiff, pngs
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20210709_Ana_-N_to_-N_channelbf,cy5,cfp,rfp_seq0000_0000.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_png --save_frames

# individual frame tiff, no multiframe tiff, no pngs
## python src/file_formatting/ImageHandler.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20210709_Ana_-N_to_-N_channelbf,cy5,cfp,rfp_seq0000_0000.nd2 --output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground --save_frames