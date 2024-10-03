# TODO's
- Train a new model similar to 33047_chris_original so we know what's going on
	- Also try running each model that exists and comparing
- Get ground truth
- Figure out evaluation system - maybe use the one from cellpose, or write a script to compare raw masks directly
- convert files to tiff's, ensure all current scripts work with tiff's and change if necessary to use `ImageHandler()`
- Learn how to hand-correct / annotate segmentation masks
- Create classification training set
- Image more cells
- Figure out tracking
- Get some kind of scientific readout / meaningful conclusion (what causes differentiation?)

# Finished

- [x] Figure out file formats - standardize to ND2 or TIFF? by: @caterer-z-t, cannot save nd2 images, lets standardize to TIFF, please see `src/file_formatting/README.md` for more information about using `ImageHandler()`