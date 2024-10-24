CLI training options
[documentation](https://cellpose.readthedocs.io/en/latest/train.html)
``` bash
--train               train network using images in dir
--train_size          train size network at end of training
--test_dir TEST_DIR   folder containing test data (optional)
--mask_filter MASK_FILTER
                        end string for masks to run on. use '_seg.npy' for
                        manual annotations from the GUI. Default: _masks
--diam_mean DIAM_MEAN
                        mean diameter to resize cells to during training -- if
                        starting from pretrained models it cannot be changed
                        from 30.0
--learning_rate LEARNING_RATE
                        learning rate. Default: 0.2
--weight_decay WEIGHT_DECAY
                        weight decay. Default: 1e-05
--n_epochs N_EPOCHS   number of epochs. Default: 500
--batch_size BATCH_SIZE
                        batch size. Default: 8
--min_train_masks MIN_TRAIN_MASKS
                        minimum number of masks a training image must have to
                        be used. Default: 5
--SGD SGD             use SGD
--save_every SAVE_EVERY
                        number of epochs to skip between saves. Default: 100
--model_name_out MODEL_NAME_OUT
                        Name of model to save as, defaults to name describing
                        model architecture. Model is saved in the folder
                        specified by --dir in models subfolder.
```

retraining the model
``` bash
python cellpose\gui\make_train.py --help
usage: make_train.py [-h] [--dir DIR] [--image_path IMAGE_PATH] [--look_one_level_down] [--img_filter IMG_FILTER]
                    [--channel_axis CHANNEL_AXIS] [--z_axis Z_AXIS] [--chan CHAN] [--chan2 CHAN2] [--invert]
                    [--all_channels] [--anisotropy ANISOTROPY] [--sharpen_radius SHARPEN_RADIUS]
                    [--tile_norm TILE_NORM] [--nimg_per_tif NIMG_PER_TIF] [--crop_size CROP_SIZE]

cellpose parameters

options:
-h, --help            show this help message and exit

input image arguments:
--dir DIR             folder containing data to run or train on.
--image_path IMAGE_PATH
                        if given and --dir not given, run on single image instead of folder (cannot train with this
                        option)
--look_one_level_down
                        run processing on all subdirectories of current folder
--img_filter IMG_FILTER
                        end string for images to run on
--channel_axis CHANNEL_AXIS
                        axis of image which corresponds to image channels
--z_axis Z_AXIS       axis of image which corresponds to Z dimension
--chan CHAN           channel to segment; 0: GRAY, 1: RED, 2: GREEN, 3: BLUE. Default: 0
--chan2 CHAN2         nuclear channel (if cyto, optional); 0: NONE, 1: RED, 2: GREEN, 3: BLUE. Default: 0
--invert              invert grayscale channel
--all_channels        use all channels in image if using own model and images with special channels
--anisotropy ANISOTROPY
                        anisotropy of volume in 3D

algorithm arguments:
--sharpen_radius SHARPEN_RADIUS
                        high-pass filtering radius. Default: 0.0
--tile_norm TILE_NORM
                        tile normalization block size. Default: 0
--nimg_per_tif NIMG_PER_TIF
                        number of crops in XY to save per tiff. Default: 10
--crop_size CROP_SIZE
                        size of random crop to save. Default: 512
```

training from a pretuned model 
``` bash 
python -m cellpose \
--dir ~/images_cyto/test/  \
--pretrained_model ~/images_cyto/test/model/cellpose_35_0 \
--save_png
```

submitting in juptyer notebook
``` python
from cellpose import io, models, train
io.logger_setup()

output = io.load_train_test_data(train_dir, test_dir, image_filter="_img",
                                mask_filter="_masks", look_one_level_down=False)
images, labels, image_names, test_images, test_labels, image_names_test = output

# e.g. retrain a Cellpose model
model = models.CellposeModel(model_type="cyto3")

model_path, train_losses, test_losses = train.train_seg(model.net,
                            train_data=images, train_labels=labels,
                            channels=[1,2], normalize=True,
                            test_data=test_images, test_labels=test_labels,
                            weight_decay=1e-4, SGD=True, learning_rate=0.1,
                            n_epochs=100, model_name="my_new_model")
```