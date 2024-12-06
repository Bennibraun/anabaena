#!/bin/bash
#SBATCH -p nvidia-a100
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --mem=5gb

# This script enables submission of GPU-enabled jobs to Fiji

nvidia-smi

python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241114_ZMB_Anabaena/set1.006/tif/ --output_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241114_ZMB_Anabaena/set1.006/tif/ --model /scratch/Shares/anabaena_mcdb6440/bulk_training_set/models/cellpose_1733459883.7576745


