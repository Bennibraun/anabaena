# TODO's
- Train a new model similar to 33047_chris_original so we know what's going on
	- Also try running each model that exists and comparing
- Get ground truth
- Figure out evaluation system - maybe use the one from cellpose, or write a script to compare raw masks directly
- Learn how to hand-correct / annotate segmentation masks
- Create classification training set
- Image more cells
- Figure out tracking
- Get some kind of scientific readout / meaningful conclusion (what causes differentiation?)
- Overlay mask to unmasked image
- Use masks for denoising
- when using `ImageHandler()` to work on full movie in `run_segmentation.py` rather than one frame
- debug `segmentation.py`
- work on ground truths, on the movies, new data -- movies are basically individual images
- preprocessing steps to uniform brightness contrast
- format images and masks for cellpose 2.0 / 3.0, `_(img/image).tiff` and `_mask.tiff`

# Finished
- [x] convert files to tiff's, ensure all current scripts work with tiff's and change if necessary to use `ImageHandler()`
- [x] when saving `.tiff's` have the channels save as one file rather than seperates. for png's pdf's, and other vector and raster images 
- [x] update `ImageHandler()` to properly format the metadata in the new images collected, be able to handle all different cases of this
- [x] Figure out file formats - standardize to ND2 or TIFF? by: @caterer-z-t, cannot save nd2 images, lets standardize to TIFF, please see `src/file_formatting/README.md` for more information about using `ImageHandler()` -- WIP