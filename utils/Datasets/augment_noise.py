#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import os
from skimage.util import random_noise
from skimage import io
from skimage.color import rgb2gray
import shutil

def args_to_dict(arguments):
    """
    Turn a list of arguments indicated by '--' into a dictonary
    """
    argument_dict = {}            
    split_pos = [idx for idx, argument in enumerate(arguments) if argument.startswith("--")]
    split_pos.append(len(arguments))

    for i in range(len(split_pos) - 1):
        left_pos = split_pos[i]
        right_pos = split_pos[i+1]
        
        if right_pos - left_pos < 2:
            continue

        key = arguments[left_pos].lstrip("--")
        values = arguments[left_pos+1 : right_pos] if len(arguments[left_pos+1 : right_pos]) > 1 else arguments[left_pos+1]

        argument_dict[key] = values
    
    return argument_dict


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

    # check if directories exist
    noisy_dataset_dir = os.path.join(os.path.dirname(dataset_dir), noisy_dataset_name)
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
    # https://stackoverflow.com/questions/59735866/how-to-create-noisy-images-for-data-augmentation
    for img_origin in imagelist:
        # destination path for noisy image
        img_dest = os.path.join(noisy_dataset_dir, os.path.relpath(img_origin, dataset_dir))

        # Read image
        image = io.imread(img_origin)

        # if image is grayscale, convert to grayscale, else image is colored
        if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1) or (len(image.shape) == 3 and image[:,:,0] == image[:,:,1]).all() and (image[:,:,0] == image[:,:,2]).all():
            image = rgb2gray(image)
            grayscale = True
        else:
            grayscale = False

        # Add noise to the image
        image = random_noise(image, mode=noise, **kwargs)

        # change floating point noise to 8-bit
        image = np.array(255 * image, dtype=np.uint8)

        # change to srgb format if greyscale
        if grayscale:
            image = np.stack([image] * 3, axis=-1)

        # save image
        io.imsave(img_dest, image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Algorithm wrapper for augmenting Images in the dataset',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--extensions', '--extensions', nargs='+', default=['.ppm'])
    parser.add_argument('--dataset_dir', type=str)
    parser.add_argument('--name', type=str, default="noisy_dataset")
    parser.add_argument('--noise', type=str, default='gaussian')

    args, unknown_args = parser.parse_known_args()
    file_extensions = args.extensions
    dataset_dir = args.dataset_dir
    noisy_dataset_name = args.name
    noise = args.noise

    # check additional arguments for noise parameters
    kwargs = args_to_dict(unknown_args)
    
    main()