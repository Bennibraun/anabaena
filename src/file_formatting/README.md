# Standardizing file formats

the code in `standardize_file_types.py` is written to keep file formats consistent across this analysis. This code consists of an object `ImageHandler()` which can read nd2, and tif(f) files and can only save them to tif(f) files given that nd2 file types are specific to nikon microscopes, and writing to it requires access to the Nikon ND2 SDK, which is not publicly available.

Subsequently, we should standardize all of our image and image analysis to tif(f) files. This code is designed to do so. Below are examples of reading in an image vs reading and saving an image. 

``` python
from anabaena.src.file_formatting import ImageHandler

# file path to input file
input_file = '/file/path/to/img/<filename>.nd2'

# or alternatively an .tif(f) file
# input_file = '/file/path/to/img/<filename>.tif'

# Initialize the handler with the provided input file
img_handler = ImageHandler(input_file)

img = img_handler.read_image()
```

to save this image into a tif(f) file please use the following with continuing from above
``` python
# Output file path and name
output_file = '/file/path/to/save/img/<filename>.tif'

img_handler.save_image(output_file)
```