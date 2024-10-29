# Standardizing file formats

the code in `standardize_file_types.py` is written to keep file formats consistent across this analysis. This code consists of an object `ImageHandler()` which can read nd2, and will save this file into its own individual images (feilds of view -- fov, or frames) for each of the channels. 

You can call this object in many ways, I will specify 2 here, bash and python. 

## 1. Bash
``` bash 
# example usage for any file type
python src/file_formatting/ImageHandler.py \
--input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB001/nd2/01.nd2 \
--output_dir /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground \
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
)

```