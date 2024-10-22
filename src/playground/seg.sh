#!/bin/bash
#SBATCH -p nvidia-a100
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --mem=5gb

# This script enables submission of GPU-enabled jobs to Fiji

nvidia-smi

python /Users/zaca2954/academics/anabaena/src/playground/run_seg.py --input_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/20241010_ZMB_Anabaena/20241010_001_ZMB003/16.nd2 \
 --output_file /Users/zaca2954/academics/anabaena/anabaena_mcdb6440/playground/test.tif --model /Users/zaca2954/academics/anabaena/models/33047/33047_chris_original



