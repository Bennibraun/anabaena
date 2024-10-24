#!/bin/bash
#SBATCH --output=/scratch/Users/zaca2954/e_and_o/%x_%j.out
#SBATCH --error=/scratch/Users/zaca2954/e_and_o/%x_%j.err
#SBATCH -p nvidia-a100
#SBATCH -N 1
#SBATCH -c 16
#SBATCH --mem=32gb
#SBATCH --mail-user=zaca2954@colorado.edu

set -euxo pipefail

dataDir="/scratch/Shares/anabaena_mcdb6440"
model='cyto3'
cd "$dataDir" || exit 1

python -m cellpose --train --use_gpu \
			 --verbose --chan 0 --chan2 0 \
			 --dir "$dataDir" \
			 --mask_filter _masks \
			 --img_filter _img \
			 --pretrained_model "$model" \
			 --learning_rate 0.1 --weight_decay 0.0001 \
			 --n_epochs 1

function finish {
		if command -v apprise &> /dev/null
			 then
					 apprise -t "GPU Run Complete" -b "Cyanosegment Train"
					 exit
		fi
}
trap finish EXIT
