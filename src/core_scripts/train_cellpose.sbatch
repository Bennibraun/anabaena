#!/bin/bash
#SBATCH --output=/scratch/Shares/anabaena_mcdb6440/training/logs/%x_%j.out
#SBATCH --error=/scratch/Shares/anabaena_mcdb6440/training/logs/%x_%j.err
#SBATCH -p nvidia-a100
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --gres=gpu:1
#SBATCH --mem=32gb

set -euxo pipefail

outdir=/scratch/Shares/anabaena_mcdb6440/training/models

# trainDir=/scratch/Shares/anabaena_mcdb6440/fov_images/20241010_ZMB_Anabaena/training_data
# trainDir=/scratch/Shares/anabaena_mcdb6440/movies/training_images
trainDir=/scratch/Shares/anabaena_mcdb6440/bulk_training_set
name="bulk.lr00001.wd0001.ep500.2chan.cyto3.12.6.24"

model="cyto3"

cd "$trainDir" || exit 1
python -m cellpose --train --use_gpu \
        --verbose --chan 0 --chan2 1 \
        --dir "$trainDir" \
        --mask_filter _mask \
        --img_filter _img \
        --pretrained_model "$model" \
        --learning_rate 0.00001 --weight_decay 0.0001 \
        --n_epochs 500 --save_every 50 \
        --savedir "$outdir" --model_name_out "$name" \
        --verbose


