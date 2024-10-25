# Standardizing file formats

the code in `standardize_file_types.py` is written to keep file formats consistent across this analysis. This code consists of an object `ImageHandler()` which can read nd2, and will save this file into its own individual images (feilds of view -- fov, or frames) for each of the channels. 

You can call this object in many ways, I will specify 2 here, bash and python. 

## 1. Bash
``` bash 
# example usage for one frame or fov
python src/file_formatting/ImageHandler.py \
--input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB001/nd2/01.nd2 \
--output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground \

# Example usage for multiple fov's
python src/file_formatting/ImageHandler.py \
--input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB.nd2 \
--output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground \
--save_fov

# Example usage for multiple frames
python src/file_formatting/ImageHandler.py \
--input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20210709_Ana_-N_to_-N_channelbf,cy5,cfp,rfp_seq0000_0000.nd2 \
--output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground \
--save_frames
```

## 2. Python
``` python
from anabaena.src.file_formatting import ImageHandler

# file path to input file
input_file = '/file/path/to/img/<filename>.nd2'
output_dir = "/file/path/to/output_dir/
# Initialize the handler with the provided input file
processor = ImageHandler(
    input_file = input_file,
    output_dir = output_dir,
    )
processor.setup_reader()
processor.process_and_save_frames(
    save_png = False, # Set to True if you want to save png's
    save_frames = False, # Set to True if you have a movie and want to save individual frames
    save_fov = False, # Set to True if you have multiple fov's and want to save them
)

```