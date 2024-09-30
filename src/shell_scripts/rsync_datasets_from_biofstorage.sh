#!/bin/bash

# This script illustrates how to upload data to Fiji from a local machine.
# I wrote it specifically for my account and for use in Windows so it may need adjustment for Mac/Linux

# Note that this cannot be run on Fiji. It needs to be on the machine that has Biofstorage mounted

rsync -avz -e ssh --progress /drives/y/* bebr1814@fiji.colorado.edu:~/projects/anabaena/scratch_data/train_data/

# The mac version would look something like this:
rsync -avz -e ssh --progress /Volumes/[drive name]/* [username]@fiji.colorado.edu:[path to directory on fiji]

