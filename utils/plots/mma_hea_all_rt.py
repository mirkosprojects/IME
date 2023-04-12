#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import itertools
import numpy as np

def read_results(filename: str, pixel_thresholds: list):
    """Reads the overall_results.csv file and returns dictonaries containing the results"""
    res_illumination = {}
    res_viewpoint = {}
    res_all = {}

    # read csv file into dictonaries
    with open(filename) as f:
        for idx, line in enumerate(f):
            line = line.split(',')
            alg = line[0]
            if idx >=2:
                res_illumination[alg] = [float(line[i+1]) for i, value in enumerate(pixel_thresholds)]
                res_viewpoint[alg] = [float(line[i+13]) for i, value in enumerate(pixel_thresholds)]
                res_all[alg] = [float(line[i+25]) for i, value in enumerate(pixel_thresholds)]
    return res_illumination, res_viewpoint, res_all

def main():
    """
    Create mean matching accuracy vs pixel threshold plot from the overall_results.csv files of multiple ratio thresholds.
    
    Create homography estimation accuracy vs pixel threshold plot from the overall_results.csv files of multiple ratio thresholds.
    """

    # iteratable colors
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'] # get default color cycle

    # create figure and axes
    fig, axs = plt.subplots(len(ratio_thresholds), 3, figsize=(17, 5*len(ratio_thresholds)), sharey=True)
    
    for idx, (rt_dir, rt) in enumerate(zip(result_dirs, ratio_thresholds)):

        ######## Mean Matching Accuracy (MMA) #########

        mma_illumination, mma_viewpoint, mma_all = read_results(os.path.join(rt_dir, 'overall_results_mma.csv'), pixel_thresholds)
        
        # create illumination subplot
        for alg, color in zip(sorted(mma_illumination.keys()), itertools.cycle(colors)):
            axs[idx][0].plot(pixel_thresholds, mma_illumination[alg],color=color, label=alg)

        # create viewpoint subplot
        for alg, color in zip(sorted(mma_viewpoint.keys()), itertools.cycle(colors)):
            axs[idx][1].plot(pixel_thresholds, mma_viewpoint[alg], color=color, label=alg)
        
        # create all subplot
        for alg, color in zip(sorted(mma_all.keys()), itertools.cycle(colors)):
            axs[idx][2].plot(pixel_thresholds, mma_all[alg], color=color, label=alg)

    # labels, title and legend
    for ax in axs[-1]:
        ax.set_xlabel('Pixel Threshold')
        ax.yaxis.set_tick_params(labelbottom=True)
    for ax, rt in zip(list(zip(*axs))[0], ratio_thresholds):
        ax.set_ylabel(f"MMA @ rt={rt}")
        ax.set_ylim([0, 1])
    axs[0][0].set_title('Illumination')
    axs[0][1].set_title('Viewpoint')
    axs[0][2].set_title('All')
    axs[0][2].legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    plt.savefig(os.path.join(os.path.dirname(result_dirs[0]), 'mma_all.png'), dpi=300)

    # create figure and axes
    fig, axs = plt.subplots(len(ratio_thresholds), 3, figsize=(17, 5*len(ratio_thresholds)), sharey=True)

    for idx, (rt_dir, rt) in enumerate(zip(result_dirs, ratio_thresholds)):
        ######## Homography Estimation Accuracy (HEA) #########

        hea_illumination, hea_viewpoint, hea_all = read_results(os.path.join(rt_dir, 'overall_results_hom.csv'), pixel_thresholds)

        # create illumination subplot
        for alg, color in zip(sorted(hea_illumination.keys()), itertools.cycle(colors)):
            axs[idx][0].plot(pixel_thresholds, hea_illumination[alg], color=color, label=alg)

        # create viewpoint subplot
        for alg, color in zip(sorted(hea_viewpoint.keys()), itertools.cycle(colors)):
            axs[idx][1].plot(pixel_thresholds, hea_viewpoint[alg], color=color, label=alg)
        
        # create all subplot
        for alg, color in zip(sorted(hea_all.keys()), itertools.cycle(colors)):
            axs[idx][2].plot(pixel_thresholds, hea_all[alg], color=color, label=alg)
        
    # labels, title and legend
    for ax in axs[-1]:
        ax.set_xlabel('Pixel Threshold')
        ax.yaxis.set_tick_params(labelbottom=True)
    for ax, rt in zip(list(zip(*axs))[0], ratio_thresholds):
        ax.set_ylabel(f"HEA @ rt={rt}")
        ax.set_ylim([0, 1])
    axs[0][0].set_title('Illumination')
    axs[0][1].set_title('Viewpoint')
    axs[0][2].set_title('All')
    axs[0][2].legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    plt.savefig(os.path.join(os.path.dirname(result_dirs[0]), 'hea_all.png'), dpi=300)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create mma and hea plots',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--result_directory', type=str, default='Results')
    parser.add_argument('--dataset', type=str, default='hpatches')
    parser.add_argument('--pixel_thresholds', '--pixel_thresholds', nargs='+', default=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    parser.add_argument('--ratio_thresholds', '--ratio_thresholds', nargs='+', default=['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])

    args = parser.parse_known_args()[0]
    result_dirs = [os.path.join(args.result_directory, args.dataset, rt) for rt in args.ratio_thresholds]
    pixel_thresholds = args.pixel_thresholds
    ratio_thresholds = args.ratio_thresholds

    main()