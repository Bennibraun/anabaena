#!/bin/bash
#SBATCH -p nvidia-a100
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --mem=5gb

# This script enables submission of GPU-enabled jobs to Fiji


nvidia-smi

python run_segmentation.py --input_file /Users/bebr1814/projects/anabaena/scratch_data/2020.3.5_ana33047_minusn_0003.nd2 --output_file /Users/bebr1814/projects/anabaena/scratch_data/test1.tif --model /Users/bebr1814/projects/anabaena/models/33047/33047_chris_original


