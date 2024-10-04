# Segmentation

Here in lies code for developing segmentation of anabaena. In this directory contains a few files. Previously written by Zach Maas, `diff_masks.py` and `segmentation_comparison.py` were written to compare masks for developing a segmentation model. 

Now, written by @caterer-z-t lies `gen_ground_truth.py` in an attempt to generate ground truth's to feed into the segmentation model. This script is written to utalize the ImageHandler class in `src/file_formatting/standardize_file_types.py` to convert the nd2 file into png's to then use various methods to develop the masks. likely this will consist of some method to automate the mask /ground truth generation then futher clarifiying these ground truths manually. An example of running this code would consist of 

``` bash 
python src/segmentation/gen_ground_truths.py --input_file /Users/bebr1814/projects/anabaena/scratch_data/train_data/2020.3.5_ana33047_minusn_0003.nd2 --output_file /Users/zaca2954/academics/anabaena/data/png/ --figure_type png
```