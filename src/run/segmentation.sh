#!/bin/bash
#SBATCH -p nvidia-a100
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --mem=5gb

# This script enables submission of GPU-enabled jobs to Fiji

nvidia-smi

# python /Users/zaca2954/academics/anabaena/src/run/run_segmentation.py --input_file /Users/bebr1814/projects/anabaena/scratch_data/train_data/2020.3.5_ana33047_minusn_0003.nd2 --output_file /Users/bebr1814/projects/anabaena/scratch_data/test1.tif --model /Users/bebr1814/projects/anabaena/models/33047/33047_chris_original


# python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB001/tif/ --output_dir projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB001/tif --model /Users/bebr1814/projects/anabaena/models/33047/33047_chris_original

# python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB002/tif/ --output_dir projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB002/tif --model /Users/bebr1814/projects/anabaena/models/33047/33047_chris_original

# python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB003/tif/ --output_dir projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB003/tif --model /Users/bebr1814/projects/anabaena/models/33047/33047_chris_original

# python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB004/tif/ --output_dir projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB004/tif --model /Users/bebr1814/projects/anabaena/models/33047/33047_chris_original



# new model
python run_segmentation_tiffs.py --input_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB001/preprocessed/ --output_dir /Users/bebr1814/projects/anabaena/scratch_data/fov_images/20241010_ZMB_Anabaena/20241010_001_ZMB001/preprocessed/ --model /Users/bebr1814/projects/anabaena/scratch_data/fov_images/training_data/models/cellpose_1731008382.5787175

