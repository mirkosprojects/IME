#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import cv2
import os
from skimage.util import random_noise
import shutil


def recursive_copy(origin: str, destination: str, ext = ['.ppm'], image_list = []):
    """
    Recursively walks through origin directory and copies all files without the extension 'ext' into destination directory.
    Ouputs a list containing paths of files in origin, that have 'ext' as their extension
    """

    # copy files
    if not os.path.isdir(origin):
        if not any(os.path.basename(origin).endswith(e) for e in ext):
            shutil.copyfile(origin, destination)
        else:
            image_list += [origin]
        return image_list
    
    # copy empty directory
    else:
        if not os.path.exists(destination):
            os.makedirs(destination)
        for element in sorted(os.listdir(origin)):
            new_origin = os.path.join(origin, element)
            new_destination = os.path.join(destination, element)
            recursive_copy(new_origin, new_destination, ext=ext, image_list=image_list)
    
    return image_list


def main():

    # noise additional parameters
    if noise == 's&p':
        kwargs = {
            'amount': 0.011
        }
    elif noise == 'speckle':
        kwargs = {
            'mean': 0.1
        }
    else:
        kwargs = {}

    # check if directories exist
    noisy_dataset_dir = os.path.join(os.path.dirname(dataset_dir), os.path.basename(dataset_dir) + '_' + noise)
    if os.path.exists(noisy_dataset_dir):
        print(f"Dataset {noisy_dataset_dir} already exists, exiting...")
        return(1)
    
    if not os.path.isdir(dataset_dir):
        print(f"Dataset {dataset_dir} doesn't exists, exiting...")
        return(1)
    
    # create list of all files with defined extension
    imagelist = recursive_copy(dataset_dir, noisy_dataset_dir, ext=file_extensions)

    # save information about noise to textfile
    kwargs_str = "\n".join(f"{key}: {value}" for key, value in kwargs.items())
    with open(os.path.join(noisy_dataset_dir, 'noise.txt'), 'w') as f:
        f.write(f"type: {noise}\n{kwargs_str}")

    # add noise to all images from the list
    for img_origin in imagelist:
        # destination path for noisy image
        img_dest = os.path.join(noisy_dataset_dir, os.path.relpath(img_origin, dataset_dir))

        # Read image
        image = cv2.imread(img_origin)

        # TODO: differentiate between color and grayscale images for noise
        # if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1) or (len(image.shape) == 3 and image[:,:,0] == image[:,:,1]).all() and (image[:,:,0] == image[:,:,2]).all():
        #     image = cv2.imread(img_path,0)

        # Add noise to the image
        image = random_noise(image, mode=noise, **kwargs)

        # change floating point noise to 8-bit
        image = np.array(255 * image, dtype=np.uint8)

        # save image
        cv2.imwrite(img_dest, image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Algorithm wrapper for augmenting Images in the dataset',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--extensions', '--extensions', nargs='+', default=['.ppm'])
    parser.add_argument('--dataset_dir', type=str)
    parser.add_argument('--noise', type=str, default='s&p')

    args = parser.parse_known_args()[0]
    file_extensions = args.extensions
    dataset_dir = args.dataset_dir
    noise = args.noise

    main()