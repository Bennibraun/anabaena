# Anabaena Image Segmentation and Classification
This repository contains tools for segmenting and classifying images related to the *Anabaena* dataset, with the ability to handle large files and work in high-performance computing environments like BioFrontiers Super Computer FIJI.

## Table of Contents
1. [Install Instructions](#install-instructions)
2. [Data Management](#data-management)
3. [Execution Instructions](#execution-instructions)
4. [Project Directory](#project-directory)
5. [Developers](#developers)

## Install Instructions
### Conda/Mamba/Micromamba environment setup
Using a conda / mamba / micromamba environment please use
``` bash
conda {or mamba or micromamba} env create -f anabaena/env/env.yml
```

Please check this environemnt has all the same dependencies as ours to do so please use the following
``` bash
conda {or mamba or micromamba} env export --no-builds > env_{yourname}.yml
python env/check_yaml.py {filepath-to-your-newly-created-env}.yml {filepath-to-another-env}.yml
```

an example would be 
``` bash
python env/check_yaml.py anabaena/env/bens_env.yml anabaena/env/env_zac.yml
```

and this will print any dependencies with version mismatch. 

### Poetry Installation (Alternative)

Additionally, you can install an environment using the `pyproject.toml`. To do so, please use `poetry` (or an alternative) with the following command:
``` bash
poetry install
```

## Data Management

These movies that we are working with contain a non-trivial file size and can be run locally, but it is reccomended to use a super computer. In our case we will use the BioFrontiers Super Computer FIJI, also note that these files should be saved in your `Scratch/` directory for better image processing. This must be done locally (not connected to fiji) To upload files to the cluster using a macOS please use the command:
### Uploading files to the cluster 
#### macOS
``` bash
rsync -avz -e ssh --progress /Volumes/[drive name]/* [username]@fiji.colorado.edu:[path to directory on fiji]
```

#### Windows
``` bash
rsync -avz -e ssh --progress /drives/y/* [username]@fiji.colorado.edu:[path to directory on fiji]
```

For more information checkout the shell script `anabaena/src/shell_scripts/rsync_datasets_from_biofstorage.sh`

## Execution Instructions
To run the script, use the following command in your terminal:
```bash
python run_segmentation.py --input_file input.nd2 --output_file output.tiff --model model_name [--gpu] [--start_frame frame_number] [--end_frame frame_number] [--debug]
```
Replace *input.nd2* with the path to your input ND2 file, *output.tiff* with the desired output TIFF file name, and *model_name* with the path of the model you want to use. The script will run segmentation on all frames (or a specified subset) of the input file and save the results as a TIFF stack.

Optional arguments:
- *--gpu*: Use GPU for segmentation if available. This gives a ~2-10x speedup depending on your hardware.
- *--start_frame frame_number*: The first frame to start segmentation on. Default is 0.
- *--end_frame frame_number*: The last frame to end segmentation on. If not provided, the script will segment all frames.
- *--debug*: Run in debug mode, which saves additional output files (flows and probabilities).

Example usage:
```bash
python run_segmentation.py --input_file data/movie.nd2 --output_file results/segmented.tiff --model models/7002_CAH_default --gpu --start_frame 10 --end_frame 50 --debug
```
This command will run segmentation on the frames 10 to 50 of *data/movie.nd2* using the 'cyto' model, and save the results as a TIFF stack in *results/segmented.tiff*. It will also save additional files with flows and probabilities for debugging purposes.


## Project directory
``` bash
anabaena/
├── env/
│   ├── check_yaml.py
│   ├── env_barebones.yml # does not contain versions of dependencies
│   └── env_working.yml   # does contain versions of dependencies 
├── models/
│   ├── 7002/             # unsure what this model is
│   └── 33047/            # previous models for the anabaena
├── src/
│   ├── classification/   # contains python scripts for classification, future problem to focus on
│   ├── file_formatting/   # contains python scripts for file formatting
│   │   ├── __init__.py
│   │   ├── README.md
│   │   └──  standardize_file_types.py  
│   ├── run/              # contains python and shell scripts for running classification and segmentation
│   ├── segmentation/     # contains python scripts for segmentation, generating the segmentation models
│   │   ├── __init__.py
│   │   ├── diff_masks.py
│   │   ├── gen_ground_truths.py
│   │   └── segmentation_comparison.py
│   ├── shell_scripts/    # contains shell and sbatch scripts for automating the train, test, benchmarking, and synching data process
│   └── utils/    # contains all the utility functions necessary in out analysis
├── __init__.py 
├── .gitignore
├── CHANGELOG
├── LICENSE
├── pyproject.toml
├── README.md
├── shell.nix
└── TODO.md
```

## Developers

This code is open source and has been initially developed by the Cameron Lab at CU Boulder under this repo. And this repo is designated for the development and improvement of this inital source for the MCDB-6440 course project. 

### Contributers
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Bennibraun">
        <img src="https://github.com/Bennibraun.png" width="300" />
      </a>
      <br />
      <b>Ben</b>
    </td>
    <td align="center">
      <a href="https://github.com/MichaelLuzadder">
        <img src="https://github.com/MichaelLuzadder.png" width="300" />
      </a>
      <br />
      <b>Michael</b>
    </td>
    <td align="center">
      <a href="https://github.com/caterer-z-t">
        <img src="https://github.com/caterer-z-t.png" width="300" />
      </a>
      <br />
      <b>Zac</b>
    </td>
  </tr>
</table>