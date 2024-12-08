#!/bin/bash
#SBATCH -p nvidia-a100
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --mem=5gb

# This script enables submission of GPU-enabled jobs to Fiji

nvidia-smi

# python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241114_ZMB_Anabaena/set1.006/tif/ --output_dir /Users/bebr1814/projects/anabaena/scratch_data/bulk_segmentation_output --model /Users/bebr1814/projects/anabaena/scratch_data/training/models/bulk.lr01.wd0001.ep500.2chan.cyto3.12.7.24
python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/bulk_test_set/ --output_dir /Users/bebr1814/projects/anabaena/scratch_data/bulk_segmentation_output --model /Users/bebr1814/projects/anabaena/scratch_data/training/models/bulk.lr01.wd0001.ep500.2chan.cyto3.12.7.24
