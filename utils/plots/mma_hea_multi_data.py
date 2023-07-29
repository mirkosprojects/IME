#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import matplotlib.pyplot as plt
import itertools
from plot_utils import read_results

def main():
    """
    Create mean matching accuracy vs pixel threshold plot from the overall_results.csv files of multiple datasets
    
    Create homography estimation accuracy vs pixel threshold plot from the overall_results.csv files of multiple datasets
    """

    # iteratable linestyles and colors
    linestyles = ['solid', 'dotted', 'dashed', 'dashdot']
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'] # get default color cycle

    # create figure and axes
    fig, axs = plt.subplots(1, 3, figsize=(17, 5), sharey=True)    

    for dataset_dir, linestyle in zip(result_dirs, itertools.cycle(linestyles)):

        ######## Mean Matching Accuracy (MMA) #########

        mma_illumination, mma_viewpoint, mma_all, pixel_thresholds = read_results(os.path.join(dataset_dir, 'overall_results_mma.csv'))
        
        # create illumination subplot
        for alg, color in zip(sorted(mma_illumination.keys()), itertools.cycle(colors)):
            axs[0].plot(pixel_thresholds, mma_illumination[alg], linestyle=linestyle, color=color, label=alg)

        # create viewpoint subplot
        for alg, color in zip(sorted(mma_viewpoint.keys()), itertools.cycle(colors)):
            axs[1].plot(pixel_thresholds, mma_viewpoint[alg], linestyle=linestyle, color=color, label=alg)
        
        # create all subplot
        for alg, color in zip(sorted(mma_all.keys()), itertools.cycle(colors)):
            axs[2].plot(pixel_thresholds, mma_all[alg], linestyle=linestyle, color=color, label=alg)
        
    # labels, title and legend
    for ax in axs:
        ax.set_xlabel('Pixel Threshold')
        ax.set_ylabel('MMA')
        ax.yaxis.set_tick_params(labelbottom=True)
        ax.set_ylim([0, 1])
    axs[0].set_title('Illumination')
    axs[1].set_title('Viewpoint')
    axs[2].set_title('All')
    axs[2].legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    plt.savefig(os.path.join(result_directory, f"mma_{result_name}.png"), dpi=300)

    # create figure and axes
    fig, axs = plt.subplots(1, 3, figsize=(17, 5), sharey=True)

    for dataset_dir, linestyle in zip(result_dirs, itertools.cycle(linestyles)):
        ######## Homography Estimation Accuracy (HEA) #########

        hea_illumination, hea_viewpoint, hea_all, pixel_thresholds = read_results(os.path.join(dataset_dir, 'overall_results_hom.csv'))

        # create illumination subplot
        for alg, color in zip(sorted(hea_illumination.keys()), itertools.cycle(colors)):
            axs[0].plot(pixel_thresholds, hea_illumination[alg], linestyle=linestyle, color=color, label=alg)

        # create viewpoint subplot
        for alg, color in zip(sorted(hea_viewpoint.keys()), itertools.cycle(colors)):
            axs[1].plot(pixel_thresholds, hea_viewpoint[alg], linestyle=linestyle, color=color, label=alg)
        
        # create all subplot
        for alg, color in zip(sorted(hea_all.keys()), itertools.cycle(colors)):
            axs[2].plot(pixel_thresholds, hea_all[alg], linestyle=linestyle, color=color, label=alg)
        
    # labels, title and legend
    for ax in axs:
        ax.set_xlabel('Pixel Threshold')
        ax.set_ylabel('HEA')
        ax.yaxis.set_tick_params(labelbottom=True)
        ax.set_ylim([0, 1])
    axs[0].set_title('Illumination')
    axs[1].set_title('Viewpoint')
    axs[2].set_title('All')
    axs[2].legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    plt.savefig(os.path.join(result_directory, f"hea_{result_name}.png"), dpi=300)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create MMA and HEA plots from multiple datasets',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--result_directory', type=str, default='Results')
    parser.add_argument('--datasets', '--datasets', nargs='+', default=['hpatches'])

    args = parser.parse_known_args()[0]
    result_dirs = [os.path.join(args.result_directory, dataset) for dataset in args.datasets]
    result_directory = args.result_directory
    result_name = "_".join(args.datasets).replace("/", "-")

    main()